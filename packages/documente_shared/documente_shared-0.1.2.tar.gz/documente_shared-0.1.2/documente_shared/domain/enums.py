from documente_shared.domain.base_enum import BaseEnum


class DocumentProcessStatus(BaseEnum):
    PENDING = 'PENDING'
    ENQUEUED = 'ENQUEUED'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

