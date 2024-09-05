import tempfile
import pandas as pd
import plotly.express as px
from PyQt6.QtCore import pyqtSlot, QObject, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QFileDialog, \
    QTabWidget, QListWidget, QHBoxLayout, QCheckBox, QLabel, QComboBox
from PyQt6.QtCore import Qt

from abstraction import EscData
from data_process import PostProcess


class ComparisonView(QDialog):
    def __init__(self,e0=None,e1=None,e2=None,e3=None,post_process=False):
        super().__init__()
        self.df_esc0=None
        self.df_esc1=None
        self.df_esc2=None
        self.df_esc3=None
        self.esc0= None
        self.esc1= None
        self.esc2= None
        self.esc3= None
        if not post_process:
            if e0:
                self.esc0 : EscData = e0
            if e1:
                self.esc1 : EscData = e1
            if e2:
                self.esc2 : EscData = e2
            if e3:
                self.esc3 : EscData = e3

            self.setWindowTitle("Comparison View")
            self.setGeometry(150, 150, 800, 600)
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
            self.list_widget = QListWidget()
            self.list_widget.addItems(['Voltage', 'Current', 'Temperature', 'eRPM', 'Throttle Duty',
                                   'Motor Duty', 'Phase Current', 'Power', 'Status 1', 'Status 2'])
        else:
            if e0:
                self.esc0 : PostProcess = e0
            if e1:
                self.esc1 : PostProcess = e1
            if e2:
                self.esc2 : PostProcess = e2
            if e3:
                self.esc3 : PostProcess = e3

            self.setWindowTitle("Comparison View - Post Processed")
            self.setGeometry(150, 150, 800, 600)
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
            self.list_widget = QListWidget()
            self.list_widget.addItems(['Voltage', 'Current', 'Temperature', 'RPM', 'Throttle Duty',
                                   'Motor Duty','Phase Current','Power'])


        self.selected_value = 'Voltage'
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.browser = QWebEngineView()
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.list_widget)
        h_layout.addWidget(self.browser)
        h_layout.setStretchFactor(self.list_widget, 1)
        h_layout.setStretchFactor(self.browser, 5)
        self.setLayout(h_layout)
        print("here")
        if not post_process:
            self.load_data()
        else:
            self.load_data_post_process()

        self.update_plot()


    def load_data(self):
        if self.esc0:
            self.df_esc0 = pd.DataFrame({
                'Time': self.esc0.timestamp,
                'Voltage': self.esc0.voltage,
                'Current': self.esc0.current,
                'Temperature': self.esc0.temp,
                'eRPM': self.esc0.e_rpm,
                'Throttle Duty': self.esc0.t_duty,
                'Motor Duty': self.esc0.m_duty,
                'Phase Current': self.esc0.phase_current,
                'Power': self.esc0.pwr,
                'Status 1': self.esc0.stat_1,
                'Status 2': self.esc0.stat_2,
                'Serial Number': self.esc0.serial_number
            })
            self.df_esc0['ESC'] = 'ESC0'
            print("ESC0 DataFrame created successfully")
            print(self.df_esc0.head())

        if self.esc1:
            self.df_esc1 = pd.DataFrame({
                'Time': self.esc1.timestamp,
                'Voltage': self.esc1.voltage,
                'Current': self.esc1.current,
                'Temperature': self.esc1.temp,
                'eRPM': self.esc1.e_rpm,
                'Throttle Duty': self.esc1.t_duty,
                'Motor Duty': self.esc1.m_duty,
                'Phase Current': self.esc1.phase_current,
                'Power': self.esc1.pwr,
                'Status 1': self.esc1.stat_1,
                'Status 2': self.esc1.stat_2,
                'Serial Number': self.esc1.serial_number
            })
            self.df_esc1['ESC'] = 'ESC1'
            print("ESC1 DataFrame created successfully")
            print(self.df_esc1.head())

        if self.esc2:
            self.df_esc2 = pd.DataFrame({
                'Time': self.esc2.timestamp,
                'Voltage': self.esc2.voltage,
                'Current': self.esc2.current,
                'Temperature': self.esc2.temp,
                'eRPM': self.esc2.e_rpm,
                'Throttle Duty': self.esc2.t_duty,
                'Motor Duty': self.esc2.m_duty,
                'Phase Current': self.esc2.phase_current,
                'Power': self.esc2.pwr,
                'Status 1': self.esc2.stat_1,
                'Status 2': self.esc2.stat_2,
                'Serial Number': self.esc2.serial_number
            })
            self.df_esc2['ESC'] = 'ESC2'
            print("ESC2 DataFrame created successfully")
            print(self.df_esc2.head())

        if self.esc3:
            self.df_esc3 = pd.DataFrame({
                'Time': self.esc3.timestamp,
                'Voltage': self.esc3.voltage,
                'Current': self.esc3.current,
                'Temperature': self.esc3.temp,
                'eRPM': self.esc3.e_rpm,
                'Throttle Duty': self.esc3.t_duty,
                'Motor Duty': self.esc3.m_duty,
                'Phase Current': self.esc3.phase_current,
                'Power': self.esc3.pwr,
                'Status 1': self.esc3.stat_1,
                'Status 2': self.esc3.stat_2,
                'Serial Number': self.esc3.serial_number
            })
            self.df_esc3['ESC'] = 'ESC3'
            print("ESC3 DataFrame created successfully")
            print(self.df_esc3.head())

        self.df_combined = pd.concat([self.df_esc0, self.df_esc1, self.df_esc2, self.df_esc3])

    def load_data_post_process(self):
        try:
            if self.esc0:
                self.df_esc0 = pd.DataFrame({
                    'Time': self.esc0.timestamp,
                    'Voltage': self.esc0.voltage,
                    'Current': self.esc0.current,
                    'Temperature': self.esc0.temp,
                    'RPM': self.esc0.rpm,
                    'Throttle Duty': self.esc0.t_duty,
                    'Motor Duty': self.esc0.m_duty,
                    'Phase Current': self.esc0.phase_current,
                    'Power': self.esc0.pwr,
                    'Serial Number': self.esc0.serial_number
                })
                self.df_esc0['ESC'] = 'ESC0'
                print("ESC0 DataFrame created successfully")
                print(self.df_esc0.head())
            if self.esc1:
                self.df_esc1 = pd.DataFrame({
                    'Time': self.esc1.timestamp,
                    'Voltage': self.esc1.voltage,
                    'Current': self.esc1.current,
                    'Temperature': self.esc1.temp,
                    'RPM': self.esc1.rpm,
                    'Throttle Duty': self.esc1.t_duty,
                    'Motor Duty': self.esc1.m_duty,
                    'Phase Current': self.esc1.phase_current,
                    'Power': self.esc1.pwr,
                    'Serial Number': self.esc1.serial_number
                })
                self.df_esc1['ESC'] = 'ESC1'
                print("ESC1 DataFrame created successfully")
                print(self.df_esc1.head())
            if self.esc2:
                self.df_esc2 = pd.DataFrame({
                    'Time': self.esc2.timestamp,
                    'Voltage': self.esc2.voltage,
                    'Current': self.esc2.current,
                    'Temperature': self.esc2.temp,
                    'RPM': self.esc2.rpm,
                    'Throttle Duty': self.esc2.t_duty,
                    'Motor Duty': self.esc2.m_duty,
                    'Phase Current': self.esc2.phase_current,
                    'Power': self.esc2.pwr,
                    'Serial Number': self.esc2.serial_number
                })
                self.df_esc2['ESC'] = 'ESC2'
                print("ESC2 DataFrame created successfully")
                print(self.df_esc2.head())
            if self.esc3:
                self.df_esc3 = pd.DataFrame({
                    'Time': self.esc3.timestamp,
                    'Voltage': self.esc3.voltage,
                    'Current': self.esc3.current,
                    'Temperature': self.esc3.temp,
                    'RPM': self.esc3.rpm,
                    'Throttle Duty': self.esc3.t_duty,
                    'Motor Duty': self.esc3.m_duty,
                    'Phase Current': self.esc3.phase_current,
                    'Power': self.esc3.pwr,
                    'Serial Number': self.esc3.serial_number
                })
                self.df_esc3['ESC'] = 'ESC3'
                print("ESC3 DataFrame created successfully")
                print(self.df_esc3.head())

            self.df_combined = pd.concat([self.df_esc0, self.df_esc1, self.df_esc2, self.df_esc3])
            print("Combined DataFrame created successfully")
            print(self.df_combined.head())

        except Exception as e:
            print(f"An error occurred: {e}")

    def on_item_clicked(self, item):
        self.selected_value = item.text()
        print(f"Selected value: {self.selected_value}")
        self.update_plot()

    def update_plot(self):
        fig = px.line(self.df_combined, x='Time', y=self.selected_value, color='ESC',
                      labels={'Time': 'Time', self.selected_value: self.selected_value},
                      title='Comparison View')

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            fig.write_html(tmp_file.name)
            tmp_file_path = tmp_file.name

        self.browser.setUrl(QUrl.fromLocalFile(tmp_file_path))