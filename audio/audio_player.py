import sys
import os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
import json


from urllib import request
from PyQt5.Qt import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QSlider, QListWidget, QWidget, QHBoxLayout, \
    QVBoxLayout, QDesktopWidget


class MediaPlayer(QWidget):

    # 初始化
    def __init__(self):
        super(MediaPlayer, self).__init__()
        self.setWindowTitle('播放器')
        # 先注册一个媒体播放器
        self.player = QMediaPlayer(self)
        # 注册其他控件
        self.volume_slider = QSlider(self)
        self.volume_save = 0
        self.player.setVolume(36)
        # 进度条
        self.progress_slider = QSlider(self)
        self.time_stamp = QLabel(self)
        # 按钮(PushButton)有，播放(暂停) 上一首，下一首 ，播放模式
        self.preview_btn = QPushButton(self)
        # 播放按钮要切换播放与暂停
        self.play_pause_btn = QPushButton(self)
        self.next_btn = QPushButton(self)
        self.play_mode = QPushButton()
        self.get_music = QPushButton('云音乐')
        self.sound_btn = QPushButton(self)

        # 播放列表
        self.mediaList = QMediaPlaylist(self)
        self.play_list = QListWidget(self)

        self.songs_list = []
        self.songs_formats = ['mp3', 'm4a', 'flac', 'wav', 'ogg']

        # 布局注册
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()

        self.widget_init()
        self.layout_init()
        self.signal_init()
        self.center()

    '''控件初始化'''
    def widget_init(self):

        self.time_stamp.setText('--/--')
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(36)
        self.volume_slider.setOrientation(Qt.Horizontal)
        self.progress_slider.setEnabled(False)
        self.progress_slider.setOrientation(Qt.Horizontal)
        self.sound_btn.setIcon(QIcon('../icon_font/sound_on.png'))
        self.next_btn.setIcon(QIcon(r'..\icon\next.png'))
        self.play_pause_btn.setIcon(QIcon(r'..\icon\play.png'))
        self.preview_btn.setIcon(QIcon(r'..\icon\prev.png'))
        self.play_mode.setIcon(QIcon('../icon_font/list_down.png'))
        self.sound_btn.setIcon(QIcon(r'..\icon_font\sound_on.png'))

        self.player.setPlaylist(self.mediaList)
        self.mediaList.setPlaybackMode(QMediaPlaylist.Sequential)


    # 布局初始化
    def layout_init(self):
        self.h1_layout.addWidget(self.progress_slider)  # 5
        self.h1_layout.addWidget(self.time_stamp)
        self.h2_layout.addWidget(self.preview_btn)
        self.h2_layout.addWidget(self.play_pause_btn)
        self.h2_layout.addWidget(self.next_btn)
        self.h2_layout.addWidget(self.sound_btn)
        self.h2_layout.addWidget(self.volume_slider)
        self.h2_layout.addWidget(self.play_mode)
        self.h2_layout.addWidget(self.get_music)

        self.all_v_layout.addLayout(self.h1_layout)
        self.all_v_layout.addWidget(self.play_list)
        self.all_v_layout.addLayout(self.h2_layout)

        self.all_v_layout.setSizeConstraint(QVBoxLayout.SetFixedSize)  # 6

        self.setLayout(self.all_v_layout)

    # 创建信号函数，连接槽函数
    def signal_init(self):
        #
        self.preview_btn.clicked.connect(lambda: self.slot_func(self.preview_btn))
        self.play_pause_btn.clicked.connect(lambda: self.slot_func(self.play_pause_btn))
        self.next_btn.clicked.connect(lambda: self.slot_func(self.next_btn))
        self.play_mode.clicked.connect(lambda: self.slot_func(self.play_mode))
        self.sound_btn.clicked.connect(lambda: self.slot_func(self.sound_btn))
        # 获取云音乐函数
        self.get_music.clicked.connect(self.get_music_func)
        # 播放器音量控制
        self.volume_slider.valueChanged.connect(self.volume_slider_func)
        self.play_list.doubleClicked.connect(self.play_list_func)
        self.player.durationChanged.connect(self.get_progress_func)
        self.player.positionChanged.connect(self.get_position_func)
        self.progress_slider.sliderMoved.connect(self.update_position_func)

    # 建立槽函数
    def slot_func(self, btn):

        if btn == self.play_pause_btn:
            if self.player.state() == 1:
                self.player.pause()
                self.play_pause_btn.setIcon(QIcon(r'G:\python3\PyQt_Study\icon\play.png'))
            else:
                self.player.play()
                self.play_pause_btn.setIcon(QIcon(r'G:\python3\PyQt_Study\icon\pause.png'))
        #下一首
        elif btn == self.next_btn:
            # 如果点击下一个按钮时为最后一首歌
            if self.mediaList.currentIndex() == self.mediaList.mediaCount() - 1:
                self.mediaList.setCurrentIndex(0)
                self.play_list.setCurrentRow(0)
            else:
                # print(self.player.state())
                if self.player.state() == 1:
                    self.play_list.setCurrentRow(self.mediaList.currentIndex() + 1)
                    self.mediaList.next()
                    self.play_pause_btn.setIcon(QIcon(r'G:\python3\PyQt_Study\icon\pause.png'))
        # 上一首
        elif btn == self.preview_btn:
            if self.mediaList.currentIndex() == 0:
                self.mediaList.setCurrentIndex(self.mediaList.mediaCount() -1)
            else:
                if self.player.state() == 1:
                    self.mediaList.previous()
                    self.play_pause_btn.setIcon(QIcon(r'G:\python3\PyQt_Study\icon\pause.png'))
        # 播放模式
        elif btn == self.play_mode:
            # 根据播放模式切换
            if self.mediaList.playbackMode() == 2:
                self.mediaList.setPlaybackMode(QMediaPlaylist.Loop)
                self.play_mode.setIcon(QIcon(r'G:\python3\PyQt_Study\icon_font\loop.png'))

            elif self.mediaList.playbackMode() == 3:
                self.mediaList.setPlaybackMode(QMediaPlaylist.Random)
                self.play_mode.setIcon(QIcon(r'..\icon_font\random.png'))

            elif self.mediaList.playbackMode() == 4:
                self.mediaList.setPlaybackMode(QMediaPlaylist.Sequential)
                self.play_mode.setIcon(QIcon(r'..\icon_font\list_loop.png'))
        # 声音按钮控制
        elif btn == self.sound_btn:
            if self.player.isMuted():
                # self.sound_btn.setIcon('')
                print("1", self.player.isMuted())
                self.volume_slider.setValue(self.volume_save)
                self.player.setMuted(False)
                self.sound_btn.setIcon(QIcon(r'G:\python3\PyQt_Study\icon_font\sound_on.png'))
            else:
                print("2", self.player.isMuted())
                self.player.setMuted(True)
                self.volume_save = self.volume_slider.value()
                self.volume_slider.setValue(0)
                self.sound_btn.setIcon(QIcon(r'G:\python3\PyQt_Study\icon_font\sound_off.png'))

    # 窗口居中
    def center(self):

        qr = self.frameGeometry()  # 获得主窗口的一个矩形特定几何图形。这包含了窗口的框架。
        cp = QDesktopWidget().availableGeometry().center()  # 算出相对于显示器的绝对值。
        # 并且从这个绝对值中，我们获得了屏幕中心点。
        qr.moveCenter(cp)  # 矩形已经设置好了它的宽和高。现在我们把矩形的中心设置到屏幕的中间去。
        # 矩形的大小并不会改变。
        self.move(qr.topLeft())  # 移动了应用窗口的左上方的点到qr矩形的左上方的点，因此居中显示在我们的屏幕上。

    # 获取音乐槽函数
    def get_music_func(self):
        self.mediaList.clear()
        url = 'http://47.108.93.231:8000/cloudMusic'
        response = request.urlopen(url).read()
        # print(json.loads(response), type(json.loads(response)))
        # 读取数据库信息
        # print(json.loads(response))
        msg = json.loads(response)['msg']
        for song in msg:
            if song['url'].split('.')[-1] in self.songs_formats:
                # self.songs_list.append([song, song['url']])
                self.mediaList.addMedia(QMediaContent(QUrl(song['url'])))
                self.play_list.addItem(song['name'])
        self.play_list.setCurrentRow(0)
        # print(self.mediaList.mediaCount())
        if self.songs_list:
            self.cur_playing_song = self.songs_list[self.play_list.currentRow()][-1]

    def volume_slider_func(self, val):
        self.player.setVolume(val)
        # if val == 0:
        #     self.sound_btn.setICon(QIcon(r'G:\python3\PyQt_Study\icon\sound.png'))
        # else:
        #     self.sound_btn.setIcon(QIcon(r'G:\python3\PyQt_Study\icon\sound.png'))

    # 播放列表双击函数
    def play_list_func(self):
        self.mediaList.setCurrentIndex(self.play_list.currentRow())
        self.player.play()
        self.play_pause_btn.setIcon(QIcon(r'G:\python3\PyQt_Study\icon\pause.png'))


    def get_progress_func(self, d):
        # 连接的函数，传入参数的d为毫秒。所以做一个时间变换
        self.progress_slider.setRange(0, d)
        self.progress_slider.setEnabled(True)
        self.get_time_func(d)

    # 时间控制函数，每次调用改变滑条位置，以及时间减少
    def get_time_func(self, d):

        seconds = int(d / 1000)
        minutes = int(seconds / 60)
        seconds -= minutes * 60
        # print("%s分" %minutes, "%s秒" %seconds)
        if minutes == 0 and seconds == 0:
            self.time_stamp.setText("--/--")
            self.play_pause_btn.setIcon(QIcon(r'G:\python3\PyQt_Study\icon\play.png'))

        else:
            self.time_stamp.setText("{}:{}".format(minutes, seconds))


    def get_position_func(self, p):
        self.progress_slider.setValue(p)
        self.get_time_func(self.progress_slider.maximum() - self.progress_slider.value())

    # 当且仅当用户手动改变滑条位置时
    def update_position_func(self, v):
        self.player.setPosition(v)
        d = self.progress_slider.maximum() - v
        self.get_time_func(d)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    play = MediaPlayer()
    play.show()
    sys.exit(app.exec_())