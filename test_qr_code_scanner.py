# test_qr_code_scanner.py
# Unit tests for the QR Code Scanner Utility.
# Author: Artiom LaMadrid

import os
import pytest
import qrcode
import cv2
import numpy as np
from pathlib import Path
import sys
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import csv
from qr_code_scanner import (
    get_camera_image,
    parse_qr_code,
    write_log_to_file,
    read_qr_code_from_camera,
)


def test_dummy():
    assert True, "This is a dummy test to ensure the test suite runs."


def test_get_camera_image_save():
    """Test if get_camera_image creates an image file."""
    get_camera_image("snapshot.png")
    assert os.path.exists("snapshot.png"), "Image file was not created."
    os.remove("snapshot.png")  # Clean up


def test_get_camera_image_return():
    """Test if get_camera_image returns an image."""
    image = get_camera_image()
    assert image is not None, "get_camera_image did not return an image."


def test_get_camera_image_failure():
    """Test if get_camera_image handles invalid camera index."""
    image = get_camera_image(filename="invalid_snapshot.png", camera_index=-1)
    assert (
        image is None
    ), "get_camera_image should return None when camera cannot be opened."
    if os.path.exists("invalid_snapshot.png"):
        os.remove("invalid_snapshot.png")


@pytest.fixture(scope="function")
def qr_test_image():
    data = "unit test string"
    filename = "unit_test_qr.png"
    qr = qrcode.make(data)
    qr.save(filename)
    image = cv2.imread(filename)
    yield data, image
    os.remove(filename)


def test_parse_qr_code_detects_code(qr_test_image):
    """Test if parse_qr_code detects a QR code."""
    data, image = qr_test_image
    qr_data = parse_qr_code(image)
    assert qr_data is not None, "parse_qr_code did not detect a QR code."


def test_parse_qr_code_returns_list(qr_test_image):
    """Test if parse_qr_code returns a list of strings."""
    data, image = qr_test_image
    qr_data = parse_qr_code(image)
    assert isinstance(qr_data, list), "parse_qr_code should return a list."
    assert all(
        isinstance(d, str) for d in qr_data
    ), "parse_qr_code should return a list of strings."


def test_parse_qr_code_correct_data(qr_test_image):
    """Test if parse_qr_code correctly decodes a QR code."""
    data, image = qr_test_image
    qr_data = parse_qr_code(image)
    assert data in qr_data, f"QR code data does not match expected: {data}"


def test_parse_qr_code_no_code():
    """Test if parse_qr_code returns None when no QR code is present."""
    image = np.zeros((300, 300, 3), dtype=np.uint8)
    qr_data = parse_qr_code(image)
    assert (
        qr_data is None
    ), "parse_qr_code should return None when no QR code is detected."

def test_read_qr_code_from_camera(mocker):
    """Test read_qr_code_from_camera with mocked dependencies."""
    mocker.patch("qr_code_scanner.parse_qr_code", return_value=["test QR code data"])
    result = read_qr_code_from_camera(timeout_duration=1)
    assert (
        result == "test QR code data"
    ), "read_qr_code_from_camera did not return expected QR code data."


def test_write_log_to_file():
    """Test if write_log_to_file creates a CSV log file with the correct content."""
    log_file = Path("test_log.csv")
    message = "This is a test log message."
    write_log_to_file(log_file, message)
    assert log_file.exists(), "Log file was not created."
    with open(log_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        assert len(rows) == 2, "Log file should have header and one message."
        assert rows[1][1] == message, "Log file should contain the correct message."
    log_file.unlink()


def test_write_log_to_file_no_message():
    """Test if write_log_to_file handles empty messages."""
    log_file = Path("test_log_empty.csv")
    write_log_to_file(log_file, "")
    assert log_file.exists(), "Log file was not created."
    with open(log_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        assert len(rows) == 2, "Log file should have header and one empty message."
        assert rows[1][1] == "", "Log file should contain empty message."
    log_file.unlink()


def test_write_log_to_file_no_filename():
    """Test if write_log_to_file handles no filename gracefully."""
    try:
        write_log_to_file("", "This should not raise an error.")
    except Exception as e:
        pytest.fail(
            f"write_log_to_file raised an exception when no filename was provided: {e}"
        )


def test_write_log_to_file_invalid_filename():
    """Test if write_log_to_file raises an OSError for invalid path."""
    with pytest.raises(OSError):
        write_log_to_file("/invalid/path/test_log.csv", "This should raise an error.")


def test_capture_stdout_and_stderr():
    """Test if capture_stdout_and_stderr captures stdout and stderr."""
    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        print("This is a test message.")
        try:
            raise Exception("This is a test exception.")
        except Exception as e:
            print(e, file=sys.stderr)
    assert (
        "This is a test message." in stdout.getvalue()
    ), "stdout did not capture the expected message."
    assert (
        "This is a test exception." in stderr.getvalue()
    ), "stderr did not capture the expected exception."
