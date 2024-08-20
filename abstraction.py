import copy
import csv
from pathlib import Path

class EscData:
    voltage = []
    current = []
    temp = []
    e_rpm=[]
    t_duty=[]
    m_duty=[]
    phase_current=[]
    pwr=[]
    stat_1=[]
    stat_2=[]
    serial_number=[]
    timestamp = []
    timestamp_len = []

    def __init__(self,voltage,current,temp,e_rpm,t_duty,
                 m_duty,phase_current,pwr,stat_1,stat_2,serial_number,timestamp_len):
        self.voltage = copy.deepcopy(voltage)
        self.current = copy.deepcopy(current)
        self.temp = copy.deepcopy(temp)
        self.e_rpm = copy.deepcopy(e_rpm)
        self.t_duty = copy.deepcopy(t_duty)
        self.m_duty = copy.deepcopy(m_duty)
        self.phase_current = copy.deepcopy(phase_current)
        self.pwr = copy.deepcopy(pwr)
        self.stat_1 = copy.deepcopy(stat_1)
        self.stat_2 = copy.deepcopy(stat_2)
        self.serial_number = copy.deepcopy(serial_number)
        self.timestamp_len = [len(self.voltage),len(self.current),len(self.temp),len(self.e_rpm),len(self.t_duty),len(self.m_duty),\
             len(self.phase_current),len(self.pwr),len(self.stat_1),len(self.stat_2)]
        self.timestamp = self.time_array()

    def time_array(self):
        time=[]
        for i in range(self.timestamp_len[0]):
            time.append(i)
        return time

    def display(self):
        print('voltage:',self.voltage)
        print('current:',self.current)
        print('temp:',self.temp)
        print('e_rpm:',self.e_rpm)
        print('t_duty:',self.t_duty)
        print('m_duty:',self.m_duty)
        print('phase_current:',self.phase_current)
        print('pwr:',self.pwr)
        print('stat_1:',self.stat_1)
        print('stat_2:',self.stat_2)
        print('serial_number:',self.serial_number)
        print('timestamp_len:',self.timestamp_len)
        print('timestamp:',self.timestamp)

    def getVoltage(self):
        return self.voltage
    def getCurrent(self):
        return self.current
    def getTemp(self):
        return self.temp
    def getERPM(self):
        return self.e_rpm
    def getTDuty(self):
        return self.t_duty
    def getMDuty(self):
        return self.m_duty
    def getPhaseCurrent(self):
        return self.phase_current
    def getPwr(self):
        return self.pwr
    def getStat1(self):
        return self.stat_1
    def getStat2(self):
        return self.stat_2
    def getSerialNumber(self):
        return self.serial_number
    def getTimestampLen(self):
        return self.timestamp_len
    def getTimestamp(self):
        return self.timestamp

def take_values_from_csv(fileName):
    rows=[]
    with open( fileName , mode='r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        fieldnames = next(csv_reader)
        for row in csv_reader:
            rows.append(row)
    #    print("total numer of rows: %d"%(csv_reader.line_num))
    serial = fieldnames[len(fieldnames)-1].partition(":")
    serial_int=serial[len(serial)-1]
    serial_int=serial_int.strip()

    v_tmp=[]
    c_tmp=[]
    t_tmp=[]
    erpm_tmp=[]
    trtl_dt=[]
    mt_dt=[]
    phs_c=[]
    pwr_tmp=[]
    s1_t=[]
    s2_t=[]
    time_t =[]

    def clr_temp_arrs():
        v_tmp.clear()
        c_tmp.clear()
        t_tmp.clear()
        erpm_tmp.clear()
        trtl_dt.clear()
        mt_dt.clear()
        phs_c.clear()
        pwr_tmp.clear()
        s1_t.clear()
        time_t.clear()

    for i in range(len(rows)):
        v_tmp.append((float(rows[i][0])))
        c_tmp.append((float(rows[i][1])))
        t_tmp.append((float(rows[i][2])))
        erpm_tmp.append((float(rows[i][3])))
        trtl_dt.append((float(rows[i][4])))
        mt_dt.append((float(rows[i][5])))
        phs_c.append((float(rows[i][6])))
        pwr_tmp.append((float(rows[i][7])))
        s1_t.append((float(rows[i][8])))
        s2_t.append((float(rows[i][9])))
        time_t.append(i)

    objName = EscData(v_tmp,c_tmp,t_tmp,erpm_tmp,trtl_dt,mt_dt,phs_c,pwr_tmp,s1_t,s2_t,serial_int,time_t)

    clr_temp_arrs()
#    objName.display()
    if (objName.timestamp_len[0] == (csv_reader.line_num-1)):
        print("Timestamp numbers are matching along entries. Timestamp Num: TRUE")
    else:
        print("Timestamp numbers are not matching along entries. Timestamp Num: FALSE")

    return objName

