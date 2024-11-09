from sqlalchemy import Column, DateTime, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

# import string
from sqlalchemy import String
from . import Base


class LastRunTime(Base):
    __tablename__ = "last_run_times"

    id = Column(Integer, primary_key=True)
    credential_id = Column(Integer, ForeignKey("credentials.id"), nullable=False)
    job_name = Column(String(50), nullable=False)
    last_run = Column(DateTime, nullable=False)

    # add unique contrainst for name and credential_id
    __table_args__ = (
        UniqueConstraint("credential_id", "job_name", name="credential_job_unique_key"),
    )

    # Function to update or create the last run time for a job
    @staticmethod
    def upsert_last_run_time(db, credential_id, job_name, run_time) -> None:
        last_run: LastRunTime | None = (
            db.query(LastRunTime)
            .filter_by(credential_id=credential_id, job_name=job_name)
            .first()
        )
        if last_run:
            last_run.last_run = run_time
        else:
            last_run = LastRunTime(
                credential_id=credential_id, job_name=job_name, last_run=run_time
            )
            db.add(last_run)
        db.commit()

    # Function to get the last run time for a job
    @staticmethod
    def get_last_run_time(db, credential_id, job_name) -> Optional[datetime]:
        last_run: Optional[LastRunTime] = (
            db.query(LastRunTime)
            .filter_by(credential_id=credential_id, job_name=job_name)
            .first()
        )
        return last_run.last_run if last_run else None
