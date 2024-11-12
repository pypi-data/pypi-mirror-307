from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from documente_shared.domain.enums import DocumentProcessStatus


@dataclass
class DocumentProcess(object):
    digest: str
    status: DocumentProcessStatus
    file_path: str
    processed_csv_path: str
    processed_xlsx_path: str
    processing_time: Optional[float] = None
    enqueued_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    @property
    def is_pending(self) -> bool:
        return self.status == DocumentProcessStatus.PENDING

    @property
    def is_enqueued(self) -> bool:
        return self.status == DocumentProcessStatus.ENQUEUED

    @property
    def is_processing(self) -> bool:
        return self.status == DocumentProcessStatus.PROCESSING

    @property
    def is_completed(self) -> bool:
        return self.status == DocumentProcessStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        return self.status == DocumentProcessStatus.FAILED

    @property
    def is_valid(self) -> bool:
        return all([
            self.digest,
            self.status,
            self.file_path,
        ])

    def enqueue(self):
        self.status = DocumentProcessStatus.ENQUEUED
        self.enqueued_at = datetime.now()

    def processing(self):
        self.status = DocumentProcessStatus.PROCESSING
        self.started_at = datetime.now()

    def failed(self):
        self.status = DocumentProcessStatus.FAILED
        self.failed_at = datetime.now()

    def completed(self):
        self.status = DocumentProcessStatus.COMPLETED
        self.processed_at = datetime.now()



    @property
    def to_dict(self) -> dict:
        return {
            'digest': self.digest,
            'status': self.status.value,
            'file_path': self.file_path,
            'processed_csv_path': self.processed_csv_path,
            'processed_xlsx_path': self.processed_xlsx_path,
            'processing_time': self.processing_time,
            'enqueued_at': self.enqueued_at.isoformat() if self.enqueued_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'failed_at': self.failed_at.isoformat() if self.failed_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DocumentProcess':
        return cls(
            digest=data.get('digest'),
            status=DocumentProcessStatus.from_value(data.get('status')),
            file_path=data.get('file_path'),
            processed_csv_path=data.get('processed_csv_path'),
            processed_xlsx_path=data.get('processed_xlsx_path'),
            processing_time=(
                data.get('processing_time')
                if data.get('processing_time') else None
            ),
            enqueued_at=(
                datetime.fromisoformat(data.get('enqueued_at'))
                if data.get('enqueued_at') else None
            ),
            started_at=(
                datetime.fromisoformat(data.get('started_at'))
                if data.get('started_at') else None
            ),
            failed_at=(
                datetime.fromisoformat(data.get('failed_at'))
                if data.get('failed_at') else None
            ),
            processed_at=(
                datetime.fromisoformat(data.get('processed_at'))
                if data.get('processed_at') else None
            ),
        )