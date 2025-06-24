# QR Code Scanner Utility

This is a lightweight Python application for scanning and logging QR codes from webcam or image input. Built using `opencv-python` and `pyzbar`.

## Author

**Artiom LaMadrid**

Built as part of a portfolio project. Originally developed during the CS50 Introduction to Programming with Python course.

---

## Functionality

The core of the program is built around a few main functions:

- **`get_camera_image(filename=None, camera_index=0)`**
  - Captures a single image from the device's default camera.
  - Saves the image to disk if a filename is provided.
  - Returns the captured image (OpenCV `numpy.ndarray`), or `None` if it fails.

- **`parse_qr_code(image)`**
  - Takes an OpenCV image array and detects QR codes.
  - Returns a list of decoded strings if successful, or `None` if no code is found.

- **`read_qr_code_from_camera(poll_interval=0.2, timeout_duration=10)`**
  - Continuously checks the camera every 200ms for up to 10 seconds.
  - Returns the first QR code’s data as a string if found, or `None`.

- **`try_with_timeout(func, timeout=10, raise_exception=False)`**
  - Wraps any function call with a timeout using Unix signal handling.
  - Returns function result or `None` if timeout occurs.

- **`write_log_to_file(filename, string)`**
  - Appends messages to a CSV log file (`runtime_log.csv`) with timestamps.
  - Logs start, results, and completion of each session.

- **`main()`**
  - Program entry point. Reads a QR code, logs the result, and optionally saves it to a file.

---

## Performed Testing

- Unit tests implemented using `pytest`:
  - Camera image capture (success and failure cases)
  - QR code detection (positive, negative, and edge cases)
  - Timeout logic
  - CSV log writing
- Tested with:
  - MacBook Air camera (macOS Sonoma 15.5)
  - External QR codes (e.g., from a phone screen)
  - Test QR images generated with `qrcode` module

---

## Tools Used

- [VS Code](https://code.visualstudio.com/)
- [Github] https://github.com
- [Copilot](https://github.com/features/copilot)
- [ChatGPT](https://chat.openai.com/)
- [Grok](https://x.ai/)
- [Stack Overflow](https://stackoverflow.com/)
- [pytest](https://docs.pytest.org/)
- [OpenCV](https://opencv.org/)
- [qrcode](https://pypi.org/project/qrcode/)

---

## Installation

**System requirements:**

- macOS or Linux with access to a physical camera
- Python 3.12 or later

**Setup instructions:**

1. Clone the repository:
   ```bash
   git clone https://github.com/artiomlamadrid/qr_code_scanner.git
   cd qr_code_scanner