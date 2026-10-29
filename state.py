from typing import TypedDict

class CommuteState(TypedDict):
    origin: str
    destination: str
    transport_mode: str
    traffic_status: str
    delay_minutes: int
    route_plan: str