# Robot control script

import curses

import serial
from serial import SerialException

def Display():
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(1)

    stdscr.addstr(0,2,"Status: %s" % ser.Status)
    stdscr.addstr(2,2,"controls:\n\tUP    - move forward.\n\tRIGHT - turn right.\n\tLEFT  - turn left.\n\tDOWN  - STOP.")
    stdscr.addstr(7,0,"\tQ     - quit.")
    stdscr.refresh()
    #ser.open_port()
    key = stdscr.getch()
    while key != ord('q'): 
        key = stdscr.getch()
        #stdscr.addch(20,25,key)
        stdscr.addstr(0,2,"Status: %s" % ser.Status)
        stdscr.refresh()
        if key == curses.KEY_UP: 
            ser.Status = ser.Write('1')
        elif key == curses.KEY_DOWN: 
            ser.Status = ser.Write('0')
        elif key == curses.KEY_RIGHT: 
            ser.Status = ser.Write('2')
        elif key == curses.KEY_LEFT: 
            ser.Status = ser.Write('3')
        if ~ser.Connected:
            ser.open_port()
    ser.close_port()
    curses.endwin()
    
class Serial_Man(object):
    def __init__(self, PortName, Baudrate):
        self.PortName = PortName
        self.Baudrate = Baudrate
        self.Port = 0
        self.Connected = False
        self.Status = "not Connected"

    def open_port(self):
        try:
            self.Port = serial.Serial(self.PortName, self.Baudrate)
        except IOError:
            self.Status = "Openning Port Error"
            #raise SerialException("could not open port \"%s\": check the device connection." % (self.PortName))
        else:
            self.Status = "Connected          "
            self.Connected = True
        return self.Status

    def Write(self, n):
        try:
            self.Port.write(n)
            self.Status = "Connected !        "
        except Exception:
            self.Status = "Write Error %s     ",Exception
            #raise SerialException("could not write to port \"%s\": check the device connection." % (self.PortName))
        else:
            return self.Status

    def close_port(self):
        if(self.Connected):
            self.Port.close()
        else:
            pass

ser = Serial_Man("/dev/ttyACM0", 9600)
Display()
