import requests
import logging
import time
import re
import html
from urllib.parse import urlparse
from typing import Optional, Union, Dict, Any, Callable, List, BinaryIO, Tuple
from pathlib import Path
import os
import mimetypes
import json
from .exceptions import (
    WebhookError,
    WebhookTimeoutError,
    WebhookRateLimitError,
    WebhookConnectionError,
    WebhookValidationError
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscordWebhook:
    """A class to handle Discord webhook interactions with enhanced security features."""
    
    MAX_RETRIES = 3
    TIMEOUT = 10  # seconds
    BASE_DELAY = 1  # Base delay for exponential backoff
    MAX_PAYLOAD_SIZE = 8 * 1024 * 1024  # 8MB Discord payload limit
    MAX_FILE_SIZE = 8 * 1024 * 1024  # 8MB per file
    MAX_TOTAL_FILES_SIZE = 50 * 1024 * 1024  # 50MB total
    ALLOWED_FILE_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.gif', '.webp',  # Images
        '.mp4', '.webm',  # Videos
        '.mp3', '.ogg', '.wav',  # Audio
        '.txt', '.pdf', '.doc', '.docx',  # Documents
        '.zip', '.rar', '.7z'  # Archives
    }
    
    # Add security constants
    ALLOWED_SCHEMES = {'https'}
    ALLOWED_DOMAINS = {'discord.com', 'discordapp.com'}
    URL_PATTERN = re.compile(
        r'^https?:\/\/((?:ptb\.|canary\.)?discord(?:app)?\.com)\/api\/webhooks\/\d+\/[\w-]+$'
    )
    
    def __init__(
        self,
        webhook_url: str,
        timeout: int = TIMEOUT,
        max_retries: int = MAX_RETRIES,
        logger: Optional[logging.Logger] = None,
        verify_ssl: bool = True
    ):
        """Initialize with enhanced security validation."""
        self._validate_webhook_url(webhook_url)
        self.webhook_url = webhook_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logger or logging.getLogger(__name__)
        self.verify_ssl = verify_ssl
        
        # Configure secure session
        self.session = self._create_secure_session()

    def _create_secure_session(self) -> requests.Session:
        """Create a secure requests session with proper configuration."""
        session = requests.Session()
        session.verify = self.verify_ssl
        
        # Set secure headers
        session.headers.update({
            'User-Agent': 'Discord-Webhook-Handler/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        return session

    def _validate_webhook_url(self, url: str) -> None:
        """Validate webhook URL for security."""
        if not isinstance(url, str):
            raise WebhookValidationError("Webhook URL must be a string")
            
        if not self.URL_PATTERN.match(url):
            raise WebhookValidationError("Invalid Discord webhook URL format")
            
        parsed = urlparse(url)
        if parsed.scheme not in self.ALLOWED_SCHEMES:
            raise WebhookValidationError(f"URL scheme must be in {self.ALLOWED_SCHEMES}")
            
        if parsed.netloc not in self.ALLOWED_DOMAINS:
            raise WebhookValidationError(f"Domain must be in {self.ALLOWED_DOMAINS}")

    def _sanitize_content(self, content: str) -> str:
        """Sanitize content to prevent XSS and other injection attacks."""
        # HTML escape special characters
        content = html.escape(content)
        
        # Remove null bytes and other control characters
        content = ''.join(char for char in content if ord(char) >= 32 or char in '\n\r\t')
        
        # Limit consecutive newlines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()

    def _validate_payload(self, payload: Dict[str, Any]) -> None:
        """Enhanced payload validation with security checks."""
        # Check total payload size
        payload_size = len(str(payload).encode('utf-8'))
        if payload_size > self.MAX_PAYLOAD_SIZE:
            raise WebhookValidationError(f"Payload size exceeds {self.MAX_PAYLOAD_SIZE} bytes")

        # Validate content
        if 'content' in payload:
            if not isinstance(payload['content'], str):
                raise WebhookValidationError("Content must be a string")
            if len(payload['content']) > 2000:
                raise WebhookValidationError("Content length exceeds 2000 characters")
            payload['content'] = self._sanitize_content(payload['content'])

        # Validate username
        if 'username' in payload:
            if not isinstance(payload['username'], str):
                raise WebhookValidationError("Username must be a string")
            if not 1 <= len(payload['username']) <= 80:
                raise WebhookValidationError("Username must be between 1 and 80 characters")
            payload['username'] = self._sanitize_content(payload['username'])

        # Validate embeds
        if 'embeds' in payload and payload['embeds']:
            if not isinstance(payload['embeds'], list):
                raise WebhookValidationError("Embeds must be a list")
            if len(payload['embeds']) > 10:
                raise WebhookValidationError("Maximum of 10 embeds allowed")
                
            for embed in payload['embeds']:
                self._validate_embed(embed)

    def _validate_embed(self, embed: Dict[str, Any]) -> None:
        """Validate embed structure and content."""
        if 'title' in embed:
            if len(embed['title']) > 256:
                raise WebhookValidationError("Embed title exceeds 256 characters")
            embed['title'] = self._sanitize_content(embed['title'])

        if 'description' in embed:
            if len(embed['description']) > 4096:
                raise WebhookValidationError("Embed description exceeds 4096 characters")
            embed['description'] = self._sanitize_content(embed['description'])

        if 'fields' in embed:
            for field in embed['fields']:
                if len(field.get('name', '')) > 256:
                    raise WebhookValidationError("Field name exceeds 256 characters")
                if len(field.get('value', '')) > 1024:
                    raise WebhookValidationError("Field value exceeds 1024 characters")
                field['name'] = self._sanitize_content(field['name'])
                field['value'] = self._sanitize_content(field['value'])

    def _validate_file(self, file: Union[str, Path, BinaryIO], filename: Optional[str] = None) -> None:
        """
        Validate file size and type before upload.
        
        Args:
            file: File path or file-like object
            filename: Optional filename when file is a file-like object
        """
        if isinstance(file, (str, Path)):
            path = Path(file)
            if not path.exists():
                raise WebhookValidationError(f"File not found: {path}")
            
            file_size = path.stat().st_size
            file_ext = path.suffix.lower()
            actual_filename = path.name
        else:
            # For file-like objects
            if not filename:
                raise WebhookValidationError("Filename must be provided for file-like objects")
            
            # Get current position
            current_pos = file.tell()
            # Seek to end to get size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            # Return to original position
            file.seek(current_pos)
            
            file_ext = Path(filename).suffix.lower()
            actual_filename = filename

        if file_size > self.MAX_FILE_SIZE:
            raise WebhookValidationError(
                f"File size {file_size} bytes exceeds maximum of {self.MAX_FILE_SIZE} bytes"
            )

        if file_ext not in self.ALLOWED_FILE_EXTENSIONS:
            raise WebhookValidationError(
                f"File extension {file_ext} not allowed. Allowed extensions: {self.ALLOWED_FILE_EXTENSIONS}"
            )

    def _prepare_file(
        self,
        file: Union[str, bytes, BinaryIO],
        filename: Optional[str] = None
    ) -> Tuple[str, BinaryIO, str]:
        """
        Prepare file for upload, returning filename, file object, and content type.
        """
        if isinstance(file, (str, Path)):
            path = Path(file)
            filename = path.name
            file_obj = open(path, 'rb')
        else:
            if not filename:
                raise WebhookValidationError("Filename must be provided for file-like objects")
            file_obj = file

        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        return filename, file_obj, content_type

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with proper cleanup."""
        self.session.close()

    def _exponential_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff time."""
        return min(self.BASE_DELAY * (2 ** attempt), 60)  # Cap at 60 seconds

    def _should_retry(self, status_code: int) -> bool:
        """Determine if the request should be retried based on status code."""
        return status_code in {429, 500, 502, 503, 504}

    def _make_request_with_retry(
        self,
        request_func: Callable[[], requests.Response]
    ) -> requests.Response:
        """
        Execute a request with retry logic.
        
        Args:
            request_func: Callable that performs the actual request
            
        Returns:
            requests.Response: The response from the server
            
        Raises:
            Various WebhookError types depending on the failure mode
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                response = request_func()
                
                if response.ok:
                    return response
                
                # Handle rate limiting explicitly
                if response.status_code == 429:
                    retry_after = float(response.headers.get("Retry-After", 5))
                    self.logger.warning(f"Rate limited. Waiting {retry_after} seconds")
                    time.sleep(retry_after)
                    continue
                
                # If we should retry based on status code
                if self._should_retry(response.status_code):
                    if attempt < self.max_retries:
                        backoff_time = self._exponential_backoff(attempt)
                        self.logger.warning(
                            f"Request failed with status {response.status_code}. "
                            f"Retrying in {backoff_time} seconds. "
                            f"Attempt {attempt + 1}/{self.max_retries}"
                        )
                        time.sleep(backoff_time)
                        continue
                
                # If we shouldn't retry or we're out of retries, raise appropriate error
                error_msg = f"Webhook request failed: {response.status_code} - {response.text}"
                raise WebhookError(error_msg, status_code=response.status_code, response_text=response.text)
                
            except requests.exceptions.Timeout as e:
                last_exception = e
                if attempt < self.max_retries:
                    backoff_time = self._exponential_backoff(attempt)
                    self.logger.warning(f"Request timed out. Retrying in {backoff_time} seconds")
                    time.sleep(backoff_time)
                    continue
                
            except requests.exceptions.ConnectionError as e:
                last_exception = e
                if attempt < self.max_retries:
                    backoff_time = self._exponential_backoff(attempt)
                    self.logger.warning(f"Connection error. Retrying in {backoff_time} seconds")
                    time.sleep(backoff_time)
                    continue
                
            except Exception as e:
                self.logger.error(f"Unexpected error: {str(e)}")
                raise

        # If we've exhausted all retries, raise the appropriate exception
        if isinstance(last_exception, requests.exceptions.Timeout):
            raise WebhookTimeoutError(f"Webhook request timed out after {self.timeout} seconds")
        elif isinstance(last_exception, requests.exceptions.ConnectionError):
            raise WebhookConnectionError(f"Failed to connect to Discord: {str(last_exception)}")
        else:
            raise WebhookError("Max retries exceeded")

    def send_message(
        self,
        content: str,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        tts: bool = False,
        embeds: Optional[list] = None,
    ) -> requests.Response:
        """Send a message to Discord webhook with enhanced error handling."""
        payload = {
            "content": content,
            "tts": tts,
        }
        
        if username:
            payload["username"] = username
        if avatar_url:
            payload["avatar_url"] = avatar_url
        if embeds:
            payload["embeds"] = embeds

        self._validate_payload(payload)
        
        def make_request():
            self.logger.debug(f"Sending webhook payload: {payload}")
            return self.session.post(
                self.webhook_url,
                json=payload,
                timeout=self.timeout
            )

        return self._make_request_with_retry(make_request)

    def send_embed(
        self,
        title: str,
        description: Optional[str] = None,
        color: Optional[int] = None,
        fields: Optional[list] = None,
        thumbnail_url: Optional[str] = None,
        image_url: Optional[str] = None,
        footer_text: Optional[str] = None,
        footer_icon: Optional[str] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> requests.Response:
        """
        Send an embedded message to Discord webhook.
        
        Args:
            title (str): Embed title
            description (Optional[str]): Embed description
            color (Optional[int]): Color code for the embed
            fields (Optional[list]): List of field dictionaries
            thumbnail_url (Optional[str]): URL for thumbnail
            image_url (Optional[str]): URL for main image
            footer_text (Optional[str]): Footer text
            footer_icon (Optional[str]): Footer icon URL
            username (Optional[str]): Override webhook username
            avatar_url (Optional[str]): Override webhook avatar
            
        Returns:
            requests.Response: The response from Discord's API
        """
        embed = {
            "title": title,
            "type": "rich"
        }
        
        if description:
            embed["description"] = description
        if color:
            embed["color"] = color
        if fields:
            embed["fields"] = fields
        if thumbnail_url:
            embed["thumbnail"] = {"url": thumbnail_url}
        if image_url:
            embed["image"] = {"url": image_url}
        if footer_text:
            embed["footer"] = {
                "text": footer_text,
                "icon_url": footer_icon if footer_icon else None
            }

        return self.send_message(
            content="",
            username=username,
            avatar_url=avatar_url,
            embeds=[embed]
        ) 

    def send_file(
        self,
        file: Union[str, Path, BinaryIO, List[Union[str, Path, BinaryIO]]],
        content: Optional[str] = None,
        filename: Optional[Union[str, List[str]]] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        tts: bool = False,
        embeds: Optional[list] = None,
    ) -> requests.Response:
        """
        Send a file or multiple files to Discord webhook.
        """
        files = []
        total_size = 0
        
        # Normalize to list
        if not isinstance(file, list):
            files_to_process = [(file, filename)]
        else:
            if filename and not isinstance(filename, list):
                raise WebhookValidationError("When sending multiple files, filenames must be a list")
            files_to_process = zip(file, filename or [None] * len(file))

        try:
            # Prepare files
            for idx, (f, fname) in enumerate(files_to_process):
                self._validate_file(f, fname)
                prepared_filename, file_obj, content_type = self._prepare_file(f, fname)
                
                # Check total size
                file_obj.seek(0, os.SEEK_END)
                total_size += file_obj.tell()
                file_obj.seek(0)
                
                if total_size > self.MAX_TOTAL_FILES_SIZE:
                    raise WebhookValidationError(
                        f"Total file size {total_size} bytes exceeds maximum of {self.MAX_TOTAL_FILES_SIZE} bytes"
                    )
                
                files.append(
                    ('file', (prepared_filename, file_obj, content_type))
                )

            # Prepare payload
            payload = {}
            if content:
                payload["content"] = content
            if username:
                payload["username"] = username
            if avatar_url:
                payload["avatar_url"] = avatar_url
            if embeds:
                payload["embeds"] = embeds
            if tts:
                payload["tts"] = tts

            self._validate_payload(payload)

            def make_request():
                self.logger.debug(f"Sending webhook payload with {len(files)} files")
                # Send as multipart/form-data
                return self.session.post(
                    self.webhook_url,
                    files=files,
                    data=payload,  # Send payload as data, not as payload_json
                    timeout=self.timeout
                )

            return self._make_request_with_retry(make_request)

        finally:
            # Clean up file objects
            for _, file_tuple in files:
                try:
                    file_tuple[1].close()
                except:
                    pass

    def send_files_with_embed(
        self,
        files: List[Union[str, Path, BinaryIO]],
        title: str,
        description: Optional[str] = None,
        color: Optional[int] = None,
        filenames: Optional[List[str]] = None,
        **embed_kwargs
    ) -> requests.Response:
        """
        Send multiple files with an embedded message.
        
        Args:
            files: List of files to send
            title: Embed title
            description: Optional embed description
            color: Optional embed color
            filenames: Optional list of filenames for file-like objects
            **embed_kwargs: Additional embed parameters
            
        Returns:
            requests.Response: The response from Discord's API
        """
        embed = {
            "title": title,
            "type": "rich"
        }
        
        if description:
            embed["description"] = description
        if color:
            embed["color"] = color
            
        # Add other embed parameters
        for key, value in embed_kwargs.items():
            if value is not None:
                embed[key] = value

        return self.send_file(
            file=files,
            filename=filenames,
            embeds=[embed]
        )