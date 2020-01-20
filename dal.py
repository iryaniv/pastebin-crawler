from tinydb import TinyDB, Query
from models.paste import Paste


class PasteDB:
    def __init__(self, json_path):
        self.__db = TinyDB(json_path)

    def add(self, paste_dict):
        self.__db.insert(paste_dict)

    def query(self, paste_id):
        paste_query = Query()
        found_pastes = self.__db.search(paste_query.id == paste_id)
        if found_pastes:
            found_paste = found_pastes[0]
            return Paste(found_paste['id'], found_paste['name'], found_paste['user'], found_paste['date'],
                         found_paste['content'])
        return None

    def does_exist(self, paste_id):
        paste_query = Query()
        found_pastes = self.__db.search(paste_query.id == paste_id)
        return len(found_pastes) >= 1


class DBOrchestrator:
    def __init__(self, db):
        self.__db = db

    def add_paste(self, paste):
        self.__db.add(paste.__dict__)

    def get_paste(self, paste_id):
        return self.__db.query(paste_id)

    def does_exist(self, paste_id):
        return self.__db.does_exist(paste_id)
