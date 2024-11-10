from .d_webhook import DiscordWebhook
from .automated_webhook import AutomatedWebhook
from .exceptions import WebhookError

__version__ = "0.1.7" # want to remove this from the package
__all__ = ["DiscordWebhook", "WebhookError", "AutomatedWebhook"] 
