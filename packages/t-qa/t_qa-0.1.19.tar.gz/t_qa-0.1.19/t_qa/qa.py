"""QA.py module contains the QA class for the Digital Worker's process."""
import atexit
import os
import re
import traceback
from datetime import datetime
from typing import Optional

import t_bug_catcher
import yaml
from thoughtful.supervisor import report_builder

from .config import COVERAGE, DEFAULT_QA_RESULT_FILE_PATH, DEFAULT_TEST_CASES_FILE_PATH, LOCAL_RUN, SCOPES
from .excel_processing.google_sheet import GoogleSheet
from .excel_processing.report import _Report
from .exception import (
    ServiceAccountKeyPathException,
    SkipIfItLocalRunException,
    SkipIfItWorkItemsNotSetException,
    TestCaseFileDoesNotExistException,
    TestCaseReadException,
    TQaBaseException,
    TQaBaseSilentException,
)
from .goole_api.account import Account
from .goole_api.google_drive_service import GoogleDriveService
from .logger import logger
from .models import RunData, TestCase
from .run_assets import RunAssets
from .status import Status
from .utils import SingletonMeta, install_sys_hook, print_coverage_report
from .workitems import METADATA, VARIABLES


class QA(metaclass=SingletonMeta):
    """QA class for the Digital Worker's process."""

    def __init__(self) -> None:
        """Initialize the QA process."""
        self.run_data = RunData(
            status=Status.SUCCESS.value,
        )
        self.service_account_key_path: str = None
        self.google_drive_service: Optional[GoogleDriveService] = None
        self.google_sheet_service: Optional[GoogleSheet] = None

    def configurate(
        self,
        service_account_key_path: str,
        test_cases_file_path: str = DEFAULT_TEST_CASES_FILE_PATH,
    ) -> None:
        """Configurate the QA process."""
        try:
            if not LOCAL_RUN:
                COVERAGE.start()
            self._set_test_cases(test_cases_file_path)
            self._set_service_account_key_path(service_account_key_path)
            self._skip_if_it_local_run()
        except TQaBaseSilentException:
            return
        except TQaBaseException as e:
            logger.warning(e)
            return
        self._set_run_date()
        atexit.register(self.dump)

    def test_case_pass(self, id: str) -> None:
        """Check the test case passed."""
        self._set_test_case_status(id=id, status=Status.PASS.value)

    def test_case_fail(self, id: str) -> None:
        """Check the test case failed."""
        self._set_test_case_status(id=id, status=Status.FAIL.value)

    def dump(self):
        """Dump the test cases."""
        try:
            print_coverage_report()
            self._set_google_services()

            self.run_data.status = self._get_run_status()

            with RunAssets(self.google_drive_service) as run_assets:
                self.run_data = run_assets.update_run_data(self.run_data)
                report = _Report(
                    local_excel_file_path=DEFAULT_QA_RESULT_FILE_PATH,
                    google_sheet=self.google_sheet_service,
                    google_drive=self.google_drive_service,
                )
                row_number = report.dump(
                    run_data=self.run_data,
                    row_number=run_assets.get_row_number(),
                )
                run_assets.set_row_number(row_number)

        except TQaBaseException as e:
            logger.warning(e)
        except Exception as e:
            logger.error(f"Error during dumping: {e}")
            traceback.print_exc()

    def _set_google_services(self):
        """Set the Google services."""
        account = Account(
            service_account_key_path=self.service_account_key_path,
            scopes=SCOPES,
        )
        self.google_drive_service = GoogleDriveService(account)
        self.google_sheet_service = GoogleSheet(account)

    def set_test_records_status_count(self, record_status_counters: dict[str, int]):
        """Set the test records status count."""
        if not isinstance(record_status_counters, dict):
            logger.error("The record status count should be a dictionary.")
            record_status_counters = {}
        if not all(isinstance(key, str) for key in record_status_counters.keys()):
            logger.error("The record_status_count KEYS should contain only strings.")
            record_status_counters = {}
        if not all(isinstance(value, int) for value in record_status_counters.values()):
            logger.error("The record_status_count VALUES should contain only integers.")
            record_status_counters = {}
        if len(record_status_counters.keys()) >= 15:
            logger.error("The record status count is too large. It should be less than 15 statuses.")
            record_status_counters = {}
        self.run_data.record_status_counters = record_status_counters

    def _get_run_status(self):
        if self.run_data.status == Status.SUCCESS.value:
            try:
                self.run_data.status = report_builder.status.value
            except AttributeError:
                logger.warning("Could not get the run result from supervisor.")
        return self.run_data.status

    def _set_test_cases(self, test_cases_file_path: str) -> None:
        if not os.path.exists(test_cases_file_path):
            raise TestCaseFileDoesNotExistException(f"Test cases file not found: {test_cases_file_path}")
        try:
            with open(test_cases_file_path) as test_cases_file:
                test_cases = yaml.safe_load(test_cases_file)["test_cases"]
                self.run_data.test_cases = [TestCase(**test_case) for test_case in test_cases]
        except (TypeError, KeyError, ValueError) as e:
            raise TestCaseReadException(f"Error during reading test cases: {e}")

    def _set_service_account_key_path(self, service_account_key_path: str) -> None:
        if service_account_key_path:
            self.service_account_key_path = service_account_key_path
        else:
            raise ServiceAccountKeyPathException("There are no access to 'T-QA Google' collection")

    def _skip_if_it_local_run(self):
        if LOCAL_RUN:
            raise SkipIfItLocalRunException()
        if not METADATA:
            raise SkipIfItWorkItemsNotSetException("'Metadata' is not set")
        if not VARIABLES:
            raise SkipIfItWorkItemsNotSetException("'Variables' is not set")

    def _set_run_date(self) -> None:
        """Get the start datetime."""
        try:
            root_path = os.environ.get("ROBOT_ROOT", "")
            console_log_folder_path = os.path.abspath(os.path.join(root_path, os.pardir))
            console_log_file_path = os.path.join(console_log_folder_path, "console.txt")
            with open(console_log_file_path, "r") as file:
                data = file.read()
            date_str = re.findall(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", data)[0]
            date_str += "UTC"
            self.run_data.run_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%Z")
        except (TypeError, FileNotFoundError, IndexError) as e:
            logger.warning("Could not get the start datetime from the empower.")
            self.run_data.run_date = datetime.now()
            t_bug_catcher.report_error(exception=e)

    def _set_test_case_status(self, id: str, status: str) -> None:
        """Check the test case."""
        if not isinstance(id, str):
            logger.error("The test case id should be a string.")
            return None
        for test_case in self.run_data.test_cases:
            if test_case.id == id:
                test_case.status = status
                return None
        else:
            logger.error(f"The test case with id '{id}' not found.")


t_qa = QA()
install_sys_hook(t_qa)

configure_qa = t_qa.configurate
test_case_failed = t_qa.test_case_fail
test_case_passed = t_qa.test_case_pass
set_test_records_status_count = t_qa.set_test_records_status_count
