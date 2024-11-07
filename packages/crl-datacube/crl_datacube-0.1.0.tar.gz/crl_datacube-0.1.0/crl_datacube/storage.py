from arraylake import Client


class BaseStorage:
    def __init__(self):
        pass
    
    def get_storage(self):
        pass
    
    def get_root_group(self):
        pass
    
    def create_dataset(self, shape, group=None, varnames=None):
        pass


class ArrayLakeStorage(BaseStorage):
    def __init__(self, client: Client, repo: str, disk_store: str):
        self.client = client
        self.repo = repo
        self.disk_store = disk_store
        
    def get_storage(self):
        return self.repo.store
    
    @property
    def root_group(self):
        return self.repo.root_group
    
    def create_group(self, group: str):
        self.root_group.create_group(group)
        
    def get_group(self, group: str = None):
        return self.root_group[group]
    
    def delete_group(self, group: str):
        del self.root_group[group]
        
    def create_dataset(self, var, group=None, varnames=None):
        pass

