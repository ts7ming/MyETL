import time


class BaseRepo:
    def __init__(self, session):
        self.session = session

    @staticmethod
    def generate_id():
        return time.time_ns()

    def __filter(self, entity, entity_filter=None):
        if entity_filter is None:
            entity_list = self.session.query(entity).all()
        else:
            entity_list = self.session.query(entity).filter(entity_filter).all()
        return entity_list

    def get_entity_list(self, entity, entity_filter=None, entity_id_list=None):
        if entity_filter is not None:
            entity_list = self.__filter(entity_filter)
        elif entity_id_list is not None:
            entity_list_str = [str(x) for x in entity_id_list]
            entity_filter = entity.id.in_(entity_list_str)
            entity_list = self.__filter(entity_filter)
        else:
            entity_list = self.__filter(entity)
        return entity_list

    def entity_update(self, entity, entity_filter=None, entity_id=None, update_info=None):
        if entity_filter is not None:
            pass
        elif entity_id is not None:
            entity_filter = entity.id == entity_id
        else:
            raise Exception('缺少更新范围')
        self.session.query(entity).filter(entity_filter).update(update_info, synchronize_session=False)
        self.session.commit()
