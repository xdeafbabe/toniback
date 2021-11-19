import fastapi

from . import routers


app = fastapi.FastAPI()
app.include_router(routers.router)
