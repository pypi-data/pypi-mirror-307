import sqlite3
import threading
from datetime import datetime
from typing import Optional, Union, Dict, Any, List
from pathlib import Path
from .d_webhook import DiscordWebhook
import logging
from .scheduler import CustomScheduler, timedelta

logger = logging.getLogger(__name__)

class AutomatedWebhook:
    """Manages automated Discord webhook deliveries with SQLite persistence."""
    
    def __init__(self, webhook_url: str, db_path: str = "webhook_automation.db"):
        """
        Initialize automated webhook manager.
        
        Args:
            webhook_url: Discord webhook URL
            db_path: Path to SQLite database file
        """
        self.webhook = DiscordWebhook(webhook_url)
        self.db_path = db_path
        self._init_db()
        self.scheduler = CustomScheduler()
        self._running = False

    def _init_db(self):
        """Initialize SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scheduled_webhooks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    schedule_type TEXT NOT NULL,
                    schedule_value TEXT NOT NULL,
                    message_type TEXT NOT NULL,
                    content TEXT,
                    embed_data TEXT,
                    files TEXT,
                    enabled BOOLEAN DEFAULT 1,
                    last_run TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS webhook_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scheduled_webhook_id INTEGER,
                    status TEXT NOT NULL,
                    response_code INTEGER,
                    error_message TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (scheduled_webhook_id) 
                        REFERENCES scheduled_webhooks(id)
                )
            """)

    def schedule_message(
        self,
        schedule_type: str,
        schedule_value: str,
        content: str,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None
    ) -> int:
        """
        Schedule a regular message delivery.
        
        Args:
            schedule_type: 'interval' or 'cron'
            schedule_value: For interval: '1h', '30m', etc. For cron: '0 9 * * *'
            content: Message content
            username: Optional webhook username
            avatar_url: Optional webhook avatar URL
            
        Returns:
            int: Scheduled webhook ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO scheduled_webhooks 
                (schedule_type, schedule_value, message_type, content)
                VALUES (?, ?, 'message', ?)
                """,
                (schedule_type, schedule_value, content)
            )
            return cursor.lastrowid

    def schedule_embed(
        self,
        schedule_type: str,
        schedule_value: str,
        title: str,
        description: Optional[str] = None,
        color: Optional[int] = None,
        **embed_kwargs
    ) -> int:
        """Schedule an embed message delivery."""
        embed_data = {
            "title": title,
            "description": description,
            "color": color,
            **embed_kwargs
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO scheduled_webhooks 
                (schedule_type, schedule_value, message_type, embed_data)
                VALUES (?, ?, 'embed', ?)
                """,
                (schedule_type, schedule_value, str(embed_data))
            )
            return cursor.lastrowid

    def _execute_webhook(self, webhook_id: int):
        """Execute a scheduled webhook delivery."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row  # Enable row factory for dict-like access
                cursor = conn.execute(
                    "SELECT * FROM scheduled_webhooks WHERE id = ?",
                    (webhook_id,)
                )
                webhook_data = cursor.fetchone()
                
                if not webhook_data:
                    return
                
                # Execute webhook based on type
                if webhook_data['message_type'] == 'message':
                    response = self.webhook.send_message(webhook_data['content'])
                elif webhook_data['message_type'] == 'embed':
                    embed_data = eval(webhook_data['embed_data'])
                    response = self.webhook.send_embed(**embed_data)
                
                # Log success
                conn.execute(
                    """
                    INSERT INTO webhook_logs 
                    (scheduled_webhook_id, status, response_code)
                    VALUES (?, 'success', ?)
                    """,
                    (webhook_id, response.status_code)
                )
                
                # Update last run time
                conn.execute(
                    """
                    UPDATE scheduled_webhooks 
                    SET last_run = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (webhook_id,)
                )
                
        except Exception as e:
            logger.error(f"Error executing webhook {webhook_id}: {str(e)}")
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO webhook_logs 
                    (scheduled_webhook_id, status, error_message)
                    VALUES (?, 'error', ?)
                    """,
                    (webhook_id, str(e))
                )

    def _schedule_job(self, webhook_id: int, schedule_type: str, schedule_value: str):
        """Add a job to the scheduler."""
        if schedule_type == 'interval':
            # Parse interval value (e.g., '1h', '30m')
            value = int(schedule_value[:-1])
            unit = schedule_value[-1]
            
            if unit == 'h':
                interval = timedelta(hours=value)
            elif unit == 'm':
                interval = timedelta(minutes=value)
            elif unit == 'd':
                interval = timedelta(days=value)
            else:
                raise ValueError(f"Invalid interval unit: {unit}")
                
            self.scheduler.add_interval_job(
                self._execute_webhook,
                interval,
                webhook_id
            )
                
        elif schedule_type == 'cron':
            # Convert cron format to HH:MM
            try:
                parts = schedule_value.split()
                if len(parts) != 5:
                    raise ValueError("Invalid cron format")
                    
                minute, hour = parts[:2]
                # Convert to 24-hour format string
                time_str = f"{int(hour):02d}:{int(minute):02d}"
                
                self.scheduler.add_daily_job(
                    self._execute_webhook,
                    time_str,
                    webhook_id
                )
            except (ValueError, IndexError):
                raise ValueError("Invalid cron format. Expected '* * * * *' format")

    def start_scheduler(self):
        """Start the scheduler."""
        if not self._running:
            self._running = True
            self.scheduler.start()

    def stop_scheduler(self):
        """Stop the scheduler."""
        if self._running:
            self._running = False
            self.scheduler.stop()

    def get_webhook_logs(
        self,
        webhook_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve webhook execution logs with filtering options.
        
        Returns:
            List of log entries as dictionaries
        """
        query = "SELECT * FROM webhook_logs WHERE 1=1"
        params = []
        
        if webhook_id:
            query += " AND scheduled_webhook_id = ?"
            params.append(webhook_id)
            
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date.isoformat())
            
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date.isoformat())
            
        if status:
            query += " AND status = ?"
            params.append(status)
            
        query += " ORDER BY timestamp DESC"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop_scheduler() 