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
        if test_type==0:
            throttle_rpm_make(path, e0, e1, e2, e3, console_widget)
    except Exception as e:
        console_widget.alert(f"!+An error occurred: {e}")


def csv_make(path, e0=None, e1=None, e2=None, e3=None,console_widget=None):
    filenames = ["esc0.csv", "esc1.csv", "esc2.csv", "esc3.csv"]
    headers = ["Time", "Voltage (V)", "Current (A)", "Temperature (C)", "RPM",
               "Throttle Duty", "Motor Duty", "Phase Current", "Power(W)"]

    for i, data in enumerate([e0, e1, e2, e3]):
        if data is not None:
            console_widget.notify(f"++Creating CSV for e{i} at: {os.path.join(path, filenames[i])}")
            esc_csv_make(headers, data, os.path.join(path, filenames[i]),console_widget)
    console_widget.log("++All CSV files created.")

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
        console_widget.alert(f"!+An error occurred while writing CSV file {path}: {e}")


def throttle_rpm_make(path, e0=None, e1=None, e2=None, e3=None, console_widget=None):
    path = os.path.join(path, "Summary")
    os.makedirs(path, exist_ok=True)
    filenames = ["esc0-summary.csv", "esc1-summary.csv", "esc2-summary.csv", "esc3-summary.csv"]

    for i, data in enumerate([e0, e1, e2, e3]):
        if data is not None:
            file_path = os.path.join(path, filenames[i])  # Correct file path
            console_widget.notify(f"++Creating SUMMARY for e{i} at: {file_path}")
            try:
                head = ["Throttle", "RPM", "Voltage", "Current", "Temperature", "Phase Current", "Motor Duty",
                        "Serial Number: " + data.serial_number]
                rows = zip(data.mean_thr, data.mean_rpm,data.mean_voltage,data.mean_current,data.mean_temp,data.mean_phase_current,data.mean_m_duty)
                with open(file_path, 'w', newline='') as csvfile:  # Open file_path, not path
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(head)
                    writer.writerows(rows)
            except Exception as e:
                console_widget.alert(f"!+An error occurred while writing SUMMARY file {file_path}: {e}")

    console_widget.log("++All SUMMARY files created.")
