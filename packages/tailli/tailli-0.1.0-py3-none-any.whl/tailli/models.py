from pydantic import BaseModel

class ApiKeyResponse(BaseModel):
    Enabled: bool
    TTL: int

class UsageResponse(BaseModel):
    success: bool