import pytest
import responses
import time
from unittest.mock import patch
from hookme.d_webhook import DiscordWebhook
from hookme.exceptions import (
    WebhookError,
    WebhookTimeoutError,
    WebhookRateLimitError,
    WebhookConnectionError,
    WebhookValidationError
)
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1304930652004552837/YkCna9BYYvYl6ZHrGQ5lVvJZxbSDknqolnDP1gh0lU3_JFhhvBEFzH2GkdhJk8UUvtLk"

@pytest.fixture
def webhook():
    return DiscordWebhook(WEBHOOK_URL, max_retries=2)

@responses.activate
def test_retry_on_server_error(webhook):
    # First attempt fails, second succeeds
    responses.add(
        responses.POST,
        WEBHOOK_URL,
        status=500,
        json={"message": "Internal Server Error"}
    )
    responses.add(
        responses.POST,
        WEBHOOK_URL,
        status=204
    )
    
    with patch('time.sleep') as mock_sleep:  # Mock sleep to speed up tests
        response = webhook.send_message("test")
        assert response.status_code == 204
        assert mock_sleep.called

@responses.activate
def test_retry_with_rate_limit(webhook):
    # Add rate limit response followed by success
    responses.add(
        responses.POST,
        WEBHOOK_URL,
        status=429,
        json={"message": "Too Many Requests"},
        headers={"Retry-After": "2"}
    )
    responses.add(
        responses.POST,
        WEBHOOK_URL,
        status=204
    )
    
    with patch('time.sleep') as mock_sleep:
        response = webhook.send_message("test")
        assert response.status_code == 204
        # Verify we respected the Retry-After header
        mock_sleep.assert_called_with(2.0)

@responses.activate
def test_max_retries_exceeded(webhook):
    # All attempts fail
    for _ in range(3):  # Initial attempt + 2 retries
        responses.add(
            responses.POST,
            WEBHOOK_URL,
            status=500,
            json={"message": "Internal Server Error"}
        )
    
    with patch('time.sleep'), pytest.raises(WebhookError) as exc_info:
        webhook.send_message("test")
    assert exc_info.value.status_code == 500

@responses.activate
def test_exponential_backoff(webhook):
    # Add multiple failures to trigger backoff
    for _ in range(2):
        responses.add(
            responses.POST,
            WEBHOOK_URL,
            status=500,
            json={"message": "Internal Server Error"}
        )
    responses.add(
        responses.POST,
        WEBHOOK_URL,
        status=204
    )
    
    with patch('time.sleep') as mock_sleep:
        response = webhook.send_message("test")
        assert response.status_code == 204
        # Verify exponential backoff timing
        assert mock_sleep.call_count == 2
        assert mock_sleep.call_args_list[0][0][0] == 1  # First retry after 1 second
        assert mock_sleep.call_args_list[1][0][0] == 2  # Second retry after 2 seconds

@responses.activate
def test_timeout_error(webhook):
    """Test that timeout errors are handled correctly"""
    responses.add(
        responses.POST,
        WEBHOOK_URL,
        body=requests.exceptions.Timeout()
    )
    
    with pytest.raises(WebhookTimeoutError) as exc_info:
        webhook.send_message("test")
    assert "Webhook request timed out after" in str(exc_info.value)

@responses.activate
def test_connection_error(webhook):
    """Test that connection errors are handled correctly"""
    responses.add(
        responses.POST,
        WEBHOOK_URL,
        body=requests.exceptions.ConnectionError()
    )
    
    with pytest.raises(WebhookConnectionError) as exc_info:
        webhook.send_message("test")
    assert "Failed to connect to Discord" in str(exc_info.value)

@responses.activate
def test_rate_limit_max_retries(webhook):
    """Test that rate limit errors are handled correctly when max retries is exceeded"""
    # Add multiple rate limit responses
    for _ in range(3):  # Initial attempt + 2 retries
        responses.add(
            responses.POST,
            WEBHOOK_URL,
            status=429,
            json={"message": "Too Many Requests", "retry_after": 1},
            headers={"Retry-After": "1"}
        )
    
    with patch('time.sleep'), pytest.raises(WebhookError) as exc_info:
        webhook.send_message("test")
    assert "Max retries exceeded" in str(exc_info.value)

@responses.activate
def test_validation_error():
    """Test that invalid webhook URLs are caught"""
    invalid_url = "https://not-discord.com/webhooks/invalid"
    
    with pytest.raises(WebhookValidationError) as exc_info:
        DiscordWebhook(invalid_url)
    assert "Invalid Discord webhook URL format" in str(exc_info.value)

@responses.activate
def test_invalid_payload(webhook):
    """Test that invalid message payloads are caught"""
    # Try to send an invalid message type
    with pytest.raises(WebhookValidationError) as exc_info:
        webhook.send_message({"invalid": "message_type"})
    assert "Content must be a string" in str(exc_info.value)