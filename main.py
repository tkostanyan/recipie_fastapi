from fastapi import FastAPI
from recipie.routes import router as recipie_router

app = FastAPI()


@app.get("/")
async def health_check():
    return {"message": "Ok"}


app.include_router(recipie_router, prefix="/recipie", tags=["recipie"])
