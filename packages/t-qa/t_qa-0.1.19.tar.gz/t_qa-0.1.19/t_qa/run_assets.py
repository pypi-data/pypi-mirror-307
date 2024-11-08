"""Assets module."""
from datetime import datetime, timedelta
from time import sleep
from typing import Optional

import pytz
import t_bug_catcher
from coverage import Coverage
from coverage.exceptions import NoSource
from retry import retry

from t_qa.config import COVERAGE, Inputs
from t_qa.goole_api.google_drive_service import GoogleDriveService
from t_qa.models import RunData, TestCase
from t_qa.workitems import METADATA, RUN_NUMBER, VARIABLES

from .logger import logger


class RunAssets:
    """Assets class."""

    def __init__(self, google_drive_service: GoogleDriveService):
        """Initialize the Assets object."""
        self._google_drive_service = google_drive_service
        self._file = {}
        self._assets = {}
        self._asset_run_data = {}

    def __enter__(self):
        """Enter the context manager."""
        self.get_assets()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit the context manager."""
        self._google_drive_service.unlock_file(self._file)
        self.upload_assets()

    def get_assets(self):
        """Get the assets from the Google Drive."""
        self._file = self._google_drive_service.create_file_if_not_exists(
            folder=self._google_drive_service.get_root_folder("T-QA Assets"),
            file_name=Inputs.ADMIN_CODE,
            mime_type="application/json",
        )
        self._assets = self.get_file_content()
        self._delete_old_run_data()
        self._asset_run_data = self._assets.get(RUN_NUMBER, {})
        return self._assets

    @retry(tries=3, exceptions=ValueError)
    def get_file_content(self):
        """Get the file content."""
        for _ in range(12):
            if self._google_drive_service.check_file_locked(self._file):
                logger.info("File is locked. Waiting for 5 seconds")
                sleep(5)
            else:
                return self._google_drive_service.get_file_content(file=self._file)
        else:
            logger.error("File is locked for more than 1 minute. Unlocking the file and retrying...")
            self._google_drive_service.unlock_file(self._file)
            raise ValueError("File is locked")

    def upload_assets(self) -> None:
        """Upload the assets to the Google Drive."""
        self._assets[RUN_NUMBER] = self._asset_run_data
        self._google_drive_service.update_json_file(file=self._file, data=self._assets)

    def update_run_data(self, run_data: RunData) -> RunData:
        """Update the run data."""
        run_data.test_cases = self._update_test_cases(run_data.test_cases)
        run_data.run_date = self._update_run_date(run_data.run_date)
        run_data.record_status_counters = self._update_record_status_counters(run_data.record_status_counters)
        run_data.bugs = self._update_bug_counter()
        run_data.code_coverage = self._update_code_coverage_percentage()
        run_data.duration = self._get_duration(run_data.run_date)
        run_data.run_link = self._update_run_link()
        run_data.empower_env = self._update_empower_env()
        return run_data

    def _update_empower_env(self) -> str:
        """Update the empower environment."""
        self._asset_run_data["empower_env"] = "Prod" if VARIABLES.get("environment", "") == "production" else "Dev"
        return self._asset_run_data["empower_env"]

    def _update_run_link(self) -> str:
        """Update the run link."""
        self._asset_run_data["run_link"] = f'=HYPERLINK("{METADATA.get("processRunUrl", "")}", "{RUN_NUMBER}")'
        return self._asset_run_data["run_link"]

    def _get_duration(self, run_date) -> str:
        duration = datetime.now(pytz.UTC) - run_date.astimezone(pytz.UTC)
        seconds = duration.seconds
        minutes = seconds // 60
        hours = minutes // 60
        duration_str = f"{hours}h {minutes % 60}m {seconds % 60}s"
        return duration_str

    def _update_test_cases(self, test_cases: list[TestCase]) -> list[TestCase]:
        """Update the test cases."""
        if self._asset_run_data.get("test_cases", False):
            for index, test_case in enumerate(test_cases):
                if test_case.status != "":
                    self._asset_run_data["test_cases"][index]["status"] = test_case.status
        else:
            self._asset_run_data["test_cases"] = [test_case.__dict__ for test_case in test_cases]

        return [TestCase(**test_case) for test_case in self._asset_run_data["test_cases"]]

    def _update_bug_counter(self, bug_counter: int = t_bug_catcher.get_errors_count()) -> str:
        """Update the bug counter."""
        if self._asset_run_data.get("bug_counter", False):
            self._asset_run_data["bug_counter"] += bug_counter
        else:
            self._asset_run_data["bug_counter"] = bug_counter
        return str(self._asset_run_data["bug_counter"])

    def _delete_old_run_data(self) -> None:
        """Delete old assets."""
        for key, value in self._assets.items():
            if value.get("run_date", None):
                run_date = datetime.strptime(value["run_date"], "%Y-%m-%d %H:%M:%S")
                if run_date < datetime.now() - timedelta(days=3):
                    del self._assets[key]

    def _update_record_status_counters(self, record_status_counters: dict[str, int]) -> dict[str, int]:
        """Update the record status counters."""
        if self._asset_run_data.get("record_status_counters", False):
            for key, value in record_status_counters.items():
                if key in self._asset_run_data["record_status_counters"]:
                    self._asset_run_data["record_status_counters"][key] += value
                else:
                    self._asset_run_data["record_status_counters"][key] = value
        else:
            self._asset_run_data["record_status_counters"] = record_status_counters
        return self._asset_run_data["record_status_counters"]

    def _update_run_date(self, run_date: datetime) -> datetime:
        """Update the start datetime."""
        if self._asset_run_data.get("start_datetime", False):
            asset_datetime = datetime.strptime(self._asset_run_data["start_datetime"], "%Y-%m-%d %H:%M:%S")
            if run_date < asset_datetime:
                self._asset_run_data["start_datetime"] = run_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            self._asset_run_data["start_datetime"] = run_date.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(self._asset_run_data["start_datetime"], "%Y-%m-%d %H:%M:%S")

    def _update_code_coverage_percentage(self, coverage: Coverage = COVERAGE) -> str:
        """Update the code coverage."""
        if self._asset_run_data.get("code_coverage", None):
            total_lines = self._asset_run_data["code_coverage"].get("total_lines", 0)
            covered_lines = self._asset_run_data["code_coverage"].get("covered_lines", 0)
        else:
            self._asset_run_data["code_coverage"] = {}
            total_lines = 0
            covered_lines = 0

        for file in coverage.get_data().measured_files():
            try:
                analysis = coverage._analyze(file)
            except NoSource:
                continue
            total_lines += len(analysis.statements)
            covered_lines += len(analysis.executed)

        self._asset_run_data["code_coverage"]["total_lines"] = total_lines
        self._asset_run_data["code_coverage"]["covered_lines"] = covered_lines
        percentage = (covered_lines / total_lines) * 100 if total_lines > 0 else 0
        return f"{percentage :.0f}%"

    def get_row_number(self) -> Optional[int]:
        """Get the row number."""
        if self._asset_run_data.get("row_number", False):
            return self._asset_run_data["row_number"]
        else:
            return None

    def set_row_number(self, row_number) -> None:
        """Set the row number."""
        self._asset_run_data["row_number"] = row_number
