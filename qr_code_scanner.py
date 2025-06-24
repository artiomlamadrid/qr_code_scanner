# QR Code Scanner Utility
# Author: Artiom LaMadrid
# Description: A Python script for scanning and logging QR codes using OpenCV and Pyzbar.
# Created: 2025-06-23

import os
import cv2
import time
import sys
import argparse
from datetime import datetime
import numpy as np
from typing import Optional
from pathlib import Path
import csv
from typing import Optional
from io import StringIO


def main() -> None:
    """Main function to handle command line arguments and initiate QR code scanning."""
    parser = argparse.ArgumentParser(
        description="Scan a QR code using the device's camera."
    )
    parser.add_argument(
        "--output", type=str, help="Optional filename to save QR code data."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout in seconds for QR code detection. Default is 10 seconds.",
    )
    args = parser.parse_args()

    if args.output:
        print(f"Output file: {args.output}")
    else:
        print("No output file provided, will only log result.")

    if args.timeout <= 0:
        print("Timeout must be a positive integer. Using default of 10 seconds.")
        args.timeout = 10
    print(f"Timeout set to: {args.timeout} seconds")

    qr_data = read_qr_code_from_camera(timeout_duration = args.timeout)
    
    print("QR code data:", qr_data if qr_data else "None")

    if qr_data:
        print("QR code detected.")
        if args.output:
            if os.path.exists(args.output):
                print(f"Warning: Overwriting existing file {args.output}")
            with open(args.output, "w") as f:
                f.write(qr_data)
            print(f"Data saved to {args.output}")
        else:
            print("No output file specified. QR code data not saved.")
        write_log_to_file("runtime_log.csv", f"QR code detected: {qr_data}")
    else:
        print("No QR code detected within timeout.")
        write_log_to_file("runtime_log.csv", f"No QR code detected within timeout.")

    return


def get_camera_image(
    filename: Optional[str] = None, camera_index: int = 0
) -> Optional[np.ndarray]:
    """Captures an image from the camera and optionally saves it to a file."""

    cap = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)
    if not cap.isOpened():
        print("Could not open camera")
        return None
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image from camera")
        cap.release()
        return None
    cap.release()
    if filename:
        cv2.imwrite(filename, frame)
        print(f"Image saved to {filename}")
    return frame


def parse_qr_code(image: np.ndarray) -> Optional[list[str]]:
    """Parses a QR code from the provided image and returns its data as a list of strings."""

    qr_decoder = cv2.QRCodeDetector()
    try:
        retval, data, points, _ = qr_decoder.detectAndDecodeMulti(image)
        if retval and data:
            return [d for d in data if d]
    except ValueError as e:
        print(f"Error decoding QR code: {e}")
    return None


def read_qr_code_from_camera(poll_interval: float = 0.2, timeout_duration: float = 10) -> Optional[str]:
    """Reads a QR code from the camera, polling at specified intervals until a QR code is detected or timeout occurs."""

    start_time = time.time()
    while time.time() - start_time < timeout_duration:
        frame = get_camera_image()  # Capture frame using get_camera_image
        if frame is None:
            print("No image captured.")
            continue
        qr_data = parse_qr_code(frame)
        if qr_data:
            return qr_data[0]  # Return the first QR code detected
        time.sleep(poll_interval)
    print("No QR code detected within the timeout period.")
    return None


def write_log_to_file(filename: str | Path, message: str) -> None:
    """Writes a log message to a specified CSV file with a timestamp."""

    if not filename:
        print("No filename provided for logging.")
        return
    path = Path(filename)
    if path.parent != Path("."):
        path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "a", newline="") as f:
            writer = csv.writer(f)
            if path.stat().st_size == 0:
                writer.writerow(["Timestamp", "Message"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message])
    except IOError as e:
        print(f"Error writing to log file: {e}")


def capture_stdout_and_stderr() -> tuple[StringIO, StringIO]:
    """Captures stdout and stderr to StringIO buffers for testing purposes."""

    stdout_buffer = StringIO()
    stderr_buffer = StringIO()
    sys.stdout = stdout_buffer
    sys.stderr = stderr_buffer
    return stdout_buffer, stderr_buffer


if __name__ == "__main__":
    main()
