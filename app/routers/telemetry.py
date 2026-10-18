from fastapi import APIRouter, HTTPException
from psycopg import OperationalError
from psycopg.errors import (
    ForeignKeyViolation,
    UniqueViolation,
    CheckViolation,
)

from app.database import get_connection
from app.schemas import Telemetry

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

@router.get("", status_code=200)
def get_telemetry():
    with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM batteries ORDER BY recorded_at LIMIT 100"
                )
                return cur.fetchall()

@router.post("", status_code=201)
def create_telemetry(readings: list[Telemetry]):
    if not readings:
        raise HTTPException(
            status_code=422,
            detail="Batch must contain at least one reading"
        )

    if len(readings) > 1000:
        raise HTTPException(
            status_code=413,
            detail="Maximum batch size is 1000"
        )

    values = [
        (
            r.battery_id,
            r.recorded_at,
            r.power_kw,
            r.temperature_c,
            r.soc_percent
        )
        for r in readings
    ]

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO telemetry (
                        battery_id,
                        recorded_at,
                        power_kw,
                        temperature_c,
                        soc_percent
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    values
                )

    except ForeignKeyViolation:
        raise HTTPException(
            status_code=404,
            detail="One or more batteries do not exist"
        )

    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Duplicate telemetry reading"
        )

    except CheckViolation:
        raise HTTPException(
            status_code=422,
            detail="Telemetry violates database constraints"
        )

    except OperationalError:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

    return {"inserted": len(readings)}