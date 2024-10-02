import uvicorn

from recipie.conf import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Bind to all interfaces
        port=8000,
        workers=settings.WORKERS_COUNT,  # Load worker count from settings
    )
