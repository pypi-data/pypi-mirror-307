from datetime import datetime
from typing import List

from pydantic import BaseModel


class DatasetVersion(BaseModel):
    semanticBindingName: str
    createdAt: datetime


class PublicDatasetVersions(BaseModel):
    data: List[DatasetVersion]

