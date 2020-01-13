
import os
import sys
import time
import serial
from datetime import datetime
try:
	import Tkinter
	from Queue import *
	from Tkinter import *
	import tkMessageBox
except ImportError:
	import tkinter
	from queue import *
	from tkinter import *
	import tkinter.messagebox as tkMessageBox

PRGPATH=os.path.abspath(os.path.dirname(__file__))
sys.path.append(PRGPATH)
sys.path.append(os.path.join(PRGPATH, 'lib'))
sys.path.append(os.path.join(PRGPATH, 'plugins'))
sys.path.append(os.path.join(PRGPATH, 'controllers'))

# Load configuration before anything else
# and if needed replace the  translate function _()
# before any string is initialized
import Utils
Utils.loadConfiguration()

import rexx
import tkExtra
from lib import bFileDialog



# Load configuration before anything else
# and if needed replace the  translate function _()
# before any string is initialized
import Utils
Utils.loadConfiguration()
from Sender import Sender, NOT_CONNECTED, STATECOLOR, STATECOLORDEF
from CNC import WAIT, CNC, GCode

FILETYPES = [	(_("All accepted"), ("*.ngc","*.cnc","*.nc", "*.tap", "*.gcode", "*.dxf", "*.probe", "*.orient", "*.stl", "*.svg")),
		(_("G-Code"),("*.ngc","*.cnc","*.nc", "*.tap", "*.gcode")),
		(_("G-Code clean"),("*.txt")),
		("DXF",       "*.dxf"),
		("SVG",       "*.svg"),
		(_("Probe"),  ("*.probe", "*.xyz")),
		(_("Orient"), "*.orient"),
		("STL",       "*.stl"),
		(_("All"),    "*")]

class GcodeSender(Sender):
    def __init__(self):
        Sender.__init__(self)

    # -----------------------------------------------------------------------
    # Load a file into editor
    # -----------------------------------------------------------------------
    def load(self, filename, autoloaded=False):
        fn, ext = os.path.splitext(filename)
        if ext == ".probe":
            pass
        else:
            if not self.gcode.probe.isEmpty():
               self.gcode.probe.init()

        self.setStatus(_("Loading: %s ...") % (filename), True)
        Sender.load(self, filename)

        if ext == ".probe":
            self.autolevel.setValues()
            self.event_generate("<<DrawProbe>>")

        elif ext == ".orient":
            self.event_generate("<<DrawOrient>>")
            self.event_generate("<<OrientSelect>>", data=0)
            self.event_generate("<<OrientUpdate>>")

        else:
            print("update canvas")

        if autoloaded:
            self.setStatus(_("'%s' reloaded at '%s'") % (filename, str(datetime.now())))
        else:
            self.setStatus(_("'%s' loaded") % (filename))

    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Send enabled gcode file to the CNC machine
    # -----------------------------------------------------------------------
    def run(self, lines=None):
        self.cleanAfter = True  # Clean when this operation stops
        print("Will clean after this operation")

        if self.serial is None and not CNC.developer:
            print("Serial Error Serial is not connected")
            return
        if self.running:
            if self._pause:
                self.resume()
                return
            print("Already running Please stop before")
            return

        # self.editor.selectClear()
        # self.selectionChange()
        print("clear canvas")
        CNC.vars["errline"] = ""

        # the buffer of the machine should be empty?
        self.initRun()
        # self.canvas.clearSelection()
        self._runLines = sys.maxsize  # temporary WARNING this value is used
        # by Sender._serialIO to check if we
        # are still sending or we finished
        self._gcount = 0  # count executed lines
        self._selectI = 0  # last selection pointer in items
        self._paths = None  # temporary
        CNC.vars["running"] = True  # enable running status
        CNC.vars["_OvChanged"] = True  # force a feed change if any
        if self._onStart:
            try:
                os.system(self._onStart)
            except:
                pass

        if lines is None:
            # if not self.gcode.probe.isEmpty() and not self.gcode.probe.zeroed:
            #	tkMessageBox.showerror(_("Probe is not zeroed"),
            #		_("Please ZERO any location of the probe before starting a run"),
            #		parent=self)
            #	return

            # class MyQueue:
            #	def put(self,line):
            #		print ">>>",line
            # self._paths = self.gcode.compile(MyQueue(), self.checkStop)
            # return

            self._paths = self.gcode.compile(self.queue, self.checkStop)
            if self._paths is None:
                self.emptyQueue()
                self.purgeController()
                return
            elif not self._paths:
                self.runEnded()
                print("Empty gcode Not gcode file was loaded")
                return

            # reset colors
            # before = time.time()
            # for ij in self._paths:  # Slow loop
            #     if not ij: continue
            #     path = self.gcode[ij[0]].path(ij[1])
            #     if path:
            #         color = self.canvas.itemcget(path, "fill")
            #         if color != CNCCanvas.ENABLE_COLOR:
            #             self.canvas.itemconfig(
            #                 path,
            #                 width=1,
            #                 fill=CNCCanvas.ENABLE_COLOR)
            #         # Force a periodic update since this loop can take time
            #         if time.time() - before > 0.25:
            #             self.update()
            #             before = time.time()

            # the buffer of the machine should be empty?
            self._runLines = len(self._paths) + 1  # plus the wait
        else:
            n = 1  # including one wait command
            for line in CNC.compile(lines):
                if line is not None:
                    if isinstance(line, str):
                        self.queue.put(line + "\n")
                    else:
                        self.queue.put(line)
                    n += 1
            self._runLines = n  # set it at the end to be sure that all lines are queued
        self.queue.put((WAIT,))  # wait at the end to become idle
        self.setStatus(_("Running..."))

    # -----------------------------------------------------------------------
    def setStatus(self, msg, force_update=False):
        print("status" + msg)

    # -----------------------------------------------------------------------
    # Set a status message from an event
    # -----------------------------------------------------------------------
    def updateStatus(self, event):
        self.setStatus(_(event.data))

    # -----------------------------------------------------------------------
    # An entry function should be called periodically during compiling
    # to check if the Pause or Stop buttons are pressed
    # @return true if the compile has to abort
    # -----------------------------------------------------------------------
    def checkStop(self):
        return False

    # ---------------------------------------------------------------------
    def disable(self):
        print("state disable")

    # -----------------------------------------------------------------------
    def openClose(self, event=None):
        if self.serial is not None:
            self.close()
        else:
            device = ""
            baudrate = 9600
            if self.open(device, baudrate):
                print("打开串口成功")

    # -----------------------------------------------------------------------
    def open(self, device, baudrate):
        try:
            return Sender.open(self, device, baudrate)
        except:
            self.serial = None
            self.thread = None
            print("打开串口失败")
        return False

    # -----------------------------------------------------------------------
    def close(self):
        Sender.close(self)

    def troncellCallback(self):
        toncellTest.callback()

    def loadAndRun(self,filename):
        self._gcount=0
        self._runLines=0
		# self._runLines=0
		# self._runLines=0
        # filename = r'/home/pi/Documents/bCNC-master/'+'sample.gcode'
        filename = r'/home/pi/Documents/bCNC-master/'+filename
        print('filename',filename)
        self.load(filename)
        self.run()


gcodeSender = GcodeSender()
# gcodeSender.open("spy://COM4?color",115200)
gcodeSender.open("hwgrep://USB",115200)

# gcodeSender.load(filename)
# gcodeSender.run()
# print("Press any key to exit.")
# key = input()


# from ControlPage import ControlPage,DROFrame
# DROFrame().setXYZ0()
# gcodeSender.setXYZ0()



import toncellTest
toncellTest.app=gcodeSender
toncellTest.initNum()
toncellTest.initColor()
toncellTest.polling()
toncellTest.initBtn()




