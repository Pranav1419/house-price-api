from app import models
from app.database import engine

models.Base.metadata.create_all(bind=engine)
print("tables created")