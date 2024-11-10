from .d_webhook import DiscordWebhook
from .automated_webhook import AutomatedWebhook
from .exceptions import WebhookError

__version__ = "0.1.5"
__all__ = ["DiscordWebhook", "WebhookError", "AutomatedWebhook"] 
