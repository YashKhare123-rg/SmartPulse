import subprocess
import sys
import os


RETRAINING_SCRIPT = (
    r"E:\SmartPulse\ml\training\automatic_retraining.py"
)


def run_retraining(test_mode=False, db_password=None):

    command = [
        sys.executable,
        RETRAINING_SCRIPT
    ]

    if test_mode:
        command.append("--test")

    environment = os.environ.copy()

    if db_password:
        environment["SMARTPULSE_DB_PASSWORD"] = db_password

    environment["OPENBLAS_NUM_THREADS"] = "1"
    environment["OMP_NUM_THREADS"] = "1"
    environment["MKL_NUM_THREADS"] = "1"
    environment["NUMEXPR_NUM_THREADS"] = "1"

    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=environment
    )

    return {
        "success": process.returncode == 0,
        "return_code": process.returncode,
        "output": process.stdout,
        "error": process.stderr
    }