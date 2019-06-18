from machine import I2C
import utime
import struct

class SCD30:

    class NotFoundException(Exception):
        pass

    class CRCException(Exception):
        pass

    START_CONT_MEASURE = 0x0010
    STOP_CONT_MEASURE = 0x0104
    SET_MEASURE_INTERVAL = 0x4600
    GET_STATUS_READY = 0x0202
    READ_MEASUREMENT = 0x0300
    SET_ASC = 0x5306
    SET_FRC = 0x5204
    SET_TEMP_OFFSET = 0x5403
    SET_ALT_COMP = 0x5102
    GET_FIRMWARE_VER = 0xd100
    SOFT_RESET = 0xd304

    CLOCK_TIME_US = 10

    # Generated using
    # crc_table = []
    # for crc in range(256):
    #     for crc_bit in range(8):
    #         if crc & 0x80:
    #             crc = (crc << 1) ^ CRC8_POLYNOMIAL;
    #         else:
    #             crc = (crc << 1);
    #         crc = crc%256
    #     crc_table.append(crc)

    CRC_TABLE = [
        0, 49, 98, 83, 196, 245, 166, 151, 185, 136, 219, 234, 125, 76, 31, 46,
        67, 114, 33, 16, 135, 182, 229, 212, 250, 203, 152, 169, 62, 15, 92, 109,
        134, 183, 228, 213, 66, 115, 32, 17, 63, 14, 93, 108, 251, 202, 153, 168,
        197, 244, 167, 150, 1, 48, 99, 82, 124, 77, 30, 47, 184, 137, 218, 235,
        61, 12, 95, 110, 249, 200, 155, 170, 132, 181, 230, 215, 64, 113, 34, 19,
        126, 79, 28, 45, 186, 139, 216, 233, 199, 246, 165, 148, 3, 50, 97, 80,
        187, 138, 217, 232, 127, 78, 29, 44, 2, 51, 96, 81, 198, 247, 164, 149,
        248, 201, 154, 171, 60, 13, 94, 111, 65, 112, 35, 18, 133, 180, 231, 214,
        122, 75, 24, 41, 190, 143, 220, 237, 195, 242, 161, 144, 7, 54, 101, 84,
        57, 8, 91, 106, 253, 204, 159, 174, 128, 177, 226, 211, 68, 117, 38, 23,
        252, 205, 158, 175, 56, 9, 90, 107, 69, 116, 39, 22, 129, 176, 227, 210,
        191, 142, 221, 236, 123, 74, 25, 40, 6, 55, 100, 85, 194, 243, 160, 145,
        71, 118, 37, 20, 131, 178, 225, 208, 254, 207, 156, 173, 58, 11, 88, 105,
        4, 53, 102, 87, 192, 241, 162, 147, 189, 140, 223, 238, 121, 72, 27, 42,
        193, 240, 163, 146, 5, 52, 103, 86, 120, 73, 26, 43, 188, 141, 222, 239,
        130, 179, 224, 209, 70, 119, 36, 21, 59, 10, 89, 104, 255, 206, 157, 172
        ]

    def __init__(self, i2c, addr):
        self.i2c = i2c
        self.addr = addr
        if not addr in i2c.scan():
            raise self.NotFoundException

    def get_firmware_version(self):
            ver = self.__read_bytes(self.GET_FIRMWARE_VER, 3)
            self.__check_crc(ver)
            return struct.unpack('BB', ver)

    def __read_bytes(self, cmd, count):
        return self.i2c.readfrom_mem(self.addr, cmd, count, addrsize=16)

    def __check_crc(self, arr):
        assert (len(arr) == 3)
        if self.__crc(arr[0], arr[1]) != arr[2]:
            raise self.CRCException

    def __crc(self, msb, lsb):
        crc = 0xff
        crc ^= msb
        crc = self.CRC_TABLE[crc]
        if lsb is not None:
            crc ^= lsb
            crc = self.CRC_TABLE[crc]
        return crc

