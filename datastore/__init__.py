from urlparse import urlparse
from filestore import FileStore

class DataStore():
    """Generic datastore, receives a conn uri on init, provides 
    load, save and find methods, might save on fs, git, blobstorage, nosql, etc
    ex:
        ds = DataStore(conn='file:///tmp/ds') -> initialize /tmp/ds folder
        if file:// is used, it hashed and split files on subfolders
        as /tmp/ds/f/i/file, /tmp/ds/a/n/another_file
    by default the conn parameter will help select the proper backend class by
    prepending the scheme like this:
        ds = DataStore(conn='redis://localhost:6379')
        the backend class should be named RedisDataStore.
    For the file backed store, the uri might point to the right folder
    One could also pass an arbitrary backend class:
        ds = DataStore(backend = SQLBackEnd, host="127.0.0.1"...)
    as long as the custom backend is prepared to receive args and kwargs
    To build new backends, create a file within the datastore folder named after
    it (e.g. filestore.py) and inside it the class name should follow the
    capitalize name, FileStore.
    """

    def __init__(self, conn=None, backend=FileStore, *args, **kwargs):
        self._conn = conn
        self._backend = backend
        r = urlparse(self._conn)
        
        if self._conn is not None and self._backend is not None:
            r = urlparse(self._conn)
            c = self._load_class(r.scheme)
            self._backend = c(r)
        else:
            self._backend = backend()
    
    def _load_class(self, scheme):
        mod = "datastore.%sstore" % scheme
        cl = "%sStore" % scheme.capitalize()
        return getattr(__import__(mod, globals(), locals(), [cl], -1), cl) 

    def load(self, name):
        return self._backend.load(name)

    def save(self, name, content):
        return self._backend.save(name, content)

    def exists(self, name):
        return self._backend.exists(name)

    def remove(self, name):
        return self._backend.remove(name)
