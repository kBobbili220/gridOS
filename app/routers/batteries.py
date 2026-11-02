from fastapi import APIRouter, HTTPException
from psycopg import OperationalError
from psycopg.errors import CheckViolation, ForeignKeyViolation

from app.database import get_connection
from app.schemas import Battery

router = APIRouter(prefix='/batteries', tags=['batteries'])

@router.get("", status_code=200)
def get_batteries():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM batteries ORDER BY battery_id LIMIT 100"
            )
            return cur.fetchall()

@router.delete("/{battery_id}", status_code=204)
def delete_battery(battery_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM batteries WHERE battery_id = %s", 
                    (battery_id,)
                )
                if cur.rowcount == 0:
                    raise HTTPException (
                        status_code=404,
                        detail="Battery not found"
                    )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete bettery with existing telemetry"
        )

    except OperationalError:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )


@router.post("", status_code=201)
def create_battery(battery: Battery):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO batteries (
                    capacity_kwh,
                    location, 
                    max_charge_kw, 
                    max_discharge_kw,
                    min_soc_percent
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING battery_id
                    """,
                    (
                        battery.capacity_kwh,
                        battery.location,
                        battery.max_charge_kw,
                        battery.max_discharge_kw,
                        battery.min_soc_percent
                    )
                )

                result = cur.fetchone()

    except CheckViolation:
        raise HTTPException(
            status_code=422,
            detail="Battery violates database constraints"
        )

    except OperationalError:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )
        
    return {"battery_id": result["battery_id"]}
