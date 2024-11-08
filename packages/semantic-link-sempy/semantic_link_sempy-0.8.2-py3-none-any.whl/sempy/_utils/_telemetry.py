import os

from .. import _version

try:
    from synapse.ml.fabric.telemetry_utils import report_usage_telemetry
    REPORT_USAGE_TELEMETRY_ENV = "REPORT_USAGE_TELEMETRY"  # Environment variable to control telemetry reporting
except ImportError:
    report_usage_telemetry = None


def log_telemetry(activity_name: str = ""):
    if report_usage_telemetry and \
            os.environ.get(REPORT_USAGE_TELEMETRY_ENV, "true").lower() == "true":
        report_usage_telemetry(
            "PyLibraryImport",
            activity_name,
            attributes={"version": _version.get_versions()['version'], "ImportType": "EXPLICIT_IMPORTED_BY_USER"},
        )
    else:
        # For unit test and robustness
        print(f"log_telemetry: {activity_name}")
