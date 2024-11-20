from fastapi import FastAPI, status

import models
from routers import auth, todos, admin, user
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/healthy", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
