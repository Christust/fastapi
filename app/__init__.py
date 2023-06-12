from fastapi import FastAPI
from app.routers import router

app = FastAPI(
    title="FastAPI",
    description="API prueba",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags = [
    {
        "name": "Users",
        "description": "Operations with users.",
    },
    {
        "name": "Auth",
        "description": "Auth operations.",
    },
]


)

app.include_router(router)
