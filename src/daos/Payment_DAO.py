from src.models.postgres_model import Payment
from src.daos.BaseDAO import GenericDAO


class PaymentDAO(GenericDAO):
    def __init__(self) -> None:
        super().__init__(Payment)
