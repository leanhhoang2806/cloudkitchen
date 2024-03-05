from src.managers.dish_manager import DishManager
from typing import Optional, List
from src.models.postgres_model import Dish
from src.errors.custom_exceptions import BothSearchTermEmpty
from src.media.long_lat.longitude_lattitude_reader import ZipcodeSearchReader


class SearchManager:
    def __init__(self, dish_manager: DishManager) -> None:
        self.dish_manager = dish_manager
        self.zipcode_manager = ZipcodeSearchReader()

    def search_by_name_and_zip(
        self, name: Optional[str], zipcode: Optional[str]
    ) -> Optional[List[Dish]]:
        if not name and not zipcode:
            raise BothSearchTermEmpty
        if name and not zipcode:
            return self.dish_manager.search_by_name(name)
        if not name and zipcode:
            zipcodes = self.zipcode_manager.find_neighbors(int(zipcode))
            return self.dish_manager.search_by_seller_zipcodes(zipcodes)
        return self.dish_manager.search_by_seller_zipcodes(name, zipcode)
