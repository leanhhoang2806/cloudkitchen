from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import health, seller_info, dish_router, media_upload_router

app = FastAPI()

# Define allowed origins
origins = ["*"]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


app.include_router(health.router, prefix="/api/v1")
app.include_router(seller_info.router, prefix="/api/v1")
app.include_router(dish_router.router, prefix="/api/v1")
app.include_router(media_upload_router.router, prefix="/api/v1")
