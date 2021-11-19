import fastapi

from .posts import router as posts_router


router = fastapi.APIRouter()
router.include_router(posts_router, prefix='/posts', tags=['posts'])
