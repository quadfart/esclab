import sys

import matplotlib.widgets
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import SpanSelector
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QGridLayout, QComboBox, QLabel, QWidget, QHBoxLayout, \
    QPushButton, QSpinBox

from abstraction import EscData


class ProcessTool(QDialog):
    def __init__(self,e0,e1,e2,e3):
        super().__init__()
        self.setWindowTitle("Process Tool")
        self.setGeometry(150, 150, 1408, 800)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        # Set up the QDialog layout
        main_layout = QVBoxLayout(self)
        layout = QGridLayout()
        main_layout.addLayout(layout)
        # Create a grid layout to hold the four plots
        grid_layout = QGridLayout()
        # Add the grid layout to the QDialog layout
        layout.addLayout(grid_layout,0,0)
        layout.setColumnStretch(1,2)

        self.esc0 : EscData = e0
        self.esc1 : EscData = e1
        self.esc2 : EscData = e2
        self.esc3 : EscData = e3

        right_layout = QVBoxLayout()
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Step Test", "Combined Step Test", "Flight Test"])
        self.dropdown.currentIndexChanged.connect(self.update_content)

        # Content box that changes based on dropdown selection
        # Labels for x-axis range
        self.x_range_label_esc0 = QLabel("Esc 0 Range: Not selected")
        self.x_range_label_esc1 = QLabel("Esc 1 Range: Not selected")
        self.x_range_label_esc2 = QLabel("Esc 2 Range: Not selected")
        self.x_range_label_esc3 = QLabel("Esc 3 Range: Not selected")


        self.step_box_layout = QVBoxLayout()
        self.step_test_label = QLabel("Step Test Post Process:")
        self.step_box_layout.addWidget(self.step_test_label)
        self.combined_step_box_layout = QVBoxLayout()
        self.combined_step_test_label = QLabel("Combined Step Test Post Process:")
        self.combined_step_box_layout.addWidget(self.combined_step_test_label)
        self.flight_box_layout = QVBoxLayout()
        self.flight_test_label = QLabel("Flight Test Post Process:")
        self.flight_box_layout.addWidget(self.flight_test_label)

        # Add dropdown, content label, and x-range label to right layout
        right_layout.addWidget(self.dropdown)
        right_layout.addWidget(self.x_range_label_esc0)
        right_layout.addWidget(self.x_range_label_esc1)
        right_layout.addWidget(self.x_range_label_esc2)
        right_layout.addWidget(self.x_range_label_esc3)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_layout.setSpacing(5)

        # Place Zero Utility
        place_zero_button_layout = QHBoxLayout()
        self.place_zero_button = QPushButton("Place 0")
        self.place_zero_button.clicked.connect(self.place_zero)
        self.int_input = QSpinBox()
        self.input_esc = QComboBox()
        self.input_esc.addItems(["Esc 0", "Esc 1", "Esc 2", "Esc 3"])
        self.input_esc.setCurrentIndex(0)
        self.int_input.setMaximum(self.get_max_index(0))
        self.input_esc.currentIndexChanged.connect(self.update_max_index)
        self.int_input.setMinimum(0)
        place_zero_button_layout.addWidget(self.place_zero_button)
        place_zero_button_layout.addWidget(self.int_input)
        place_zero_button_layout.addWidget(self.input_esc)
        right_layout.addLayout(place_zero_button_layout)
        # Place Zero Utility

        # Add the right layout to the main layout
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        layout.addWidget(right_widget,0,1)

        # Create a Matplotlib figure and axes
        self.fig, (self.ax0) = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.fig)
        # Add the canvas to the layout
        grid_layout.addWidget(self.canvas,1,0)
        grid_layout.addWidget(NavigationToolbar2QT(self.canvas,self),0,0)
        # Plot the data
        self.ax0.plot(self.esc0.timestamp, self.esc0.t_duty)
        self.ax0.set_ylim(-5, max(self.esc0.t_duty)+10)
        self.ax0.set_title('Esc 0')
        # Create the SpanSelector
        self.span0 = SpanSelector(
            self.ax0,
            self.onselect0,
            "horizontal",
            useblit=True,
            props=dict(alpha=0.5, facecolor="tab:blue"),
            interactive=True,
            drag_from_anywhere=True,
            ignore_event_outside=True,

        )
        # Create a Matplotlib figure and axes
        self.fig1, (self.ax1) = plt.subplots(figsize=(8, 6))
        self.canvas1 = FigureCanvas(self.fig1)
        # Add the canvas to the layout
        grid_layout.addWidget(self.canvas1,1,1)
        grid_layout.addWidget(NavigationToolbar2QT(self.canvas1, self), 0, 1)
        # Plot the data
        self.ax1.plot(self.esc1.timestamp, self.esc1.t_duty)
        self.ax1.set_ylim(-5, max(self.esc1.t_duty)+10)
        self.ax1.set_title('Esc 1')
        # Create the SpanSelector
        self.span1 = SpanSelector(
            self.ax1,
            self.onselect1,
            "horizontal",
            useblit=True,
            props=dict(alpha=0.5, facecolor="tab:gray"),
            interactive=True,
            drag_from_anywhere=True,
            ignore_event_outside=True
        )
        # Create a Matplotlib figure and axes
        self.fig2, (self.ax2) = plt.subplots(figsize=(8, 6))
        self.canvas2 = FigureCanvas(self.fig2)
        # Add the canvas to the layout
        grid_layout.addWidget(self.canvas2,3,0)
        grid_layout.addWidget(NavigationToolbar2QT(self.canvas2, self), 2, 0)
        # Plot the data
        self.ax2.plot(self.esc2.timestamp, self.esc2.t_duty)
        self.ax2.set_ylim(-5, max(self.esc2.t_duty)+10)
        self.ax2.set_title('Esc 2')
        # Create the SpanSelector
        self.span2 = SpanSelector(
            self.ax2,
            self.onselect2,
            "horizontal",
            useblit=True,
            props=dict(alpha=0.5, facecolor="tab:pink"),
            interactive=True,
            drag_from_anywhere=True,
            ignore_event_outside=True
        )
        # Create a Matplotlib figure and axes
        self.fig3, (self.ax3) = plt.subplots(figsize=(8, 6))
        self.canvas3 = FigureCanvas(self.fig3)
        # Add the canvas to the layout
        grid_layout.addWidget(self.canvas3,3,1)
        grid_layout.addWidget(NavigationToolbar2QT(self.canvas3, self), 2, 1)
        # Plot the data
        self.ax3.plot(self.esc3.timestamp, self.esc3.t_duty)
        self.ax3.set_ylim(-5, max(self.esc3.t_duty)+10)
        self.ax3.set_title('Esc 3')
        # Create the SpanSelector
        self.span3 = SpanSelector(
            self.ax3,
            self.onselect3,
            "horizontal",
            useblit=True,
            props=dict(alpha=0.5, facecolor="tab:orange"),
            interactive=True,
            drag_from_anywhere=True,
            ignore_event_outside=True
        )
    def onselect0(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.esc0.timestamp, (xmin, xmax))
        indmax = min(len(self.esc0.timestamp) - 1, indmax)

        region_x = self.esc0.timestamp[indmin:indmax]
        region_y = self.esc0.t_duty[indmin:indmax]

        # Print the start and end indices to the console
        print(f"Plot0:Selected range: Start index = {indmin}, End index = {indmax}")
        self.x_range_label_esc0.setText(f'Esc 0 Range : {indmin},{indmax}')

    def onselect1(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.esc1.timestamp, (xmin, xmax))
        indmax = min(len(self.esc1.timestamp) - 1, indmax)

        region_x = self.esc1.timestamp[indmin:indmax]
        region_y = self.esc1.t_duty[indmin:indmax]

        # Print the start and end indices to the console
        print(f"Plot1:Selected range: Start index = {indmin}, End index = {indmax}")
        self.x_range_label_esc1.setText(f'Esc 1 Range : {indmin},{indmax}')
    def onselect2(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.esc2.timestamp, (xmin, xmax))
        indmax = min(len(self.esc2.timestamp) - 1, indmax)

        region_x = self.esc2.timestamp[indmin:indmax]
        region_y = self.esc2.t_duty[indmin:indmax]

        # Print the start and end indices to the console
        print(f"Plot2:Selected range: Start index = {indmin}, End index = {indmax}")
        self.x_range_label_esc2.setText(f'Esc 2 Range : {indmin},{indmax}')
    def onselect3(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.esc3.timestamp, (xmin, xmax))
        indmax = min(len(self.esc3.timestamp) - 1, indmax)

        region_x = self.esc3.timestamp[indmin:indmax]
        region_y = self.esc3.t_duty[indmin:indmax]

        # Print the start and end indices to the console
        print(f"Plot3:Selected range: Start index = {indmin}, End index = {indmax}")
        self.x_range_label_esc3.setText(f'Esc 3 Range : {indmin},{indmax}')

    def update_content(self, index):
        # Update content based on dropdown selection
        if index == 0:
            self.content_label.setText("Content for Option 1")
        elif index == 1:
            self.content_label.setText("Content for Option 2")
        elif index == 2:
            self.content_label.setText("Content for Option 3")
    def place_zero(self):
        value = self.int_input.value()
        esc = self.input_esc.currentIndex()
        if esc == 0:
            self.esc0.t_duty[value]=0
        elif esc == 1:
            self.esc1.t_duty[value]=0
        elif esc == 2:
            self.esc2.t_duty[value]=0
        elif esc == 3:
            self.esc3.t_duty[value]=0
        self.ax0.clear()
        self.ax0.plot(self.esc0.timestamp, self.esc0.t_duty)
        self.canvas.draw()
        self.ax1.clear()
        self.ax1.plot(self.esc1.timestamp, self.esc1.t_duty)
        self.canvas1.draw()
        self.ax2.clear()
        self.ax2.plot(self.esc2.timestamp, self.esc2.t_duty)
        self.canvas2.draw()
        self.ax3.clear()
        self.ax3.plot(self.esc3.timestamp, self.esc3.t_duty)
        self.canvas3.draw()

    def get_max_index(self,esc):
        if esc == 0:
            return int(len(self.esc0.timestamp)-1)
        elif esc == 1:
            return int(len(self.esc1.timestamp)-1)
        elif esc == 2:
            return int(len(self.esc2.timestamp)-1)
        elif esc == 3:
            return int(len(self.esc3.timestamp)-1)
    def update_max_index(self,index):
        max_value = self.get_max_index(index)
        self.int_input.setMaximum(max_value)
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and display the dialog
    dialog = ProcessTool()
    dialog.exec()