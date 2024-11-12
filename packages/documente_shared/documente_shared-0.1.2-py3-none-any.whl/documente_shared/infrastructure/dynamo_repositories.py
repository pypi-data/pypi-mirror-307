from documente_shared.domain.entities import DocumentProcess
from documente_shared.domain.repositories import DocumentProcessRepository


class DynamoDocumentProcessRepository(DocumentProcessRepository):
    def persist(self, instance: DocumentProcess) -> DocumentProcess:
        pass

    def delete(self, instance: DocumentProcess):
        pass