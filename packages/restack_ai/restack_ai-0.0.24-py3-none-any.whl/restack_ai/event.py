from pydantic import BaseModel
from typing import Any, Dict, Optional

class WorkflowEvent(BaseModel):
    name: str
    input: Optional[Dict[str, Any]] = None

class SendWorkflowEvent(BaseModel):
    event: WorkflowEvent
    workflow: Optional[str] = None