from typing import Optional
from pydantic import BaseModel, Field

class MonitoringCycleSummary(BaseModel):
    status: str = Field(..., description="Status of the cycle: 'completed' or 'failed'")
    farmers_checked: int = Field(..., description="Total count of registered farmers reviewed")
    risks_detected: int = Field(..., description="Count of High and Medium risk hazards identified")
    alerts_simulated: int = Field(..., description="Count of simulated warning messages (demo mode)")
    alerts_sent: int = Field(..., description="Count of warning messages dispatched via live gateway")
    duplicates_suppressed: int = Field(..., description="Count of alerts suppressed due to 24-hour guard")
    duplicates_skipped: Optional[int] = Field(None, description="Alias for duplicates_suppressed")
    failures: int = Field(..., description="Count of weather API failures, dispatch errors, or unhandled exceptions")
    cycle_duration_seconds: float = Field(..., description="Execution duration in seconds")
    error: Optional[str] = Field(None, description="Top-level error message if cycle failed to start")
