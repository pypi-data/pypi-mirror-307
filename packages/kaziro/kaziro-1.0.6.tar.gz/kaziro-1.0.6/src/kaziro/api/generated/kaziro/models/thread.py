from pydantic import BaseModel


class ThreadMetadata(BaseModel):
    thread_id: str
    user_id: str
    created_at: str
    # Add any other metadata fields that are relevant


class ThreadCreateResponse(BaseModel):
    thread_id: str
