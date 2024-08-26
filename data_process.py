from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from pandas.core import indexes

from abstraction import EscData, take_values_from_csv


class StepTest(EscData):
    def __init__(self, esc_data,type=0,esc_id=0):
        super().__init__(esc_data.voltage, esc_data.current, esc_data.temp, esc_data.e_rpm, esc_data.t_duty,
                         esc_data.m_duty, esc_data.phase_current, esc_data.pwr, esc_data.stat_1, esc_data.stat_2,esc_data.serial_number)
        self.rpm = self.compute_rpm()
        self.running_array=[(1,0,0,0,0,1,0,1,0,1),(0,1,0,0,1,0,1,0,1,1),(0,0,1,0,1,1,0,0,1,1),(0,0,0,1,0,0,1,1,1,0)]

        self.zero_crossing=[]
        if type == 0:
            self.t_duty.insert(0,0)
            self.synchronize_steps(self.detect_step_commands())
            self.crop_data()
        elif type == 1:
            self.start_end_crop()
            print("type==1","esc_id:",esc_id)
            self.find_zero_crossing()
            print(self.zero_crossing)
            self.combined_step_syncro(esc_id=esc_id)

        elif type == 2:
            pass
        else:
            print("Error: Post Process Type Not recognized.")

    def start_end_crop(self):
        # Crop from the start
        for i, value in enumerate(self.t_duty):
            if value == 0:
                # Crop all lists up to and including the first zero in t_duty
                self.timestamp = self.timestamp[i:]
                self.voltage = self.voltage[i:]
                self.current = self.current[i:]
                self.temp = self.temp[i:]
                self.e_rpm = self.e_rpm[i:]
                self.t_duty = self.t_duty[i:]
                self.m_duty = self.m_duty[i:]
                self.phase_current = self.phase_current[i:]
                self.pwr = self.pwr[i:]
                self.stat_1 = self.stat_1[i:]
                self.stat_2 = self.stat_2[i:]
                break

        # Crop from the end
        for i in range(len(self.t_duty) - 1, -1, -1):
            if self.t_duty[i] == 0:
                # Crop all lists after the first zero from the end in t_duty
                self.timestamp = self.timestamp[:i + 1]
                self.voltage = self.voltage[:i + 1]
                self.current = self.current[:i + 1]
                self.temp = self.temp[:i + 1]
                self.e_rpm = self.e_rpm[:i + 1]
                self.t_duty = self.t_duty[:i + 1]
                self.m_duty = self.m_duty[:i + 1]
                self.phase_current = self.phase_current[:i + 1]
                self.pwr = self.pwr[:i + 1]
                self.stat_1 = self.stat_1[:i + 1]
                self.stat_2 = self.stat_2[:i + 1]
                break

    def combined_step_syncro(self, esc_id, step_duration_sec=35):
        # Initialize the arrays for storing synchronized data
        time, rpm, current, motor_duty, temp, throttle_duty, voltage = [], [], [], [], [], [], []

        # Get the running array for the given ESC ID
        running_arr = self.running_array[esc_id]

        # Total duration is step_duration_sec multiplied by the number of steps
        total_duration_sec = step_duration_sec * len(running_arr)

        # Calculate the overall time increment based on total duration
        overall_dt = total_duration_sec / len(running_arr)

        current_time = 0
        j=0
        for i_stp, run in enumerate(running_arr):
            if run:  # Only process steps where the ESC is running
                (step_start_idx, step_end_idx) = self.zero_crossing[j]
                j+=1
                # Calculate the number of data points in the current step
                num_points = step_end_idx - step_start_idx + 1

                # Calculate the time increment for this step
                dt = step_duration_sec / num_points

                # Create the time array for this step
                t_temp = np.arange(i_stp * step_duration_sec, (i_stp + 1) * step_duration_sec, dt)
                time.extend(t_temp)

                # Extend the other arrays with the data for this step
                rpm.extend(self.rpm[step_start_idx:step_end_idx + 1])
                current.extend(self.current[step_start_idx:step_end_idx + 1])
                motor_duty.extend(self.m_duty[step_start_idx:step_end_idx + 1])
                temp.extend(self.temp[step_start_idx:step_end_idx + 1])
                throttle_duty.extend(self.t_duty[step_start_idx:step_end_idx + 1])
                voltage.extend(self.voltage[step_start_idx:step_end_idx + 1])


            j = 0
            current_time += step_duration_sec
            time.append(current_time)
            rpm.append(0)
            current.append(0)
            motor_duty.append(0)
            temp.append(0)
            throttle_duty.append(0)
            voltage.append(0)

        if not running_arr[-1]:
            num_points = len(time) - len(rpm)
            print("NumPoints",num_points)# Number of points needed to fill the final segment
            if num_points > 0:
                t_temp = np.linspace(current_time, current_time + step_duration_sec, num_points, endpoint=False)
                time.extend(t_temp)

        # Ensure that time array length matches other arrays
        if len(time) != len(rpm):
            raise ValueError("Mismatch in the length of time and data arrays")

        # Update the object's attributes with the synchronized data
        self.rpm = rpm
        self.current = current
        self.m_duty = motor_duty
        self.temp = temp
        self.t_duty = throttle_duty
        self.voltage = voltage
        self.timestamp = time

        # Print the final timestamp to check the total time
        print(f"Final timestamp: {self.timestamp[-1]} seconds, Length {len(self.timestamp)}")

    def find_zero_crossing(self):
        start_index = []
        end_index = []

        for i in range(1, len(self.timestamp)):
            if self.t_duty[i] == 0 and self.t_duty[i - 1] != 0:
                start_index.append(self.timestamp[i])
            elif self.t_duty[i] != 0 and self.t_duty[i - 1] == 0:
                end_index.append(self.timestamp[i])

        # Ensure that the number of start and end indices are the same
        # to avoid index errors when appending to zero_crossing
        min_len = min(len(start_index), len(end_index))
        self.zero_crossing = [(end_index[i],start_index[i]) for i in range(min_len)]

    def compute_rpm(self,var=23):
        return np.array(self.e_rpm) / var

    def crop_data(self):
        del self.voltage[len(self.timestamp)-1:]
        del self.current[len(self.timestamp)-1:]
        del self.temp[len(self.timestamp)-1:]
        del self.rpm[len(self.timestamp)-1:]
        del self.t_duty[len(self.timestamp)-1:]
        del self.m_duty[len(self.timestamp)-1:]
        del self.phase_current[len(self.timestamp)-1:]
        del self.pwr[len(self.timestamp)-1:]
        del self.stat_1[len(self.timestamp)-1:]
        del self.stat_2[len(self.timestamp)-1:]
        del self.timestamp[-1]

    def detect_step_commands(self, threshold=9, min_gap=5):
        step_cmd_diff = np.diff(self.t_duty)
        step_cmd_idx = np.where(np.abs(step_cmd_diff) > threshold)[0]

        step_cmd_idx = [step_cmd_idx[i] for i in range(len(step_cmd_idx))
                        if i == 0 or (step_cmd_idx[i] - step_cmd_idx[i - 1] >= min_gap)]

        return step_cmd_idx

    def detect_difference_pairs(self, pairs: list, threshold_factor: float = 2) -> list:
        if not isinstance(pairs, list) or not all(isinstance(pair, tuple) and len(pair) == 2 for pair in pairs):
            raise TypeError("pairs must be a list of 2-element tuples.")
        differences = [abs(pair[0] - pair[1]) for pair in pairs]
        mean_diff = np.mean(differences)
        std_diff = np.std(differences)

        threshold = mean_diff + threshold_factor * std_diff
        filtered_pairs = [pairs[idx] for idx, diff in enumerate(differences) if diff <= threshold]

        while len(filtered_pairs) > 29:
            filtered_pairs.pop()

        return filtered_pairs

    def synchronize_steps(self, step_cmd_idx, step_duration_sec=5):
        time, rpm, current, motor_duty, temp, throttle_duty, voltage = [], [], [], [], [], [], []

        steps = [(step_cmd_idx[i], step_cmd_idx[i + 1] - 1) for i in range(len(step_cmd_idx) - 1)]

        filtered_steps = self.detect_difference_pairs(steps)

        for i_stp in range(len(filtered_steps)):
            step_start_idx, step_end_idx = filtered_steps[i_stp]

            dt = step_duration_sec / (step_end_idx - step_start_idx + 1)

            t_temp = np.arange(i_stp * step_duration_sec, (i_stp + 1) * step_duration_sec, dt)
            time.extend(t_temp)

            rpm.extend(self.rpm[step_start_idx:step_end_idx + 1])
            current.extend(self.current[step_start_idx:step_end_idx + 1])
            motor_duty.extend(self.m_duty[step_start_idx:step_end_idx + 1])
            temp.extend(self.temp[step_start_idx:step_end_idx + 1])
            throttle_duty.extend(self.t_duty[step_start_idx:step_end_idx + 1])
            voltage.extend(self.voltage[step_start_idx:step_end_idx + 1])

        self.rpm = rpm
        self.current = current
        self.m_duty = motor_duty
        self.temp = temp
        self.t_duty = throttle_duty
        self.voltage = voltage
        self.timestamp = time

        print("Step Test Values Set.")

    def plot_throttle_duty(self, step_cmd_idx):
        print("ThrottleDuty Data:",self.t_duty)
        plt.figure()
        plt.plot(self.t_duty)
        for idx in step_cmd_idx:
            plt.axvline(x=idx, color='r', linestyle='--')
        plt.show(block=False)

