from pydantic import BaseModel, Field, AwareDatetime

class Battery(BaseModel):
    capacity_kwh: float = Field(gt=0)
    location: str | None = None
    max_charge_kw: float = Field(gt=0)
    max_discharge_kw: float = Field(gt=0)
    min_soc_percent: float = Field(default=20, ge=0, le=100)


class Telemetry(BaseModel):
    battery_id: int = Field(gt=0)
    recorded_at: AwareDatetime
    power_kw: float
    temperature_c: float 
    soc_percent: float = Field(ge=0, le=100)