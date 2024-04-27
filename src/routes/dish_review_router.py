from fastapi import Depends, Response, status
from src.validations.validators import validate_token
from src.managers.Dish_Review_manager import DishReviewManager
from src.models.data_model import DishReviewCreateWithS3, DishReviewCreate
from src.models.postgres_model import DishReviewPydantic
from src.managers.s3_manager import S3_UPLOADER
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter
from typing import Optional, List


router = CustomAPIRouter()
dish_review_manager = DishReviewManager()


@router.post("/dish-review/", response_model=DishReviewPydantic)
async def create_dish_review(
    payload: DishReviewCreate,
    token=Depends(validate_token),
):
    s3_path = S3_UPLOADER.upload_to_s3_no_validation(payload.image_data)
    review = dish_review_manager.create(
        DishReviewCreateWithS3(
            s3_path=s3_path,
            dish_id=payload.dish_id,
            buyer_id=payload.buyer_id,
            content=payload.content,
            rating=payload.rating,
        )
    )
    return DishReviewPydantic.from_orm(review)


@router.get("/dish-review/{dish_review_id}", response_model=DishReviewPydantic)
async def get_dish_review(dish_review_id: UUID, token=Depends(validate_token)):
    review = dish_review_manager.get(dish_review_id)
    return DishReviewPydantic.from_orm(review)


@router.delete("/dish-review/{dish_review_id}", response_model=DishReviewPydantic)
async def delete_dish_review(dish_review_id: UUID, token=Depends(validate_token)):
    deleted_count = dish_review_manager.delete(dish_review_id)
    return {"deleted_count": deleted_count}


@router.get(
    "/dish-review/dish/{dish_id}/buyer/{buyer_id}",
    response_model=Optional[DishReviewPydantic],
)
async def get_dish_review_by_dish_id_and_buyer_id(
    dish_id: UUID, buyer_id: UUID, token=Depends(validate_token)
):
    review = dish_review_manager.get_dish_review_by_dish_id_and_buyer_id(
        dish_id, buyer_id
    )
    return (
        DishReviewPydantic.from_orm(review)
        if review
        else Response(status_code=status.HTTP_204_NO_CONTENT)
    )


@router.get(
    "/dish-review/dish/{dish_id}", response_model=Optional[List[DishReviewPydantic]]
)
async def get_dish_review_by_dish_id(dish_id: UUID):
    reviews = dish_review_manager.get_by_dish_id(dish_id)
    return [DishReviewPydantic.from_orm(review) for review in reviews]


@router.get("/dish-review/rating/{dish_id}")
async def get_dish_review_rating(dish_id: UUID):
    rating = dish_review_manager.get_dish_review_rating_summary(dish_id)
    return {"rating": rating}
