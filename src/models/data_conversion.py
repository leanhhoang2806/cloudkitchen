from src.models.postgres_model import Order, Dish
from src.models.data_model import (
    OrderInformationForExternal,
    DishInformationForExternal,
)


def map_to_order_external(
    order_from_db: Order, shipping_address: str = None
) -> OrderInformationForExternal:
    return OrderInformationForExternal(
        id=order_from_db.id,
        dish_id=order_from_db.dish_id,
        status=order_from_db.status,
        created_at=order_from_db.created_at,
        updated_at=order_from_db.updated_at,
        address=shipping_address,
    )


def map_to_dish_external(
    dish_from_db: Dish, seller_name: str = None
) -> DishInformationForExternal:
    return DishInformationForExternal(
        id=dish_from_db.id,
        name=dish_from_db.name,
        seller_name=seller_name,
        description=dish_from_db.description,
        price=dish_from_db.price,
        s3_path=dish_from_db.s3_path,
        quantities=dish_from_db.quantities,
        is_featured=dish_from_db.is_featured,
        status=dish_from_db.status,
        created_at=dish_from_db.created_at,
        updated_at=dish_from_db.updated_at,
    )
