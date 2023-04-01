import machine
import math

class MPU6050():
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.start()
        self.i2c.writeto(self.addr, bytearray([107, 0]))
        self.i2c.stop()

    def get_raw_values(self):
        self.i2c.start()
        a = self.i2c.readfrom_mem(self.addr, 0x3B, 14)
        self.i2c.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767
    def get_Angle(self):  # 计算三轴倾角         
        # raw_ints = self.get_raw_values()
        value = self.get_values()
        angle = {}
        #angle['X_Angle']  = acos(self.bytes_toint(raw_ints[0], raw_ints[1]) / 16384.0) * 57.29577
        #angle['Y_Angle']  = acos(self.bytes_toint(raw_ints[2], raw_ints[3]) / 16384.0) * 57.29577
        #angle['Z_Angle']  = acos(self.bytes_toint(raw_ints[4], raw_ints[5]) / 16384.0) * 57.29577
        # X轴
        if -1 <= (value['AcX']/16384.0) <= 1:
            if value['AcZ'] > 0:
                angle['X_Angle'] = math.acos(value['AcX']/16384.0)* 57.29577
            else:
                angle['X_Angle'] = -math.acos(value['AcX']/16384.0)* 57.29577
        else:
            angle['X_Angle'] = 180
        # Y轴
        if -1 <= (value['AcY']/16384.0) <= 1:
            if value['AcZ'] > 0:
                angle['Y_Angle'] = math.acos(value['AcY']/16384.0)* 57.29577
            else:
                angle['Y_Angle'] = -math.acos(value['AcY']/16384.0)* 57.29577
        else:
            angle['Y_Angle'] = 180
        # Z轴得用加速度积分
        
        return angle

