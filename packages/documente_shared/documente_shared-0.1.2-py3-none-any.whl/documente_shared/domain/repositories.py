from abc import ABC, abstractmethod

from documente_shared.domain.entities import DocumentProcess


class DocumentProcessRepository(ABC):

    @abstractmethod
    def persist(self, instance: DocumentProcess) -> DocumentProcess:
        raise NotImplementedError

    @abstractmethod
    def delete(self, instance: DocumentProcess):
        raise NotImplementedError