from src.daos.database_session import session


class GenericDAO:
    def __init__(self, model):
        self.model = model

    def create(self, data):
        try:
            instance = self.model(**data.dict())
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
