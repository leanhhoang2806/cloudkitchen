from src.managers.buyer_manager import BuyerManager
from src.managers.dish_manager import DishManager
from src.managers.payment_manager import PaymentManager
from src.managers.discounted_dish_manager import DiscountedDishManager


class AllManagers:
    def __init__(self) -> None:
        self.buyer_manager = BuyerManager()
        self.dish_manager = DishManager()
        self.payment_manager = PaymentManager()
        self.discounted_dish_manager = DiscountedDishManager()


ALL_MANAGER = AllManagers()
