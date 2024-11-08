from agenteasy.termbase import MongoStorage, TermData
from agenteasy.config import settings


def test_find_terms():
    print(settings.MONGO_URL, settings.MONGO_DB_NAME, settings.MONGO_COLLECTION_NAME)
    ms = MongoStorage(
        settings.MONGO_URL, settings.MONGO_DB_NAME, settings.MONGO_COLLECTION_NAME
    )
    td = TermData(ms, "VI")
    print(td.data)
    result = td.find_terms("琼液仙壶和本源")
    print(result)
    assert isinstance(result, dict)
    assert len(result) == 2
