# -*- encoding: utf-8 -*-
import pymongo

from pyzrpc.meta import SubjectMeta, CONFIG_MONGO_CONFIG_KEY, CONFIG_MONGO_MONGO_DBNAME_KEY


class Client(SubjectMeta):
    _table_name = None
    _config = None

    @property
    def table_name(self):
        return self._table_name

    @table_name.setter
    def table_name(self, value):
        self._table_name = value

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def get_collection(self):
        client = pymongo.MongoClient(self.config, connect=False)
        return client[CONFIG_MONGO_MONGO_DBNAME_KEY][self.table_name]

    def update(self, config):
        self._config = config.get(CONFIG_MONGO_CONFIG_KEY)

    def get_list(self, query: dict, field: dict, limit: int, skip_no: int,
                 sort_field: str = 'update_time', sort: int = -1):
        collection = self.get_collection()
        data = collection.find(query, field).sort(sort_field, sort).limit(limit).skip(skip_no)
        data = [i for i in data]
        count = collection.count_documents(query)
        return count, data

    def update_many(self, query: dict, update_data: dict, upsert=False):
        collection = self.get_collection()
        collection.update_many(query, {"$set": update_data}, upsert=upsert)
        return None

    def push_many(self, query: dict, update_data: dict, upsert=False):
        collection = self.get_collection()
        collection.update_many(query, {"$push": update_data}, upsert=upsert)
        return None

    def push_one(self, query: dict, update_data: dict, upsert=False):
        collection = self.get_collection()
        collection.find_one_and_update(query, {"$push": update_data}, upsert=upsert)
        return None

    def pull_one(self, query: dict, update_data: dict):
        collection = self.get_collection()
        collection.find_one_and_update(query, {"$pull": update_data})
        return None

    def insert_data(self, data: dict):
        collection = self.get_collection()
        collection.insert_one(data)
        return None

    def delete_data(self, query: dict):
        collection = self.get_collection()
        collection.delete_many(query)
        return None

    def distinct_field_query(self, field: str, query: dict):
        collection = self.get_collection()
        data = collection.distinct(field, filter=query)
        return data

    def get_all_data(self, query: dict, field: dict):
        collection = self.get_collection()
        data = collection.find(query, field)
        data = [i for i in data]
        return data


class _Services(Client):

    def __init__(self):
        self.table_name = 'SERVICE_LIST'


class _Tasks(Client):

    def __init__(self):
        self.table_name = 'TASK_LIST'
