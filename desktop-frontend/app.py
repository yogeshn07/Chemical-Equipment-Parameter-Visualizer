import sys
import requests
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

BACKEND_UPLOAD_URL = "http://127.0.0.1:8000/api/upload/"
BACKEND_SUMMARY_URL = "http://127.0.0.1:8000/api/summary/"


class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.title = QLabel("<h2>Chemical Equipment Parameter Visualizer</h2>")
        layout.addWidget(self.title)

        self.upload_btn = QPushButton("Upload CSV File")
        self.upload_btn.clicked.connect(self.upload_csv)
        layout.addWidget(self.upload_btn)

        self.summary_label = QLabel("No data loaded yet.")
        layout.addWidget(self.summary_label)

        self.chart_btn = QPushButton("Show Chart")
        self.chart_btn.clicked.connect(self.show_chart)
        self.chart_btn.setEnabled(False)
        layout.addWidget(self.chart_btn)

        self.setLayout(layout)
        self.summary_data = None

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "rb") as f:
                response = requests.post(
                    BACKEND_UPLOAD_URL, files={"file": f}
                )

            if response.status_code != 200:
                QMessageBox.critical(self, "Error", "Upload failed")
                return

            self.fetch_summary()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def fetch_summary(self):
        response = requests.get(BACKEND_SUMMARY_URL)
        self.summary_data = response.json()

        text = (
            f"Total Equipment: {self.summary_data['total_equipment']}\n"
            f"Avg Flowrate: {self.summary_data['avg_flowrate']}\n"
            f"Avg Pressure: {self.summary_data['avg_pressure']}\n"
            f"Avg Temperature: {self.summary_data['avg_temperature']}"
        )

        self.summary_label.setText(text)
        self.chart_btn.setEnabled(True)

    def show_chart(self):
        labels = ["Flowrate", "Pressure", "Temperature"]
        values = [
            self.summary_data["avg_flowrate"],
            self.summary_data["avg_pressure"],
            self.summary_data["avg_temperature"],
        ]

        plt.bar(labels, values)
        plt.title("Average Equipment Parameters")
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())
