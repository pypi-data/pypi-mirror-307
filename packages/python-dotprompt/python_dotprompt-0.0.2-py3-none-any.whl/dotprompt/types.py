from typing import Any, Dict, List, Optional, Union

# Core type definitions
Role = str
Part = Dict[str, Any]
MediaPart = Dict[str, Dict[str, str]]
MessageData = Dict[str, Union[Role, List[Part], Dict[str, Any]]]
DocumentData = Dict[str, Any]


class PromptMetadata:
    """Class for storing prompt metadata"""

    def __init__(self, model: Optional[str] = None):
        self.model = model

    def __repr__(self) -> str:
        return f"PromptMetadata(model={self.model!r})"
