import json
import logging
import os
import sys
import zipfile
from datetime import datetime
from io import StringIO

import coloredlogs
import tornado.ioloop
import tornado.web
import tornado.websocket
from ansi2html import Ansi2HTMLConverter
from markupsafe import Markup

from utils.custom_print import CustomPrint, print_clients
from utils.files import get_file_type
from utils.inventory_updater import update_inventory
from utils.sheet_report import generate_sheet_report

# Store connected clients
connected_clients = set()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """
        This function gets logs, converts them to HTML format, marks them as safe HTML, and writes them.
        """
        logs = print_clients() + sys.stdout.getvalue()
        converter = Ansi2HTMLConverter()
        logs = converter.convert(logs)
        logs = Markup(logs)  # Mark the logs as safe HTML
        self.write(logs)


class FileSenderHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        """
        This function adds a client to a set of connected clients and prints information about the
        connection.
        """
        connected_clients.add(self)

        CustomPrint.print(
            f"INFO - Connection established with: {self.request.remote_ip} - Connected clients: {len(connected_clients)}",
            connected_clients=connected_clients,
        )

    def on_close(self):
        """
        This function removes a disconnected client from a list of connected clients and prints
        information about the disconnection.
        """
        connected_clients.remove(self)
        CustomPrint.print(
            f"INFO - Connection ended with: {self.request.remote_ip} - Connected clients: {len(connected_clients)}",
            connected_clients=connected_clients,
        )


class FileReceiveHandler(tornado.web.RequestHandler):
    # this downloads file per request of the client
    def get(self, filename):
        """
        This function checks if a requested file exists, and if it does, sends it as a response with
        appropriate headers, otherwise returns a 404 error.

        Args:
          filename: a string representing the name of the file that the client is requesting to
        download.
        """
        # Check if the requested file exists
        file_path = f"data/{filename}"
        try:
            with open(file_path, "rb") as file:
                data = file.read()

            # Set the response headers
            self.set_header("Content-Type", "application/json")
            self.set_header("Content-Disposition", f'attachment; filename="{filename}"')

            # Send the file as the response
            self.write(data)
            CustomPrint.print(
                f'INFO - Sent "{filename}" to {self.request.remote_ip}',
                connected_clients=connected_clients,
            )
        except FileNotFoundError:
            self.set_status(404)
            self.write(f'File "{filename}" not found.')
            CustomPrint.print(
                f'ERROR - File "{filename}" not found.',
                connected_clients=connected_clients,
            )

        self.finish()


class FileUploadHandler(tornado.web.RequestHandler):
    # this saves a file that the client uploads
    async def post(self):
        """
        This is an asynchronous function that receives a file, saves it to a local location, and updates
        inventory if the file is a JSON batch file.
        """
        file_info = self.request.files.get("file")
        should_signal_connect_clients: bool = False
        if file_info:
            file_data = file_info[0]["body"]
            file_name = file_info[0]["filename"]

            if get_file_type(file_name) == "JSON":
                # Save the received file to a local location
                with open(f"data/{file_name}", "wb") as file:
                    file.write(file_data)
            elif get_file_type(file_name) == "JPEG":
                # Save the received file to a local location
                with open(f"parts in inventory images/{file_name}", "wb") as file:
                    file.write(file_data)
            CustomPrint.print(
                f'INFO - Received "{file_name}" from {self.request.remote_ip}',
                connected_clients=connected_clients,
            )

            if file_name == "parts_batch_to_upload.json":
                self.write("Batch sent successfully")
                update_inventory(f"data/{file_name}", connected_clients)
            else:
                self.write("File uploaded successfully.")
            should_signal_connect_clients = True
            if should_signal_connect_clients and get_file_type(file_name) == "JSON":
                signal_clients_for_changes(client_to_ignore=self.request.remote_ip)
        else:
            self.write("No file received.")
            CustomPrint.print("ERROR - No file received.", connected_clients=connected_clients)


class ImageHandler(tornado.web.RequestHandler):
    def get(self, image_name):
        """
        This function retrieves an image file and sends it as a response to a client's request, or
        returns a 404 error if the file does not exist.

        Args:
          image_name: A string representing the name of the image file that the client is requesting.
        """
        filepath = os.path.join("parts in inventory images", image_name)
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                self.set_header("Content-Type", "image/jpeg")
                self.write(f.read())
            CustomPrint.print(
                f'INFO - Sent "{image_name}" to {self.request.remote_ip}',
                connected_clients=connected_clients,
            )
        else:
            self.set_status(404)


class CommandHandler(tornado.web.RequestHandler):
    def post(self):
        """
        This is a Python function that receives a command from a client, checks if it is
        "send_sheet_report", and if so, generates a sheet report and sends it to connected clients.
        """
        # Receive the command from the client
        command = self.get_argument("command")
        CustomPrint.print(
            f'INFO - Command "{command}" from {self.request.remote_ip}',
            connected_clients=connected_clients,
        )
        if command == "send_sheet_report":
            # await self.run_in_executor(self.generate_sheet_report)
            generate_sheet_report(connected_clients)
        # Send the response back to the client
        # self.write('done')
        self.finish()


class SetOrderNumberHandler(tornado.web.RequestHandler):
    def post(self):
        order_number = self.get_argument("order_number")
        if order_number is not None:
            # Process the received integer value
            with open("order_number.json", 'r') as file:
                json_file = json.load(file)
                json_file["order_number"] = int(order_number)

            with open("order_number.json", 'w') as file:
                json.dump(json_file, file)
                
            CustomPrint.print(
                f'INFO - {self.request.remote_ip} set order number to {order_number}',
                connected_clients=connected_clients,
            )
        else:
            self.set_status(400)  # Bad request status code


class GetOrderNumberHandler(tornado.web.RequestHandler):
    def get(self):
        # Retrieve the order number from wherever it is stored
        with open("order_number.json", 'r') as file:
            order_number = json.load(file)["order_number"]
        # Return the order number as a response
        self.write({"order_number": order_number})
        CustomPrint.print(
            f'INFO - Sent order number to {self.request.remote_ip}',
            connected_clients=connected_clients,
        )


def signal_clients_for_changes(client_to_ignore) -> None:
    """
    This function signals connected clients to download changes, except for the client specified to be
    ignored.

    Args:
      client_to_ignore: The IP address of a client that should be ignored and not signaled for changes.
    """
    CustomPrint.print(
        f"INFO - Signaling {len(connected_clients)} clients",
        connected_clients=connected_clients,
    )
    for client in connected_clients:
        if client.request.remote_ip == client_to_ignore:
            CustomPrint.print(
                f"INFO - Ignoring {client.request.remote_ip}",
                connected_clients=connected_clients,
            )
            continue
        if client.ws_connection and client.ws_connection.stream.socket:
            client.write_message("download changes")
            CustomPrint.print(
                f"INFO - Signaling {client.request.remote_ip} to download changes",
                connected_clients=connected_clients,
            )


def config_logs() -> None:
    """
    It configures the logs.
    """
    logging.basicConfig(
        filename=f"{os.path.dirname(os.path.realpath(__file__))}/logs/server.log",
        filemode="a",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level=logging.INFO,
    )


def backup_inventroy_files():
    """
    It backs up the inventory file to a backup file
    """
    logging.info("Backing up inventory files")
    files = os.listdir(f"{os.path.dirname(os.path.realpath(__file__))}/data")
    for file_path in files:
        path_to_zip_file: str = (
            f"{os.path.dirname(os.path.realpath(__file__))}/backups/{file_path} - {datetime.now().strftime('%B %d %A %Y %I-%M-%S %p')}.zip"
        )
        file = zipfile.ZipFile(path_to_zip_file, mode="w")
        file.write(
            f"{os.path.dirname(os.path.realpath(__file__))}/data/{file_path}",
            file_path,
            compress_type=zipfile.ZIP_DEFLATED,
        )
        file.close()
    logging.info("Inventory file backed up")
    CustomPrint.print("INFO - Backup complete", connected_clients=connected_clients)


if __name__ == "__main__":
    coloredlogs.install(level="INFO")  # Enable colored logs
    sys.stdout = StringIO()
    CustomPrint.print(
        """

                           **//*
                 *&&&&&&&&&&&&&&&%%%%%%
             %&&&&&&&&&&&&&&&&&&%%%%    #%%%%%(                                   ████████████████████
          &&&&&&&&&&&&%%%(           *%%%%%%((/                                  ████████████████████
       *&&&&&&&&&&&&%%(            %%%%%%(((    (##/                            ██▀                ██
      &&&&&&&&&&&&&%%           %%%%%%#((     #######               ▄████████                     ██                                 ██
    &&&&&&&&& #&&&%&          %%%%%#((*       %########           ▄█▀      ▀███▄▄████▄▄▄         ██
   &&&&&&&&   %&&%%%       %%%%%%(((           (#####(((         █▀          ██████    ▀█▄      ▄█            ▄▄   ▄▄█▄    ▄▄▄▄▄    ██          ▄███▄        ▄▄▄▄▄▄
  &&&&&&&&    %%%%%%     %%%%%#((                ##((((((       ██          █▀   ████    █     ██  ▀█▄██  ▄██████    ███  ██████ ▄████      ▄███▀   ▀     ▄▄██▀▀▀  
 %&&&&&&%     %%%%%%      ##((                    (((((((/      █          ▄█       ███  █    ██     ███▄██▀ ███     ███ █   ██   ███    ▄██▀   ▄       ▄█▀ ▄▄▄▄▄
 &&&&&&%      %%%%%%                    ###((((((((((((///      ██         ██        █████  ▄█▀      ████▀  ███     ███▀    ██   ███    ▄█     ██      ██  █▀  ███
*&&&&&&       %%%%%%                   /(##(((((((((//////       ██        ▀█          ██ ▄█▀       ███▀   ███      ██    ▄█▀   ███    ██     ███     ██      ▄██
(&&&&&&       %%%%%%                   /((((           ///        ██                    ▄██▀       ███    ███      ███  ▄██▀   ███    ██    ██ ██    ███     ▄██
 &&&&&%#      %%%%%#        %%%%#(     /((((         ***//         ▀██▄▄            ▄▄██▀         ███     ██       ████▀▀     ▄██     ██   ██ ███    ██    ▄▄█▀
 %%%&%%%       %%%#      /%%%%#((/     /((((      **//////           ▀▀██████████████▀           ███     ████     ▄█▀         ███▀    ▀████▀ ███     ▀██████▀
  %%%%%%%              %%%%##((        /////    *////////                                                                                    ██
  *%%%%%%%%         #%%%%#((/          *////   /////////                                                                                    ██
    %%%%%%%%#     %%%%#(((             ///// //////////                                                                                    ██
     %%%%%%%%%*%%%%##((*              ///////////////                                                                                    ▄██
       %%%%%%%%%##((/               ///////////////*                                                                             ▀█▄   ▄█▀
         #%####(((    #(          ///////////////                                                                                  ▀███▀
                 (####(((((((((//////////*
                           ****

"""
    )

    config_logs()
    # backup_inventroy_files()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/file/(.*)", FileReceiveHandler),
            (r"/command", CommandHandler),
            (r"/upload", FileUploadHandler),
            (r"/ws", FileSenderHandler),
            (r"/image/(.*)", ImageHandler),
            (r"/set_order_number", SetOrderNumberHandler),
            (r"/get_order_number", GetOrderNumberHandler),
        ]
    )
    app.listen(80)
    CustomPrint.print("INFO - Server started")
    tornado.ioloop.IOLoop.current().start()
