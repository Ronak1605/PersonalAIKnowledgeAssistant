from abc import ABC, abstractmethod
from typing import List
from ingestion.models.input import Input


class BaseLoader(ABC):
    """
    Abstract base class for all ingestion loaders.
    """

    @abstractmethod
    def load(self, source: str) -> List[Input]:
        """
        Load raw input from `source` and return normalized Input objects.
        """
        raise NotImplementedError
