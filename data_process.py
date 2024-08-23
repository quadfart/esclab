from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from pandas.core import indexes

from abstraction import EscData, take_values_from_csv

class CombinedStepTest(EscData):
    def __init__(self, esc_data):
        super().__init__(esc_data.voltage, esc_data.current, esc_data.temp, esc_data.e_rpm, esc_data.t_duty,
                         esc_data.m_duty, esc_data.phase_current, esc_data.pwr, esc_data.stat_1, esc_data.stat_2,esc_data.serial_number)
        self.zero_crossing=[]
        def start_end_crop(self):
            for i in range(len(self.timestamp)):
                if self.timestamp[i] == 0:
                    del self.timestamp[:i]
                    del self.voltage[:i]
                    del self.current[:i]
                    del self.temp[:i]
                    del self.e_rpm[:i]
                    del self.t_duty[:i]
                    del self.m_duty[:i]
                    del self.phase_current[:i]
                    del self.pwr[:i]
                    del self.stat_1[:i]
                    del self.stat_2[:i]
                    break
                else:
                    pass
            for i in reversed(range(len(self.timestamp))):
                if self.timestamp[i] == 0:
                    del self.timestamp[i:]
                    del self.voltage[i:]
                    del self.current[i:]
                    del self.temp[i:]
                    del self.e_rpm[i:]
                    del self.t_duty[i:]
                    del self.m_duty[i:]
                    del self.phase_current[i:]
                    del self.pwr[i:]
                    del self.stat_1[i:]
                    del self.stat_2[i:]
                    break
                else:
                    pass

        def compute_rpm(self, var=23):
            return np.array(self.e_rpm) / var

        def find_zero_crossing(self):
            start_index=[]
            end_index=[]
            for i in range(1,len(self.timestamp)):
                if self.t_duty[i] == 0 & self.t_duty[i-1] != 0:
                    start_index.append(self.timestamp[i])
                elif self.t_duty[i] != 0 & self.t_duty[i-1] == 0:
                    end_index.append(self.timestamp[i])
                else:
                    pass
            for i in range(len(start_index)):
                self.zero_crossing.append((start_index[i],end_index[i]))


class StepTest(EscData):
    def __init__(self, esc_data):
        super().__init__(esc_data.voltage, esc_data.current, esc_data.temp, esc_data.e_rpm, esc_data.t_duty,
                         esc_data.m_duty, esc_data.phase_current, esc_data.pwr, esc_data.stat_1, esc_data.stat_2,esc_data.serial_number)
        self.rpm = self.compute_rpm()
        self.t_duty.insert(0,0)
        self.synchronize_steps(self.detect_step_commands())
        self.crop_data()

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

