from src.daos.database_session import session
from uuid import UUID


class GenericDAO:
    def __init__(self, model):
        self.model = model

    def create(self, data):
        try:
            data_dict = self._convert_uuids_to_strings(data.dict())
            instance = self.model(**data_dict)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def get(self, instance_id):
        try:
            return (
                session.query(self.model).filter(self.model.id == instance_id).first()
            )
        finally:
            session.close()

    def update(self, instance_id, data):
        try:
            instance = (
                session.query(self.model).filter(self.model.id == instance_id).first()
            )
            if instance:
                for key, value in data.dict().items():
                    setattr(instance, key, value)
                session.commit()
                session.refresh(instance)
            return instance
        finally:
            session.close()

    def delete(self, instance_id):
        try:
            deleted_count = (
                session.query(self.model).filter(self.model.id == instance_id).delete()
            )
            session.commit()
            return deleted_count
        finally:
            session.close()

    def _convert_uuids_to_strings(self, data_dict):
        converted_data = {}
        for key, value in data_dict.items():
            if isinstance(value, UUID):
                converted_data[key] = str(value)
            else:
                converted_data[key] = value
        return converted_data
