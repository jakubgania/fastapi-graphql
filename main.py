from fastapi import FastAPI

from routers import graphql_v1

app = FastAPI()

app.include_router(graphql_v1.router)