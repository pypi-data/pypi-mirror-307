from .BaseRegistry import BaseRegistry


class Embedding(BaseRegistry):
    def __init__(self, api_key, redis_client):
        self.api_key = api_key
        self.redis_client=redis_client

    async def create_new_darn(self, **kwargs):
        pass

    async def update_darn(self, **kwargs):
        pass

    async def list_darn(self, page=1, page_size=10, query="", _type=""):
        pass

    async def delete_darn(self, **kwargs):
        pass
