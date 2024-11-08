"""
DotPrompt - A template engine for structured chat messages
"""

from .types import Role, Part, MediaPart, MessageData, DocumentData, PromptMetadata
from .prompt import DotPrompt

__all__ = [
    "DotPrompt",
    "Role",
    "Part",
    "MediaPart",
    "MessageData",
    "DocumentData",
    "PromptMetadata",
]

__version__ = "1.0.0"
