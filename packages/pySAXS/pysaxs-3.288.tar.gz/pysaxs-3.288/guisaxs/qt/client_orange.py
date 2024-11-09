"""
Created on Tue July 23 11:06 2024
Labo : LIONS
@author: ines_robin
"""


from PyQt5 import QtCore, QtWidgets, uic, QtGui
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import socket
import threading
import time
import sys
import re
import pySAXS

# monitor the directory
class FileEventHandler(FileSystemEventHandler):
    def __init__(self, client_socket, client_dialog, message_signal):
        super().__init__()
        self.client_socket = client_socket
        self.client_dialog = client_dialog
        self.message_signal = message_signal

    def on_created(self, event):
        if not event.is_directory:
            self.send_file(event.src_path)
            self.client_dialog.resend_directory()

    def send_file(self, file_path):
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as file:
                    file_data = file.read()
                    self.client_socket.sendall(file_data)
                    message = f"Sent: {file_path}"
                    self.message_signal.emit(message)
            except Exception as e:
                message = f"Error sending {file_path}: {e}"
                self.message_signal.emit(message)
        else:
            message = f"File not found: {file_path}"
            self.message_signal.emit(message)

class ClientDialog(QtWidgets.QDialog):
    connection_established = QtCore.pyqtSignal()
    message_signal = QtCore.pyqtSignal(str)

    #def __init__(self):
    def __init__(self, parent=None):
        super().__init__()

        #self.workingdirectory = os.path.dirname(os.path.realpath(__file__))
        self.workingdirectory=""
        self.parent=parent
        if self.parent is not None:
            self.workingdirectory = self.parent.workingdirectory

        #self.ui = uic.loadUi(os.path.join(self.workingdirectory, "client1.ui"), self)
        self.ui = uic.loadUi(pySAXS.UI_PATH + "client1.ui", self)
        # Set the window icon
        #self.setWindowIcon(QtGui.QIcon(os.path.join(self.workingdirectory, "orange.png")))
        self.icon = QtGui.QIcon(pySAXS.ICON_PATH +"orange.png")
        self.setWindowIcon(self.icon)

        self.setWindowTitle('Connection client for Orange Data Mining ')
        self.ui.pushButton.clicked.connect(self.OnClick_pushButton)

        self.connected = False
        self.client_socket = None
        self.directory = None

        self.ip_input = self.ui.findChild(QtWidgets.QTextEdit, "textEdit")
        self.ip_input.setPlaceholderText("Enter server IP address")

        self.directory_display = self.ui.findChild(QtWidgets.QTextEdit, "textEdit_2")
        self.directory_display.setReadOnly(False)
        self.directory_display.setText(self.workingdirectory)

        self.log_display = self.ui.findChild(QtWidgets.QTextEdit, "textEdit_3")
        self.log_display.setReadOnly(True)

        self.select_directory_button = self.ui.findChild(QtWidgets.QToolButton, "toolButton")
        self.select_directory_button.clicked.connect(self.select_directory)

        self.message_signal.connect(self.update_log_display)

        #        if parent is not None:
        self.pref=None
        if self.parent is not None:
            self.pref=self.parent.pref
            if self.pref.fileExist():
                self.pref.read()
                # print( "ref file exist")
                server_adress = self.pref.get('server_adress', section="orange workflow")
                if server_adress is not None:
                    self.ip_input.setText(str(server_adress))


    def select_directory(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if directory:
            self.directory = directory
            self.directory_display.setText(directory)

    def OnClick_pushButton(self):
        # Connect Button
        host = self.ip_input.toPlainText().strip()
        if not self.is_valid_ip(host):
            message = "Please enter a valid IP address."
            self.show_error_message("Invalid IP Address", message)
            return

        manual_directory = self.directory_display.toPlainText().strip()
        if manual_directory:
            self.directory = manual_directory
        else:
            self.select_directory()
            if not self.directory:
                message = "Please select a directory."
                self.show_error_message("Invalid Directory", message)
                return
        #saving prefs
        self.savePrefs()
        #trying to connect in a thread
        threading.Thread(target=self.client_program, args=(host,)).start()

    def savePrefs(self):
        # save the preferences
        if self.parent is not None:
            self.pref.set('server_adress', section="orange workflow", value=str(self.ui.ip_input.toPlainText().strip()))
            self.pref.save()

    def update_log_display(self, message):
        current_text = self.log_display.toPlainText()
        new_text = f"{current_text}\n{message}"
        self.log_display.setText(new_text)

    def show_error_message(self, title, message):
        QtWidgets.QMessageBox.critical(self, title, message)

    def is_valid_ip(self, ip):
        # Validate IPv4 address
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if pattern.match(ip):
            return all(0 <= int(num) <= 255 for num in ip.split('.'))
        return False

    def client_program(self, host):
        port = 12345
        max_retries = 5
        retry_interval = 5
        retries = 0

        while retries < max_retries and not self.connected:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.settimeout(20)
                self.client_socket.connect((host, port))
                message = "Successfully connected to server."
                self.message_signal.emit(message)

                self.connection_established.emit()
                self.connected = True

                self.client_socket.sendall(self.directory.encode())
                message = f"Directory sent to server: {self.directory}"
                self.message_signal.emit(message)

                self.start_watching_directory()

                while self.connected:
                    time.sleep(1)

                break

            except socket.timeout:
                message = "Unable to connect to server within the timeout period."
                self.message_signal.emit(message)
                self.show_error_message("Connection Timeout", message)
            except ConnectionRefusedError:
                message = "Connection refused, retrying..."
                self.message_signal.emit(message)
            except Exception as e:
                message = f"An error occurred while connecting: {e}"
                self.message_signal.emit(message)
                self.show_error_message("Connection Error", message)
            finally:
                if self.client_socket:
                    self.client_socket.close()

                retries += 1
                if retries < max_retries and not self.connected:
                    message = f"Retrying connection in {retry_interval} seconds..."
                    self.message_signal.emit(message)
                    time.sleep(retry_interval)
                else:
                    message = "Maximum connection attempts reached or already connected. Stopping client."
                    self.message_signal.emit(message)

    def start_watching_directory(self):
        if os.path.exists(self.directory):
            self.event_handler = FileEventHandler(self.client_socket, self, self.message_signal)
            self.observer = Observer()
            self.observer.schedule(self.event_handler, self.directory, recursive=True)
            self.observer.start()
            message = f"Watching directory: {self.directory}"
            self.message_signal.emit(message)
        else:
            message = f"The directory {self.directory} does not exist."
            self.message_signal.emit(message)
            self.show_error_message("Directory Error", message)

    def resend_directory(self):
        if self.connected and self.client_socket:
            try:
                self.client_socket.sendall(self.directory.encode())
                message = f"Directory resent to server: {self.directory}"
                self.message_signal.emit(message)
            except Exception as e:
                message = f"Error sending directory to server: {e}"
                self.message_signal.emit(message)
                self.show_error_message("Directory Error", message)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = ClientDialog()
    myapp.show()
    sys.exit(app.exec_())
