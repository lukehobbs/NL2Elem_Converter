import os
import sys

from PyQt5.QtCore import pyqtSignal, QUrl, Qt
from PyQt5.QtGui import QDesktopServices, QCursor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QDesktopWidget, \
    QMessageBox
from nl2elem_to_csv.csv_writer import write_to_csv
from nl2elem_to_csv.data_processor import process_data
from nl2elem_to_csv.nl2elem_reader import read


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        # noinspection PyUnresolvedReferences
        self.clicked.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NL2Elem Converter")
        self.setWindowIcon(QIcon('icon.ico'))
        self.setGeometry(100, 100, 400, 200)
        self.center_window()

        # File selection button
        self.btn_select_file = QPushButton("Select File", self)
        self.btn_select_file.move(20, 20)
        self.btn_select_file.clicked.connect(self.open_file_dialog)

        # Display selected file path
        self.selected_file_label = QLineEdit(self)
        self.selected_file_label.move(120, 20)
        self.selected_file_label.setReadOnly(True)
        self.selected_file_label.setFixedWidth(250)

        # Initialize the output file label but hide it initially
        self.output_file_label = ClickableLabel(self)
        self.output_file_label.move(20, 130)
        self.output_file_label.setFixedWidth(360)
        self.output_file_label.setVisible(False)
        # noinspection PyUnresolvedReferences
        self.output_file_label.clicked.connect(self.open_output_location)
        self.abs_output_file_path = None

        # Convert button
        self.btn_convert = QPushButton("Convert", self)
        self.btn_convert.move(20, 60)
        self.btn_convert.clicked.connect(self.convert_file)
        self.btn_convert.setEnabled(False)  # Disabled until a file is selected

        # Status label
        self.status_label = QLabel("Status: Waiting for file selection...", self)
        self.status_label.move(20, 100)
        self.status_label.setFixedWidth(360)

    def center_window(self):
        window_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center)
        self.move(window_geometry.topLeft())

    def update_status(self, message, color="black"):
        colored_message = f"<span style='color:{color};'>{message}</span>"
        self.status_label.setText("Status: " + colored_message)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a .nl2elem file", "",
                                                   "NL2Elem Files (*.nl2elem)", options=options)
        if file_name:
            if not file_name.endswith('.nl2elem'):
                self.update_status("Invalid file type selected. Please select a .nl2elem file.", "red")
                self.btn_convert.setEnabled(False)  # Keep the convert button disabled
                return  # Exit the function without doing anything else

            self.status_label.setStyleSheet("")
            self.selected_file_label.setText(file_name)
            self.btn_convert.setEnabled(True)  # Enable the convert button only for valid file type
            self.update_status("File selected. Ready to convert.")

    def convert_file(self):
        input_file = self.selected_file_label.text()
        try:
            # Conversion
            data = read(input_file)
            processed_data = process_data(data)
            output_file = os.path.splitext(input_file)[0] + ".csv"
            write_to_csv(processed_data, output_file)

            # Check if the output file already exists
            if os.path.exists(output_file):
                reply = QMessageBox.question(self, 'File Exists',
                                             f"The file {os.path.basename(output_file)} already exists. Overwrite?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    self.update_status("Conversion cancelled. The output file exists.", "red")
                    return  # Exit without overwriting

            # Update status with a success message
            self.update_status("Conversion Complete!", "green")

            # Update and show the output file label
            self.abs_output_file_path = os.path.abspath(output_file)
            file_name = os.path.basename(output_file)
            self.output_file_label.setText(
                f'Output File: <span style="text-decoration: underline; color: blue; cursor: pointer;">{file_name}</span>')
            self.output_file_label.setCursor(QCursor(Qt.PointingHandCursor))
            self.output_file_label.setVisible(True)

            # Update select button label
            self.btn_select_file.setText("Select another file")
            self.btn_convert.setEnabled(False)

        except Exception as e:
            # Update status with an error message
            self.update_status(f"Conversion failed. Error: {str(e)}", "red")

    def open_output_location(self):
        if hasattr(self, 'abs_output_file_path') and os.path.exists(self.abs_output_file_path):
            output_dir = os.path.dirname(self.abs_output_file_path)
            QDesktopServices.openUrl(QUrl.fromLocalFile(output_dir))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
