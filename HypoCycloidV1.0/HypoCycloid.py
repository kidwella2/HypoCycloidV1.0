
# # # # # # # # # # # # # # # # # # # # # # # #
# Name: Austin Kidwell
# Version: 1.0
# Date: 9/24/2021
# # # # # # # # # # # # # # # # # # # # # # # #

import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
from PyQt5 import uic, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.Qt import QUrl
import math

mpl.rcParams['animation.ffmpeg_path'] = r'ffmpeg\\bin\\ffmpeg.exe'  # for mp4 save

qtCreatorFile = "HCmenu.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class HypoCycloid(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)            # Ui set-up
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.widgetPlayer)  # widget for video output
        self.widgetPlayer = QVideoWidget()  # Video display widget
        self.player.durationChanged.connect(self.getDuration)       # progress bar
        self.player.positionChanged.connect(self.getPosition)
        self.progressBar.sliderMoved.connect(self.updatePosition)

    def start(self):
        try:
            radius = float(self.lineEditRadius.text())              # get user info
            vbradius = float(self.lineEditVBRadius.text())
            offset = float(self.lineEditOffset.text())
            length = float(self.lineEditLength.text())
            width = float(self.lineEditWidth.text())
            spindles = int(self.lineEditSpindle.text())
        except Exception as e:                                      # block wrong data
            print('No/Wrong Values Entered')
            print('Catch: ', e.__class__)
            return 1
        angle = 150
        vbangle = 150
        self.Cycle(radius, vbradius, offset, length, width, spindles, angle, vbangle)

    def Cycle(self, rad, vbrad, ofs, leng, wid, spin, ang, vbang):  # loop through motion and get values
        x1 = []  # store coordinates in lists
        y1 = []
        x2 = []
        y2 = []
        xo = []
        yo = []
        xw = []
        yw = []
        xl = []
        yl = []
        for i in range(360):        # loop 1 cycle in cartoon feeder
            angle = math.radians(ang)
            x = rad * ((1 - math.tan(angle / 2) ** 2) / (1 + math.tan(angle / 2) ** 2))     # math for values
            y = rad * ((2 * math.tan(angle / 2)) / (1 + math.tan(angle / 2) ** 2))
            print('Angle: ', ang)
            print('x1: ', x, 'y1: ', y)
            x1.append(x)                # set spindle center data
            y1.append(y)
            angle = math.radians(vbang)
            vbx2 = vbrad * ((1 - math.tan(angle / 2) ** 2) / (1 + math.tan(angle / 2) ** 2))
            vby2 = vbrad * ((2 * math.tan(angle / 2)) / (1 + math.tan(angle / 2) ** 2))
            x2.append(vbx2 + x)             # get vacuum cup points
            y2.append(vby2 + y)
            vbang2 = vbang - 90  # angle for offset and width
            vbang3 = vbang + 90  # angle for length
            if vbang2 < 0:  # keeps looping
                vbang2 += 360
            if vbang3 > 360:
                vbang3 -= 360
            angle2 = math.radians(vbang2)
            angle3 = math.radians(vbang3)
            vbxo = ofs * ((1 - math.tan(angle2 / 2) ** 2) / (1 + math.tan(angle2 / 2) ** 2))
            vbyo = ofs * ((2 * math.tan(angle2 / 2)) / (1 + math.tan(angle2 / 2) ** 2))
            xo.append(vbxo + x2[i])  # get offset points
            yo.append(vbyo + y2[i])
            vbxw = (ofs + wid) * ((1 - math.tan(angle2 / 2) ** 2) / (1 + math.tan(angle2 / 2) ** 2))
            vbyw = (ofs + wid) * ((2 * math.tan(angle2 / 2)) / (1 + math.tan(angle2 / 2) ** 2))
            xw.append(vbxw + x2[i])  # get width points
            yw.append(vbyw + y2[i])
            length = leng - ofs
            vbxl = length * ((1 - math.tan(angle3 / 2) ** 2) / (1 + math.tan(angle3 / 2) ** 2))
            vbyl = length * ((2 * math.tan(angle3 / 2)) / (1 + math.tan(angle3 / 2) ** 2))
            xl.append(vbxl + x2[i])  # get length points
            yl.append(vbyl + y2[i])
            print('Vacuum Block Angle: ', vbang)
            print('Vacuum Cup Center: ', x2[i], 'y2: ', y2[i])
            print('Offset x: ', xo[i], 'yo:', yo[i])
            print('Width x: ', xw[i], 'yw:', yw[i])
            print('Length x: ', xl[i], 'yl:', yl[i])
            print()
            if i == 359:                # display data after finished collecting data
                self.Display(x1, y1, x2, y2, xw, yw, xl, yl, spin)
            ang += 1
            vbang -= 2
            if ang > 360:  # keeps angle in bounds
                ang -= 360
            if vbang < 0:  # keeps vacuum block angle in bounds
                vbang += 360

    def Display(self, x1, y1, x2, y2, xw, yw, xl, yl, spin):
        xmin = min(xl)          # used to find bounds for animation
        ymin = min(yl)
        xmax = max(xl)
        ymax = max(yl)
        if xmin > min(xw):
            xmin = min(xw)
        if ymin > min(yw):
            ymin = min(yw)
        if xmax < max(xw):
            xmax = max(xw)
        if ymax < max(yw):
            ymax = max(yw)
        x3, y3 = self.GetSpindle2(x2, y2, spin)

        plt.ioff()                  # turn plot display off
        fig = plt.figure()          # plot

        plt.suptitle("Hypo Cycloid", fontsize=14)  # name and bounds
        plt.plot(xmin, ymin)
        plt.plot(xmax, ymax)

        plt.plot(x1, y1, color='tab:gray')  # set labels and colors for graph/animation
        graph, = plt.plot([], [], '--', color='tab:purple', label='Picking Cup')
        graph2, = plt.plot([], [], '-.', color='r', label='Approaching Cup')
        graph3, = plt.plot([], [], color='g', label='Width')
        graph4, = plt.plot([], [], color='b', label='Length')
        plt.grid(color='#7171C6', linestyle='-', linewidth=.2)  # light grey)
        plt.autoscale(enable=True, axis='both', tight=None)
        plt.gca().set_aspect('equal')
        plt.legend()

        def init():
            return graph, graph2, graph3, graph4,

        def animate(i):  # animation data
            graph.set_data(x2[:i], y2[:i])
            graph2.set_data(x3[:i], y3[:i])
            graph3.set_data(xw[:i], yw[:i])
            graph4.set_data(xl[:i], yl[:i])
            return graph, graph2, graph3, graph4,

        ani = FuncAnimation(fig, animate, frames=120, interval=50, save_count=len(x1),      # animation
                            init_func=init, blit=True)

        f = r"HC.mp4"  # save mp4
        writervideo = animation.FFMpegWriter(fps=40)
        ani.save(f, writer=writervideo)
        # ani.save('HC.gif', writer='PillowWriter')         # save gif

        plt.show()
        plt.close(fig)

    def GetSpindle2(self, x2, y2, spindle):  # crate spindle line behind current one
        x3 = []
        y3 = []
        total = 359
        delay = (total + 1) / spindle
        start = total - delay + 1
        for i in range(len(x2)):
            temp = int(i + start)
            if temp > total:
                temp -= total
            x3.append(x2[temp])
            y3.append(y2[temp])
        return x3, y3

    def cancel(self):
        self.close()

    def load(self):
        self.setupUi(self)      # set-up to update
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.widgetPlayer)

        self.player.durationChanged.connect(self.getDuration)  # progress bar
        self.player.positionChanged.connect(self.getPosition)
        self.progressBar.sliderMoved.connect(self.updatePosition)

        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(r'HC.mp4')))  # load and play
        self.player.play()
        app.exec_()             # need to update

    def playvid(self):                  # pause and play video
        if self.player.state() == 1:
            self.player.pause()
        else:
            self.player.play()

    def getDuration(self, d):       # d is total time in ms
        self.progressBar.setRange(0, d)
        self.progressBar.setEnabled(True)
        self.displayTime(d)

    def getPosition(self, p):
        self.progressBar.setValue(p)
        self.displayTime(self.progressBar.maximum() - p)

    def displayTime(self, ms):      # show time and convert from ms
        minutes = int(ms / 60000)
        seconds = int((ms - minutes * 60000) / 1000)
        self.labelTime.setText('{}:{}'.format(minutes, seconds))

    def updatePosition(self, v):
        self.player.setPosition(v)
        self.displayTime(self.progressBar.maximum() - v)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = HypoCycloid()
    window.show()
    sys.exit(app.exec_())
