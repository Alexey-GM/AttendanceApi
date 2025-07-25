from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.utils.jwt import get_current_lecturer_id
from app.models import DisciplinePlan, WorkGroup, Discipline, ActivityType
from app.utils.response import format_response

router = APIRouter()

@router.get("/my-discipline-plans")
async def get_my_discipline_plans(
    db: AsyncSession = Depends(get_db),
    lecturer_id: int = Depends(get_current_lecturer_id),
):
    try:
        q = await db.execute(
            select(DisciplinePlan)
            .where(DisciplinePlan.lecturer_id == lecturer_id)
        )
        plans = q.scalars().all()
        result = []
        for plan in plans:
            # Получаем связанные объекты
            work_group = await db.get(WorkGroup, plan.work_group_id)
            discipline = await db.get(Discipline, plan.discipline_id)
            activity_type = await db.get(ActivityType, plan.activity_type_id)
            result.append({
                "id": plan.id,
                "work_group": {
                    "id": work_group.id,
                    "name": work_group.name,
                    "comment": work_group.comment,
                } if work_group else None,
                "discipline": {
                    "id": discipline.id,
                    "name": discipline.name,
                } if discipline else None,
                "activity_type": {
                    "id": activity_type.id,
                    "short_name": activity_type.short_name,
                    "full_name": activity_type.full_name,
                } if activity_type else None,
                "academic_hours": plan.academic_hours,
            })
        return format_response(data=result, message="Success", code=200)
    except Exception as e:
        return format_response(message=str(e), code=400) 