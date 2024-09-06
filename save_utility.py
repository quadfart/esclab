import os
import csv

def test_mkdir(files_path, test_type, e0=None, e1=None, e2=None, e3=None,console_widget=None):
    try:
        directory = None
        if test_type == 0:
            directory = "StepTest"
        elif test_type == 1:
            directory = "CombinedStepTest"
        elif test_type == 2:
            directory = "FlightTest"

        path = os.path.join(files_path, directory)
        os.makedirs(path, exist_ok=True)
        csv_make(path, e0, e1, e2, e3, console_widget)
    except Exception as e:
        console_widget.log(f"An error occurred: {e}")


def csv_make(path, e0=None, e1=None, e2=None, e3=None,console_widget=None):
    filenames = ["esc0.csv", "esc1.csv", "esc2.csv", "esc3.csv"]
    headers = ["Time", "Voltage (V)", "Current (A)", "Temperature (C)", "RPM",
               "Throttle Duty", "Motor Duty", "Phase Current", "Power(W)"]

    for i, data in enumerate([e0, e1, e2, e3]):
        if data is not None:
            console_widget.log(f"Creating CSV for e{i} at: {os.path.join(path, filenames[i])}")
            esc_csv_make(headers, data, os.path.join(path, filenames[i]),console_widget)
    console_widget.log("All CSV files created.")

def esc_csv_make(headers, esc, path,console_widget=None):
    try:
        head = headers.copy()
        head.append("Serial Number: " + esc.serial_number)
        rows = zip(esc.timestamp, esc.voltage, esc.current, esc.temp, esc.rpm,
                   esc.t_duty, esc.m_duty, esc.phase_current, esc.pwr)
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(head)
            writer.writerows(rows)
    except Exception as e:
        console_widget.log(f"An error occurred while writing CSV file {path}: {e}")