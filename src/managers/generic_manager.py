class GenericManager:
    def __init__(self, dao):
        self.dao = dao

    def create(self, data):
        return self.dao.create(data)

    def get(self, instance_id):
        return self.dao.get(instance_id)

    def update(self, instance_id, data):
        return self.dao.update(instance_id, data)

    def delete(self, instance_id):
        return self.dao.delete(instance_id)
