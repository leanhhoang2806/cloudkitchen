from src.daos.Payment_DAO import PaymentDAO
from src.managers.generic_manager import GenericManager


class PaymentManager(GenericManager):
    def __init__(self) -> None:
        super().__init__(PaymentDAO())
