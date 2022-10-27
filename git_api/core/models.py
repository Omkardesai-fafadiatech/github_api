from django.conf import settings


class MongoDBModel:
    def encode_object_id_to_string(self, info):
        info["_id"] = str(info["_id"])
        return info

    def add(self, info):
        self.collection.insert_one(info)

    def find(self, filter_criteria):
        return list(self.collection.find(filter_criteria))

    def list_all(self):
        return map(self.encode_object_id_to_string, list(self.collection.find()))

    def count(self):
        return self.collection.count_documents({})

    def drop(self):
        self.collection.drop()


class GitIssues(MongoDBModel):
    def __init__(self):
        self.collection = settings.DB["issues"]


class GitPullRequests(MongoDBModel):
    def __init__(self):
        self.collection = settings.DB["pr"]

