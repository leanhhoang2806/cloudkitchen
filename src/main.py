from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import (
    health,
    seller_info,
    dish_router,
    media_upload_router,
    buyer_router,
    order_router,
    featured_dish_router,
    search_router,
    payment_router,
    stripe_payment_router,
    discounted_dish_router,
    # chat_router,
    dish_review_router,
    seller_application_router,
)
from alembic.config import Config
from alembic import command


def run_migrations():
    alembic_cfg = Config("./alembic.ini")  # Path to your Alembic configuration file
    command.upgrade(alembic_cfg, "head")


run_migrations()
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
app.include_router(buyer_router.router, prefix="/api/v1")
app.include_router(order_router.router, prefix="/api/v1")
app.include_router(featured_dish_router.router, prefix="/api/v1")
app.include_router(search_router.router, prefix="/api/v1")
app.include_router(payment_router.router, prefix="/api/v1")
app.include_router(stripe_payment_router.router, prefix="/api/v1")
app.include_router(discounted_dish_router.router, prefix="/api/v1")
# app.include_router(chat_router.router, prefix="/api/v1")
app.include_router(dish_review_router.router, prefix="/api/v1")
app.include_router(seller_application_router.router, prefix="/api/v1")
