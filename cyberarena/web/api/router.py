from fastapi.routing import APIRouter

from cyberarena.web.api import (
    connection,
    docs,
    dummy,
    echo,
    economy,
    game,
    monitoring,
    profile,
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])

api_router.include_router(connection.router, prefix="/sign", tags=["sign"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(economy.router, prefix="/economy", tags=["economy"])
api_router.include_router(game.router, prefix="/game", tags=["game"])
