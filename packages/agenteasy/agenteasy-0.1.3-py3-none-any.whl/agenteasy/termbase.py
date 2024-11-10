import re
from pydantic import BaseModel, HttpUrl
from pymongo.mongo_client import MongoClient
import pandas as pd

class MongoConfig(BaseModel):
    url: HttpUrl | None = None
    db_name: str | None = None
    collection_name: str | None = None


def setup_termbase(config: MongoConfig, locale: str):
    termbase = TermData(
        MongoStorage(
            **config.model_dump(exclude_none=True)
            # os.getenv("mongo_url"), os.getenv("db_name"), os.getenv("collection_name")
        ),
        locale,
    )
    return termbase


class MongoStorage:
    def __init__(self, connect_url, db_name, collection_name) -> None:
        self.client = self.create_connection(connect_url)
        self.db_name = db_name
        self.collection_name = collection_name

    def __del__(self):
        if self.client:
            self.client.close()

    def create_connection(self, connect_url: str):
        client = MongoClient(connect_url)
        try:
            client.admin.command("ping")
            print("Connected")
        except Exception as e:
            raise ConnectionError(e)
        return client

    @property
    def collection(self):
        if self.db_name is None:
            return
        if self.client is None:
            return
        if self.collection_name is None:
            return
        return self.client[self.db_name].get_collection(self.collection_name)

    def upload_many(self, docs: list):
        if self.collection is not None:
            result = self.collection.insert_many(docs)
            return result


class TermData:
    def __init__(
        self,
        mongo_store: MongoStorage | None = None,
        locales: str | None = None,
        term_min_length: int = 2,
        term_max_length: int = 6,
    ) -> None:
        self.mongo = mongo_store
        self._locale = None
        self.data: dict[str, list] | None = None
        self.term_min_length: int = term_min_length
        self.term_max_length: int = term_max_length
        self.locale = locales

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, value):
        if value:
            self._locale = value
            self.data = self.get_data(self._locale)

    def get_data(self, locales: str):
        if (self.mongo is None) or (self.mongo.collection is None):
            return
        data = self.mongo.collection.find({"locales": locales})
        result = {i["source"]: i["targets"] for i in data}
        sorted_keys = list(result.keys())
        sorted_keys.sort(key=lambda x: len(x), reverse=True)
        sorted_dict = {k: result[k] for k in sorted_keys}
        return sorted_dict

    def find_terms(self, text: str):
        if self.data is None:
            return {}
        result = {}
        _text = text
        for k, v in self.data.items():
            if k in _text:
                result[k] = v
                _text.replace(k, "+")
        if len(result) > 0:
            return result
        return "None"

    def update_terms(self, new_terms):
        _content = {}
        for k, v in new_terms.items():
            if k in self.data:
                continue
            if len(k) > self.term_max_length or len(k) < self.term_min_length:
                continue
            if re.search("\\d|[A-Za-z]", k):
                continue
            _content[k] = v
        self.data.update(_content)
        if len(_content) > 0:
            _docs = [
                {"locales": self.locale, "source": k, "targets": v, "confirmed": False}
                for k, v in _content.items()
            ]
            if self.mongo is not None:
                result = self.mongo.upload_many(_docs)
            return result

    def load_from_dataframe(self, df: pd.DataFrame):
        if self.data is None:
            self.data = {}
        for i, row in df.iterrows():
            val = row.iat[0]
            if val in self.data:
                self.data[val].append(row.iat[1])
            else:
                self.data[val] = [row.iat[1]]
