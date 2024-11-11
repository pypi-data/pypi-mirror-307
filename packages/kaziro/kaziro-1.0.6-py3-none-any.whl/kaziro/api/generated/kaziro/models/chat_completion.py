from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ChatCompletionMessage(BaseModel):
    role: str
    content: str


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatCompletionMessage


class ChatCompletionResponse(BaseModel):
    id: str
    created: int
    choices: List[ChatCompletionChoice]
    extra: Optional[Dict[str, Any]] = None
