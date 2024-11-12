from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateGreetingV0(BaseModel):
    app_id: Optional[int] = None
    greeting_is_anonymous: bool
    greeting_anonymous_sender_name: Optional[str] = None
    user_id: Optional[UUID] = None
    greeting_text: Optional[str] = None
