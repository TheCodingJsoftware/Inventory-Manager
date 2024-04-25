import requests
from PyQt6.QtCore import QThread, pyqtSignal

from utils.ip_utils import get_server_ip_address, get_server_port
from utils.json_file import JsonFile


class UploadThread(QThread):
    signal = pyqtSignal(object)

    def __init__(self, file_to_upload: list[str]) -> None:
        QThread.__init__(self)
        # Declaring server IP and port
        self.SERVER_IP: str = get_server_ip_address()
        self.SERVER_PORT: int = get_server_port()
        self.upload_url = f"http://{self.SERVER_IP}:{self.SERVER_PORT}/upload"

        self.files_to_upload = file_to_upload

    def run(self) -> None:
        try:
            for file_to_upload in self.files_to_upload:
                # Send the file as a POST request to the server
                if file_to_upload.endswith(".json"):
                    with open(f"data/{file_to_upload}", "rb") as file:
                        files = {"file": (file_to_upload, file.read(), "application/json")}
                elif file_to_upload.endswith(".jpeg"):
                    with open(f"images/{file_to_upload}", "rb") as file:
                        files = {"file": (file_to_upload, file.read(), "image/jpeg")}
                response = requests.post(self.upload_url, files=files)
                if response.status_code == 200:
                    self.signal.emit("Successfully uploaded")
                else:
                    self.signal.emit(response.status_code)
        except Exception as e:
            self.signal.emit(e)
            print(e)
