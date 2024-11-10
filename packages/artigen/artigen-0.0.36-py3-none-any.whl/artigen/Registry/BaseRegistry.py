from abc import ABC, abstractmethod


class BaseRegistry(ABC):

    @abstractmethod
    async def create_new_darn(self, **kwargs):
        pass

    @abstractmethod
    async def update_darn(self, **kwargs):
        pass

    @abstractmethod
    async def list_darn(self, **kwargs):
        pass

    @abstractmethod
    async def delete_darn(self, **kwargs):
        pass
