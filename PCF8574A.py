from RPi import GPIO
import time
import subprocess

class LCDScreen():

    def __init__(self, isVierBits=False, E=21, RS=20, DB7=22, DB6=5, DB5=6, DB4=27, DB3=17, DB2=25, DB1=12, DB0=16):
        # BCM mode gebruiken
        GPIO.setmode(GPIO.BCM)

        self.__shortDelay = 0.01
        self.__longDelay = 0.5
        self.__isVierBits = isVierBits
        self.__E = E
        self.__RS = RS
        self.__DB7 = DB7
        self.__DB6 = DB6
        self.__DB5 = DB5
        self.__DB4 = DB4
        self.__DB3 = DB3
        self.__DB2 = DB2
        self.__DB1 = DB1
        self.__DB0 = DB0

        GPIO.setup(self.__E, GPIO.OUT)
        GPIO.setup(self.__RS, GPIO.OUT)

        GPIO.setup(self.__DB0, GPIO.OUT)
        GPIO.setup(self.__DB1, GPIO.OUT)
        GPIO.setup(self.__DB2, GPIO.OUT)
        GPIO.setup(self.__DB3, GPIO.OUT)
        GPIO.setup(self.__DB4, GPIO.OUT)
        GPIO.setup(self.__DB5, GPIO.OUT)
        GPIO.setup(self.__DB6, GPIO.OUT)
        GPIO.setup(self.__DB7, GPIO.OUT)

        self.__dataBits = [self.__DB0, self.__DB1, self.__DB2, self.__DB3, self.__DB4, self.__DB5, self.__DB6,
                           self.__DB7]

        # standaard hoog zetten
        GPIO.output(self.__E, GPIO.HIGH)
        GPIO.output(self.__RS, GPIO.HIGH)

    def send_instruction(self, value):
        GPIO.output(self.__E, 1)
        GPIO.output(self.__RS, 0)
        self.set_data_value(value)
        GPIO.output(self.__E, 0)
        time.sleep(self.__shortDelay)

    def __send_character(self, value):
        GPIO.output(self.__E, 1)
        GPIO.output(self.__RS, 1)
        self.set_data_value(value)
        GPIO.output(self.__E, 0)
        time.sleep(self.__shortDelay)

    def set_data_value(self, value):
        mask = 0x01
        for pin in self.__dataBits:
            if (value & mask == 0):
                GPIO.output(pin, 0)
            else:
                GPIO.output(pin, 1)
            mask = mask << 1

    def LCD_init(self):
        self.send_instruction(0x3B)  # function instruction
        self.send_instruction(0x01)  # clear display
        self.send_instruction(0xF)  # display on
        self.send_instruction(0x3)  # cursor home

    def send_line(self, line):

        teller = 0
        for letter in line:
            if (teller < 16):
                self.__send_character(ord(letter))
                teller += 1

            elif (teller == 16):
                teller += 1
                self.second_row()
                self.__send_character(ord(letter))

            elif (teller >= 16):
                teller += 1
                self.__send_character(ord(letter))

    def second_row(self):
        self.send_instruction(0xC0)

    def reset_LCD(self):
        self.send_instruction(0x01)  # clear display

    def displayOn(self):
        self.send_instruction(0xF)  # display on

    def statusip1(self):
        # adressen ophalen van de pi
        ips = subprocess.check_output(['hostname', '--all-ip-addresses'])
        ips = ips.decode()
        ips = ips.split(" ")
        # \n verwijderen
        del ips[-1]
        # ips = str(ips)


        if (ips[0] == '169.254.10.1'):
            self.send_line(ips[1])
        else:
            self.send_line(ips[0])
