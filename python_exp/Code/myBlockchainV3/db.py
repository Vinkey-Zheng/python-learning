import pickle


class DB():
    def __init__(self, db_file):
        self._db_file = db_file
        try:
            with open(self._db_file, 'rb') as f:
                self.kv = pickle.load(f)
        except FileNotFoundError:
            self.kv = {}

    def commit(self):
        with open(self._db_file, 'wb') as f:
            pickle.dump(self.kv, f)

    def get(self, key):
        return self.kv[key]

    def put(self, key, value):
        self.kv[key] = value

    def delete(self, key):
        del self.kv[key]

    def reset(self, bucket):
        self.kv = {}