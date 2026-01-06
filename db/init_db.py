from db.session import engine
from db.models import Base
from db import models 

Base.metadata.create_all(bind=engine)
print("Database tables created.")
