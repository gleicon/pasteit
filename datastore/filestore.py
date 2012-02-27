import os

class FileStore():
    def __init__(self, parsed_uri, hash_method=None):
        self._hash_method = hash_method if hash_method else self._hash_by_name
        self._parsed_uri = parsed_uri
        self._root = self._parsed_uri.path if self._parsed_uri.path else '/tmp/ds'

    def _hash_by_name(self, name):
        return "%s/%c/%c/%s"% (self._root, name[0], name[1], name)

    def load(self, name):
        full_path_file = self._hash_method(name)
        try:
            f = open(full_path_file, 'rb')
            r = f.read()
            f.close()
            return r
        except:
            return None

    def save(self, name, content):
        full_path_file = self._hash_method(name)
        bdir = os.path.dirname(full_path_file)
        try:
            if not os.path.exists(bdir):
                os.makedirs(bdir)
            f = open(full_path_file, 'wb')
            f.write(content)
            f.close()
        except Exception, e:
            print "Exception: ", e
            return False
        return True

    def exists(self, name):
        full_path_file = self._hash_method(name)
        return os.path.exists(full_path_file)
    
    def remove(self, name):
        full_path_file = self._hash_method(name)
        bdir = os.path.dirname(full_path_file)
        if os.path.exists(full_path_file): 
            os.unlink(full_path_file)
            try:
                os.rmdir(bdir)
            except:
                pass
        else:
            return False
        return True

