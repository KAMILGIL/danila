import sys
from PyQt5 import uic
from os.path import expanduser
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont


class TrackSaver:
    def __init(self):
        self.track_list = []
        try:
            self.file = open("tracklist.txt", 'r')
            for i in self.file.readlines():
                self.track_list.append(i[:-2])
        except:
            print(7)
            #self.file = open("tracklist.txt", 'w')

    def add_track(self, url):
        self.track_list.append(url)

    def delete_track(self, i):
        if i < len(self.track_list):
            return None
        del self.track_list[i]
        self.file.close()
        self.file = open("tracklist.txt", 'w')
        for i in self.track_list:
            self.file.write(i + "/n")


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('player.ui', self)
        self.pause = True
        self.time = QTimer()
        self.time.timeout.connect(self.redraw)
        self.pause_button.clicked.connect(self.pause_play)
        self.next_button.clicked.connect(self.nxt)
        self.previous_button.clicked.connect(self.previous)
        self.slider.sliderReleased.connect(self.move)
        self.slider.setMinimum(0)
        self.sliderMaximum = 600
        self.slider.setMaximum(self.sliderMaximum)
        self.lst = []
        self.d = []
        self.update_tracks()
        self.track = 0
        for i in range(len(self.lst)):
            item = QTableWidgetItem('1')
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(i, 0, item)
        self.player = QMediaPlayer()
        self.player.durationChanged.connect(self.duration)
        self.createMenubar()
        self.start()
        self.table.cellClicked.connect(self.func)
    
    def func(self, row, column):
        self.track = self.d.index(self.table.item(row, column).text())
        self.start()
    
    
    
    def update_tracks(self):
        self.table.setColumnCount(1)
        self.table.setRowCount(len(self.lst))
        self.table.setHorizontalHeaderLabels(["tracks"])
        self.table.clicked.connect(self.change)

    def pause_play(self):
        if len(self.lst) == 0:
            return None
        if self.pause:
            self.time.start(1000)
            self.player.play()
        else:
            self.player.pause()
        self.pause = not self.pause

    def start(self):
        self.slider.setValue(0)
        if len(self.lst) > 0:
            self.player.setMedia(self.lst[self.track])
            font = QFont()
            font.setPointSize(16)
            self.label.setFont(font)
            self.label.setText(self.d[self.track])           
            self.player.play()
        if self.pause:
            self.player.pause()
        else:
            self.time.start(1000)

    def closeEvent(self, event):
        # print("exit")
        self.player.stop()

    def createMenubar(self):
        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')
        filemenu.addAction(self.fileOpen())

    def fileOpen(self):
        fileAc = QAction('Open File', self)
        fileAc.setShortcut('Ctrl+O')
        fileAc.setStatusTip('Open File')
        fileAc.triggered.connect(self.openFile)
        return fileAc

    def openFile(self):
        fileChoosen = QFileDialog.getOpenFileUrl(self, 'Open Music File', expanduser('~'), 'Audio (*.mp3 *.ogg *.wav)',
                                                 '*.mp3 *.ogg *.wav')
        if fileChoosen is not None:
            self.lst.append(QMediaContent(fileChoosen[0]))
            self.update_tracks()
            url = fileChoosen[0].url().split('/')[-1][:-4]
            item = QTableWidgetItem(url)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)            
            self.table.setItem(len(self.lst) - 1, 0, item)
            self.d.append(url)

    def duration(self):
        self.sliderMaximum = self.player.duration()
        self.slider.setMaximum(self.sliderMaximum)

    def change(self):
        self.track = self.table.currentRow()
        self.pause_play()

    def nxt(self):
        self.track = (self.track - 1) % len(self.lst)
        self.start()

    def previous(self):
        self.track = (self.track + 1) % len(self.lst)
        self.start()

    def move(self):
        self.player.setPosition(self.slider.value())

    def redraw(self):
        if self.pause:
            return
        a = self.player.position()
        self.label_4.setText(
            str(a // 60000) + ':' + '0' * (2 - len(str((a % 60000) // 1000))) + str((a % 60000) // 1000))
        self.time.start(1000)
        self.slider.setValue(self.slider.value() + 1000)
        if self.slider.value() >= self.sliderMaximum:
            self.nxt()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())