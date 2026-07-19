from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.database.dependencies import get_db

from app.repositories.repair_job_repository import RepairJobRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.ai.openai_service import OpenAIService
from app.services.repair_job_service import RepairJobService

router = APIRouter(
    prefix="/api/ai",
    tags=["AI"],
)


@router.post("/test")
def test_ai(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Test OpenAI connection."""

    ai = OpenAIService()

    result = ai.test_connection()

    return {
        "success": True,
        "response": result,
    }


@router.post("/diagnose/{repair_job_id}")
def diagnose_repair_job(
    repair_job_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Generate an AI diagnosis for a repair job."""

    repair_job_service = RepairJobService(
        RepairJobRepository(db),
        VehicleRepository(db),
    )

    try:
        repair_job = repair_job_service.generate_ai_diagnosis(
            repair_job_id
        )

        return {
            "success": True,
            "repair_job_id": str(repair_job.id),
            "diagnosis": repair_job.ai_diagnosis,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
