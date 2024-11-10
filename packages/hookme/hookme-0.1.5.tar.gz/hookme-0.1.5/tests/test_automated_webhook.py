import pytest
import sqlite3
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from hookme.automated_webhook import AutomatedWebhook
from hookme.exceptions import WebhookValidationError

TEST_WEBHOOK_URL = "https://discord.com/api/webhooks/1304930652004552837/YkCna9BYYvYl6ZHrGQ5lVvJZxbSDknqolnDP1gh0lU3_JFhhvBEFzH2GkdhJk8UUvtLk"
TEST_DB = "test_webhook_automation.db"

@pytest.fixture
def automated_webhook():
    webhook = AutomatedWebhook(TEST_WEBHOOK_URL, TEST_DB)
    yield webhook
    # Cleanup
    webhook.stop_scheduler()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_init_db(automated_webhook):
    """Test database initialization"""
    with sqlite3.connect(TEST_DB) as conn:
        # Verify tables exist
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = {row[0] for row in cursor.fetchall()}
        assert "scheduled_webhooks" in tables
        assert "webhook_logs" in tables

@patch('hookme.d_webhook.DiscordWebhook.send_message')
def test_schedule_message(mock_send, automated_webhook):
    """Test scheduling a regular message"""
    mock_send.return_value = MagicMock(status_code=204)
    
    webhook_id = automated_webhook.schedule_message(
        schedule_type='interval',
        schedule_value='1h',
        content='Test message'
    )
    
    assert webhook_id > 0
    
    # Verify database entry
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.execute(
            "SELECT * FROM scheduled_webhooks WHERE id = ?",
            (webhook_id,)
        )
        webhook_data = cursor.fetchone()
        assert webhook_data is not None
        assert webhook_data[2] == '1h'  # schedule_value
        assert webhook_data[3] == 'message'  # message_type
        assert webhook_data[4] == 'Test message'  # content

@patch('hookme.d_webhook.DiscordWebhook.send_embed')
def test_schedule_embed(mock_send, automated_webhook):
    """Test scheduling an embed message"""
    mock_send.return_value = MagicMock(status_code=204)
    
    webhook_id = automated_webhook.schedule_embed(
        schedule_type='cron',
        schedule_value='0 9 * * *',
        title='Test Embed',
        description='Test description',
        color=0xFF0000
    )
    
    assert webhook_id > 0
    
    # Verify database entry
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.execute(
            "SELECT * FROM scheduled_webhooks WHERE id = ?",
            (webhook_id,)
        )
        webhook_data = cursor.fetchone()
        assert webhook_data is not None
        assert webhook_data[2] == '0 9 * * *'  # schedule_value
        assert webhook_data[3] == 'embed'  # message_type
        assert 'Test Embed' in webhook_data[5]  # embed_data

def test_scheduler_start_stop(automated_webhook):
    """Test scheduler start and stop functionality"""
    assert not automated_webhook._running
    
    automated_webhook.start_scheduler()
    assert automated_webhook._running
    
    automated_webhook.stop_scheduler()
    assert not automated_webhook._running

@patch('hookme.d_webhook.DiscordWebhook.send_message')
def test_webhook_execution(mock_send, automated_webhook):
    """Test webhook execution"""
    # Create a proper mock response
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_send.return_value = mock_response
    
    webhook_id = automated_webhook.schedule_message(
        schedule_type='interval',
        schedule_value='1h',
        content='Test execution'
    )
    
    # Set row_factory before executing webhook
    with sqlite3.connect(TEST_DB) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT * FROM scheduled_webhooks WHERE id = ?",
            (webhook_id,)
        )
        # Verify webhook was created
        assert cursor.fetchone() is not None
    
    # Manually trigger execution
    automated_webhook._execute_webhook(webhook_id)
    
    # Verify log entry
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.execute(
            "SELECT * FROM webhook_logs WHERE scheduled_webhook_id = ?",
            (webhook_id,)
        )
        log_entry = cursor.fetchone()
        assert log_entry is not None
        assert log_entry[2] == 'success'  # status
        assert log_entry[3] == 204  # response_code

def test_get_webhook_logs(automated_webhook):
    """Test log retrieval functionality"""
    # Create some test logs
    webhook_id = automated_webhook.schedule_message(
        schedule_type='interval',
        schedule_value='1h',
        content='Test logs'
    )
    
    # Insert test log entries
    with sqlite3.connect(TEST_DB) as conn:
        conn.execute(
            """
            INSERT INTO webhook_logs 
            (scheduled_webhook_id, status, response_code)
            VALUES (?, ?, ?)
            """,
            (webhook_id, 'success', 204)
        )
        conn.execute(
            """
            INSERT INTO webhook_logs 
            (scheduled_webhook_id, status, error_message)
            VALUES (?, ?, ?)
            """,
            (webhook_id, 'error', 'Test error')
        )
    
    # Test filtering
    logs = automated_webhook.get_webhook_logs(webhook_id=webhook_id)
    assert len(logs) == 2
    
    error_logs = automated_webhook.get_webhook_logs(
        webhook_id=webhook_id,
        status='error'
    )
    assert len(error_logs) == 1
    assert error_logs[0]['error_message'] == 'Test error'

@patch('hookme.automated_webhook.CustomScheduler')
def test_schedule_job_interval(mock_scheduler_class, automated_webhook):
    """Test job scheduling with intervals"""
    # Create a mock instance
    mock_scheduler = MagicMock()
    mock_scheduler_class.return_value = mock_scheduler
    automated_webhook.scheduler = mock_scheduler
    
    webhook_id = automated_webhook.schedule_message(
        schedule_type='interval',
        schedule_value='2h',
        content='Test interval'
    )
    
    automated_webhook._schedule_job(webhook_id, 'interval', '2h')
    mock_scheduler.add_interval_job.assert_called_once_with(
        automated_webhook._execute_webhook,
        timedelta(hours=2),
        webhook_id
    )

@patch('hookme.automated_webhook.CustomScheduler')
def test_schedule_job_cron(mock_scheduler_class, automated_webhook):
    """Test job scheduling with cron"""
    # Create a mock instance
    mock_scheduler = MagicMock()
    mock_scheduler_class.return_value = mock_scheduler
    automated_webhook.scheduler = mock_scheduler
    
    webhook_id = automated_webhook.schedule_message(
        schedule_type='cron',
        schedule_value='0 9 * * *',
        content='Test cron'
    )
    
    automated_webhook._schedule_job(webhook_id, 'cron', '0 9 * * *')
    mock_scheduler.add_daily_job.assert_called_once_with(
        automated_webhook._execute_webhook,
        '09:00',
        webhook_id
    )

def test_invalid_interval(automated_webhook):
    """Test handling of invalid interval values"""
    with pytest.raises(ValueError) as exc_info:
        automated_webhook._schedule_job(1, 'interval', '1x')
    assert "Invalid interval unit" in str(exc_info.value)

def test_context_manager(automated_webhook):
    """Test context manager functionality"""
    with automated_webhook as webhook:
        assert not webhook._running
        webhook.start_scheduler()
        assert webhook._running
    
    assert not automated_webhook._running 