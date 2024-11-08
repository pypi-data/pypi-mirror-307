"""Configuration file for the QA library."""
import os

from coverage import Coverage

from t_qa.workitems import METADATA, VARIABLES


def configure_coverage():
    """Get the coverage object."""
    if Coverage.current():
        __coverage = Coverage.current()
    elif Coverage().config.config_file:
        __coverage = Coverage()
    else:
        __coverage = Coverage(branch=True, omit=["config-3.py"])
        __coverage.exclude(r"    def __repr__")
        __coverage.exclude(r"raise AssertionError")
        __coverage.exclude(r"raise NotImplementedError")
        __coverage.exclude(r"if 0:")
        __coverage.exclude(r"if __name__ == .__main__.:")
        __coverage.exclude(r"if TYPE_CHECKING:")
        __coverage.exclude(r"class .*\bProtocol\):")
        __coverage.exclude(r"@(abc\.)?abstractmethod")
    return __coverage


DEFAULT_WORK_ITEM_FIELD = [
    "userEmail",
    "changeStatusUrl",
    "environment",
    "supervisorCallbackUrl",
    "jwtProcessUpdatesWebhook",
    "refreshTokenUrl",
    "processRunUrl",
    "accessToken",
    "refreshToken",
]
ROOT_PATH = os.getcwd()
OUTPUT_PATH = os.path.join(ROOT_PATH, "output")
TEMP_PATH = os.path.join(ROOT_PATH, "temp")
if os.path.exists(OUTPUT_PATH):
    DEFAULT_QA_RESULT_FILE_PATH = os.path.join(OUTPUT_PATH, "qa_result.xlsx")
else:
    DEFAULT_QA_RESULT_FILE_PATH = os.path.join(ROOT_PATH, "qa_result.xlsx")
DEFAULT_TEST_CASES_FILE_PATH = os.path.join(ROOT_PATH, "test_cases.yaml")
LOCAL_RUN = os.environ.get("RC_PROCESS_RUN_ID") is None
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]

COVERAGE = configure_coverage()


class Inputs:
    """Inputs class."""

    ADMIN_CODE: str = METADATA.get("process", dict()).get("adminCode", "")
    ENVIRONMENT: str = VARIABLES.get("environment", "")
