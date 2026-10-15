from contextlib import asynccontextmanager
from fastapi import FastAPI
from . import ml,models
from .database import engine
from .router import predict, history

models.Base.metadata.create_all(bind=engine) # creates the table if it doesn't exist
print("Database tables created successfully.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    ml.load_model()
    yield

app = FastAPI(title="House Price API", lifespan=lifespan)

app.include_router(predict.router)
app.include_router(history.router)

@app.get("/health")
def health():
    return {"status": "ok"}