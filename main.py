import os
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QFileDialog, \
    QTabWidget, QListWidget, QHBoxLayout, QCheckBox, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
import tempfile
from plotly.subplots import make_subplots
from abstraction import take_values_from_csv, EscData

class CombinedView(QDialog):
    def __init__(self,e0,e1,e2,e3):
        super().__init__()

        self.esc0 = e0
        self.esc1 = e1
        self.esc2 = e2
        self.esc3 = e3

        self.setWindowTitle("Combined View")
        self.setGeometry(150,150,800,600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        self.checkbox_layout = QVBoxLayout()
        self.checkboxes = []
        names = ['Voltage','Current','Temperature','eRPM','Throttle Duty','Motor Duty','Phase Current','Power','Status 1','Status 2']
        for i in range(10):
            checkbox = QCheckBox(names[i])
            checkbox.stateChanged.connect(self.update_status)
            self.checkbox_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        checkbox_container = QWidget()
        checkbox_container.setLayout(self.checkbox_layout)

        self.browser = QWebEngineView()

        main_layout = QHBoxLayout()

        main_layout.addWidget(self.browser)
        main_layout.addWidget(checkbox_container)

        main_layout.setStretchFactor(checkbox_container, 1)
        main_layout.setStretchFactor(self.browser, 6)

        self.setLayout(main_layout)

        self.status_label = QLabel()
        self.checkbox_layout.addWidget(self.status_label)

        self.load_data()
        self.update_plot(None)

    def update_status(self):
        checked_boxes = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        print(checked_boxes)
        self.update_plot(checked_boxes)
    def load_data(self):

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

        self.df_esc0['ESC'] = 'ESC0'
        self.df_esc1['ESC'] = 'ESC1'
        self.df_esc2['ESC'] = 'ESC2'
        self.df_esc3['ESC'] = 'ESC3'
        self.df_combined = pd.concat([self.df_esc0, self.df_esc1, self.df_esc2, self.df_esc3])

    def update_plot(self, option=None):
        if option is None or not all(col in self.df_combined.columns for col in option):
            fig = make_subplots(rows=1, cols=1)
        else:
            num_columns = len(option)
            num_rows = (num_columns - 1) // 3 + 1

            fig = make_subplots(rows=num_rows, cols=3,
                                subplot_titles=option,
                                shared_xaxes='all',
                                vertical_spacing=0.15,
                                horizontal_spacing=0.1)
            esc_colors = {
                'ESC0': 'blue',
                'ESC1': 'red',
                'ESC2': 'green',
                'ESC3': 'purple'
            }
            esc_traces = {esc: [] for esc in self.df_combined['ESC'].unique()}
            for i, col_name in enumerate(option):
                row = i // 3 + 1
                col = i % 3 + 1
                for esc in self.df_combined['ESC'].unique():
                    df_filtered = self.df_combined[self.df_combined['ESC'] == esc]
                    trace = go.Scatter(
                        x=df_filtered['Time'],
                        y=df_filtered[col_name],
                        mode='lines',
                        name=f"{col_name} ({esc})",
                        line=dict(color=esc_colors.get(esc, 'black')),
                        legendgroup=esc
                    )
                    esc_traces[esc].append(trace)
                    fig.add_trace(trace, row=row, col=col)
            for esc, traces in esc_traces.items():
                fig.add_trace(
                    go.Scatter(
                        x=[],
                        y=[],
                        mode='lines',
                        name=esc,
                        line=dict(color=esc_colors.get(esc, 'black')),
                        visible='legendonly',
                        legendgroup=esc
                    )
                )
            fig.update_layout(
                showlegend=True,
                title="ESC Data Over Time"
            )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            fig.write_html(tmp_file.name)
            tmp_file_path = tmp_file.name
        self.browser.setUrl(QUrl.fromLocalFile(tmp_file_path))

class ComparisonView(QDialog):
    def __init__(self,e0,e1,e2,e3):
        super().__init__()

        self.esc0 = e0
        self.esc1 = e1
        self.esc2 = e2
        self.esc3 = e3

        self.setWindowTitle("Individual View")
        self.setGeometry(150, 150, 800, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        self.selected_value = 'Voltage'
        self.list_widget = QListWidget()
        self.list_widget.addItems(['Voltage', 'Current', 'Temperature', 'eRPM', 'Throttle Duty',
                                   'Motor Duty', 'Phase Current', 'Power', 'Status 1', 'Status 2'])
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.browser = QWebEngineView()
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.list_widget)
        h_layout.addWidget(self.browser)
        h_layout.setStretchFactor(self.list_widget, 1)
        h_layout.setStretchFactor(self.browser, 5)
        self.setLayout(h_layout)

        self.load_data()
        self.update_plot()

    def load_data(self):
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

        self.df_esc0['ESC'] = 'ESC0'
        self.df_esc1['ESC'] = 'ESC1'
        self.df_esc2['ESC'] = 'ESC2'
        self.df_esc3['ESC'] = 'ESC3'
        self.df_combined = pd.concat([self.df_esc0, self.df_esc1, self.df_esc2, self.df_esc3])

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

class IndividualView(QDialog):
    def __init__(self,e0,e1,e2,e3):
        super().__init__()
        self.esc0=e0
        self.esc1=e1
        self.esc2=e2
        self.esc3=e3

        # Set window title and size
        self.setWindowTitle("Individual View")
        self.setGeometry(150, 150, 800, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        self.tab_widget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        self.create_tab("ESC 0", self.create_plot_1())
        self.create_tab("ESC 1", self.create_plot_2())
        self.create_tab("ESC 2", self.create_plot_3())
        self.create_tab("ESC 3", self.create_plot_4())

    def create_plot_1(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc0.voltage))),
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
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-0'+'  '+'Serial Number'+ self.esc0.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

    def create_plot_2(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc1.voltage))),
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
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-1'+'  '+'Serial Number'+ self.esc1.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

    def create_plot_3(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc2.voltage))),
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
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-2'+'  '+'Serial Number'+ self.esc2.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

    def create_plot_4(self):
        try:
            df = pd.DataFrame({
                'Index': list(range(len(self.esc3.voltage))),
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
            fig = px.line(df, x='Index', y=['Voltage','Current','Temperature','eRPM','Throttle Duty','Motor Duty','Phase Current','Power'], title='ESC-3'+'  '+'Serial Number'+ self.esc3.serial_number)
            return fig
        except Exception as e:
            print(f"Error in create_plot_1: {e}")
            return px.Figure()

    def create_tab(self, title, fig):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            fig.write_html(tmp_file.name)
            tmp_file_path = tmp_file.name

        browser = QWebEngineView()
        browser.setUrl(QUrl.fromLocalFile(tmp_file_path))

        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(browser)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, title)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My PyQt6 Window")
        self.setGeometry(100, 100, 900, 400)

        self.esc0_data =[]
        self.esc1_data =[]
        self.esc2_data =[]
        self.esc3_data =[]

        self.folder_selected=False

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Left side layout
        left_layout = QVBoxLayout()
        left_layout.setSpacing(30)
        main_layout.addLayout(left_layout, stretch=3)

        # Logo placeholder
        self.logo_label = QLabel("Logo", self)  # Replace with actual logo if available
        left_layout.addWidget(self.logo_label)

        # Buttons on the left side
        self.individual_view_button = QPushButton("Individual View", self)
        self.individual_view_button.clicked.connect(self.open_individual_view_window)
        self.individual_view_button.setFixedHeight(60)
        left_layout.addWidget(self.individual_view_button)
        self.individual_view_button.setEnabled(False)

        self.comparison_view_button = QPushButton("Comparison View", self)
        self.comparison_view_button.clicked.connect(self.open_comparison_view_window)
        self.comparison_view_button.setFixedHeight(60)
        left_layout.addWidget(self.comparison_view_button)
        self.comparison_view_button.setEnabled(False)

        self.combined_view_button = QPushButton("Combined View", self)
        self.combined_view_button.clicked.connect(self.open_combined_view_window)
        self.combined_view_button.setFixedHeight(60)
        left_layout.addWidget(self.combined_view_button)
        self.combined_view_button.setEnabled(False)

        # Right side layout
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        main_layout.addLayout(right_layout, stretch=1)

        # Folder button and display widget on the right side
        self.folder_button = QPushButton("Select Folder", self)
        self.folder_button.clicked.connect(self.open_folder_browser)
        right_layout.addWidget(self.folder_button)

        self.path_display_widget = QWidget()
        self.path_display_widget.setFixedHeight(30)
        right_layout.addWidget(self.path_display_widget)

        self.path_label = QLabel("No folder selected", self)
        self.path_display_widget_layout = QVBoxLayout()
        self.path_display_widget.setLayout(self.path_display_widget_layout)
        self.path_display_widget_layout.addWidget(self.path_label)
        self.path_display_widget.setStyleSheet("background-color: gray;")

        self.load_button = QPushButton("Load Data", self)
        self.load_button.clicked.connect(self.load_data_button)
        self.load_button.setEnabled(False)
        right_layout.addWidget(self.load_button)

        self.load_display_widget = QWidget()
        self.load_display_widget.setFixedHeight(30)
        right_layout.addWidget(self.load_display_widget)

        self.load_label = QLabel("Files not Loaded !", self)
        self.load_display_widget_layout = QVBoxLayout()
        self.load_display_widget.setLayout(self.load_display_widget_layout)
        self.load_display_widget_layout.addWidget(self.load_label)
        self.load_display_widget.setStyleSheet("background-color: gray;")

        self.manipulate_button = QPushButton("Manipulate Data", self)
        self.manipulate_button.clicked.connect(self.manipulate_data_button)
        self.manipulate_button.setEnabled(False)
        right_layout.addWidget(self.manipulate_button)

        self.manipulate_display_widget = QWidget()
        self.manipulate_display_widget.setFixedHeight(30)
        right_layout.addWidget(self.manipulate_display_widget)

        self.manipulate_label = QLabel("No Action!", self)
        self.manipulate_display_widget_layout = QVBoxLayout()
        self.manipulate_display_widget.setLayout(self.manipulate_display_widget_layout)
        self.manipulate_display_widget_layout.addWidget(self.manipulate_label)
        self.manipulate_display_widget.setStyleSheet("background-color: gray;")

        self.save_button = QPushButton("Save Manipulated Data", self)
        self.save_button.clicked.connect(self.save_action)
        self.save_button.setEnabled(False)
        right_layout.addWidget(self.save_button)

    def save_action(self):
        pass
    def manipulate_data_button(self):
        self.manipulate_label.setText("Clicked (No Function Yet!)")
        self.manipulate_display_widget.setStyleSheet("background-color: green;")
        self.save_button.setEnabled(True)

    def load_data_button(self):
            try:
                self.esc0_data = take_values_from_csv(Path(self.files_path[0]))
                self.esc1_data = take_values_from_csv(Path(self.files_path[1]))
                self.esc2_data = take_values_from_csv(Path(self.files_path[2]))
                self.esc3_data = take_values_from_csv(Path(self.files_path[3]))

                if all([self.esc0_data is not None, self.esc1_data is not None,
                        self.esc2_data is not None, self.esc3_data is not None]):
                    self.manipulate_button.setEnabled(True)
                    self.combined_view_button.setEnabled(True)
                    self.individual_view_button.setEnabled(True)
                    self.comparison_view_button.setEnabled(True)
                    self.load_label.setText("Files Loaded")
                    self.load_display_widget.setStyleSheet("background-color: green;")
                else:
                    self.manipulate_button.setEnabled(False)
                    self.load_label.setText("Failed to Load")
                    self.load_display_widget.setStyleSheet("background-color: gray;")
            except Exception as e:
                print(f"An error occurred: {e}")
                self.manipulate_button.setEnabled(False)
                self.load_label.setText("Error occurred")
                self.path_display_widget.setStyleSheet("background-color: gray;")


    def open_folder_browser(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_name:
            print(f"Selected folder: {folder_name}")

            self.files_path = []  # Clear the previous file paths
            valid_folder = False

            for i in range(4):
                csv_name = os.path.join(folder_name, f"esc{i}.csv")
                if os.path.isfile(csv_name):
                    self.files_path.append(csv_name)
                    valid_folder = True
                else:
                    print(f"File not found: {csv_name}")

            if self.files_path:
                self.load_button.setEnabled(True)  # Enable button only if at least one file exists
            else:
                self.load_button.setEnabled(False)  # Disable button if no files are found

            # Update folder path display
            self.path_label.setText(f"Selected Folder: {folder_name}")
            if valid_folder:
                self.path_display_widget.setStyleSheet("background-color: green;")
            else:
                self.path_display_widget.setStyleSheet("background-color: gray;")

            print(self.files_path)

    def open_individual_view_window(self):
        self.plot_window = IndividualView(e0=self.esc0_data,e1=self.esc1_data,e2=self.esc2_data,e3=self.esc3_data)
        self.plot_window.exec()

    def open_comparison_view_window(self):
        dialog = ComparisonView(e0=self.esc0_data,e1=self.esc1_data,e2=self.esc2_data,e3=self.esc3_data)
        dialog.exec()

    def open_combined_view_window(self):
        dialog = CombinedView(e0=self.esc0_data,e1=self.esc1_data,e2=self.esc2_data,e3=self.esc3_data)
        dialog.exec()

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())