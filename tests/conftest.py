import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DATA_DIR = os.path.join(BASE_DIR, "logdata")
LOG_DATA_GIT = "https://github.com/HearthSim/hsreplay-test-data"


def pytest_configure(config):
    if not os.path.exists(LOG_DATA_DIR):
        proc = subprocess.Popen(["git", "clone", LOG_DATA_GIT, LOG_DATA_DIR])
        assert proc.wait() == 0


def logfile(path):
    return os.path.join(LOG_DATA_DIR, "hslog-tests", path)
