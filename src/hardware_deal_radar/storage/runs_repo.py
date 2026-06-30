from __future__ import annotations

import json

from hardware_deal_radar.models import RunSummary
from hardware_deal_radar.storage.models import ErrorLogRecord, RunRecord
from hardware_deal_radar.utils.time import utcnow


class RunsRepository:
    def __init__(self, session) -> None:
        self.session = session

    def create_run(self, mode: str) -> RunRecord:
        record = RunRecord(started_at=utcnow(), status="running", mode=mode)
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def finish_run(
        self, record: RunRecord, summary: RunSummary, status: str = "success"
    ) -> RunRecord:
        record.finished_at = utcnow()
        record.status = status
        record.searches_count = summary.searches_count
        record.marketplaces_count = summary.marketplaces_count
        record.raw_results_count = summary.raw_results_count
        record.new_listings_count = summary.new_listings_count
        record.updated_listings_count = summary.updated_listings_count
        record.strong_alerts_count = summary.strong_alerts_count
        record.digest_candidates_count = summary.digest_candidates_count
        record.errors_count = summary.errors_count
        record.summary_json = json.dumps(summary.model_dump(mode="json"), default=str)
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def log_error(
        self,
        run_id: int | None,
        error_type: str,
        message: str,
        source: str | None = None,
        marketplace: str | None = None,
    ) -> None:
        record = ErrorLogRecord(
            run_id=run_id,
            source=source,
            marketplace=marketplace,
            error_type=error_type,
            message=message,
            created_at=utcnow(),
        )
        self.session.add(record)
        self.session.commit()
