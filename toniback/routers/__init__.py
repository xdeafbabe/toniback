import fastapi

from .blogs import router as blogs_router
from .posts import router as posts_router


router = fastapi.APIRouter()

router.include_router(blogs_router, prefix='/blogs', tags=['blogs'])
router.include_router(posts_router, prefix='/posts', tags=['posts'])
