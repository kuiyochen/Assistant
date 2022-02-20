# import os
# os.system('control.exe Inetcpl.cpl')

################# 中英檢測 不成功 ##############
# import ctypes
# import win32api
# # https://stackoverflow.com/questions/42047253/how-to-detect-current-keyboard-language-in-python
# # For debugging Windows error codes in the current thread
# user32 = ctypes.WinDLL('user32', use_last_error=True)
# curr_window = user32.GetForegroundWindow()
# thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
# # Made up of 0xAAABBBB, AAA = HKL (handle object) & BBBB = language ID
# klid = user32.GetKeyboardLayout(thread_id)
# # Language ID -> low 10 bits, Sub-langua    ge ID -> high 6 bits
# # Extract language ID from KLID
# lid = klid & (2**16 - 1)
# # Convert language ID from decimal to hexadecimal
# lid_hex = hex(lid)
# print(lid_hex)

# https://blog.csdn.net/weixin_43035074/article/details/112567510
# http://timgolden.me.uk/pywin32-docs/contents.html

# klid = win32api.GetKeyboardLayoutList()[0]
# print(klid)
# KeyboardState = win32api.GetKeyboardState()
# print(int.from_bytes(KeyboardState, "little"))
# print(KeyboardState)
# imm32 = ctypes.WinDLL('imm32', use_last_error=True)
# b = imm32.ImmGetDescriptionA(klid, 255)
# print(b)

def input_mode_detect(): # 中英檢測
    import PIL
    import PIL.ImageGrab
    import cv2
    import numpy as np
    im = PIL.ImageGrab.grab()
    image = np.asarray(im)
    # image = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2GRAY)
    clip = [1040, 1070, 1735, 1760]
    image = image[clip[0]:clip[1], clip[2]:clip[3]]
    # cv2.namedWindow("image")
    # cv2.imshow("image", image)
    clip_image = image[5:10, 5:10]
    clip_image = cv2.cvtColor(clip_image, cv2.COLOR_RGB2GRAY)
    # clip_image = cv2.Canny(clip_image, 30, 150)
    input_mode = "英" if (clip_image > 100).any() else "中"
    # cv2.namedWindow("clip_image")
    # cv2.imshow("clip_image", clip_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return input_mode
# print(input_mode_detect())


import keyboard
import threading
import time
class language_switch(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.RUN = True
    def run(self):
        self.th = []
        class keyboard_recording_thread(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self._stop_event = threading.Event()
            def run(self):
                keyboard.start_recording()
            def stop(self):
                keyboard.stop_recording()
                self._stop_event.set()
            def stopped(self):
                return self._stop_event.is_set()

        self.th.append(keyboard_recording_thread())
        self.th[0].start()

        alt_down = keyboard.KeyboardEvent(event_type = 'down', scan_code = 56, name='alt', time=1.0, device=None, modifiers=None, is_keypad=False)
        alt_up = keyboard.KeyboardEvent(event_type = 'up', scan_code = 56, name='alt', time=1.001, device=None, modifiers=None, is_keypad=False)
        ctrl_down = keyboard.KeyboardEvent(event_type = 'down', scan_code = 29, name='ctrl', time=1.0, device=None, modifiers=None, is_keypad=False)
        ctrl_up = keyboard.KeyboardEvent(event_type = 'up', scan_code = 29, name='ctrl', time=1.001, device=None, modifiers=None, is_keypad=False)
        shift_down = keyboard.KeyboardEvent(event_type = 'down', scan_code = 42, name='shift', time=1.0, device=None, modifiers=None, is_keypad=False)
        shift_up = keyboard.KeyboardEvent(event_type = 'up', scan_code = 42, name='shift', time=1.001, device=None, modifiers=None, is_keypad=False)
        esc_down = keyboard.KeyboardEvent(event_type = 'down', scan_code = 1, name='esc', time=1.0, device=None, modifiers=None, is_keypad=False)
        esc_up = keyboard.KeyboardEvent(event_type = 'up', scan_code = 1, name='esc', time=1.001, device=None, modifiers=None, is_keypad=False)
        delete_down = keyboard.KeyboardEvent(event_type = 'down', scan_code = 83, name='delete', time=1.0, device=None, modifiers=None, is_keypad=False)
        delete_up = keyboard.KeyboardEvent(event_type = 'up', scan_code = 83, name='delete', time=1.001, device=None, modifiers=None, is_keypad=False)
        Z_down = keyboard.KeyboardEvent(event_type = 'down', scan_code = 44, name='Z', time=1.0, device=None, modifiers=None, is_keypad=False)
        Z_up = keyboard.KeyboardEvent(event_type = 'up', scan_code = 44, name='Z', time=1.001, device=None, modifiers=None, is_keypad=False)
        # j = 0

        DETECTING_TIMEOUT_THRESHOLD = 2.
        while self.RUN:
            if keyboard.read_key() == "insert":
                if len(self.th) > 1:
                    for i in range(len(self.th))[::-1][1:]:
                        if self.th[i].stopped():
                            del self.th[i]
                # https://github.com/boppreh/keyboard/blob/master/keyboard/__init__.py
                recorded_events_queue, hooked = keyboard._recording
                recorded = list(recorded_events_queue.queue).copy()
                if len(recorded):
                    if recorded[-1].is_keypad:
                        continue
                self.th[-1].stop()
                # print(recorded[0].__dict__)
                # print(recorded)
                # break

                mode = input_mode_detect()
                if mode == "中": # 用esc消除中文輸入法
                    # keyboard.play([delete_down, delete_up])
                    # time.sleep(0.5)
                    # for i in range(len(recorded) // 4 + 1):
                    #     keyboard.play([esc_down, esc_up])
                    #     time.sleep(0.001)
                    1
                    print("中文輸入")
                else:
                    # keyboard.play([alt_down, ])
                    # time.sleep(0.001)
                    # keyboard.play([ctrl_down, ])
                    # time.sleep(0.001)
                    # keyboard.play([shift_down, ])
                    # time.sleep(0.001)
                    # keyboard.play([Z_down, ])
                    # time.sleep(0.2)
                    # keyboard.play([Z_up, ])
                    # time.sleep(0.001)
                    # keyboard.play([ctrl_up, ])
                    # time.sleep(0.001)
                    # keyboard.play([shift_up, ])
                    # time.sleep(0.001)
                    # keyboard.play([alt_up, ])
                    # time.sleep(0.001)
                    self.th.append(keyboard_recording_thread()) # 重新錄製
                    time.sleep(0.5)
                    self.th[-1].start()
                    continue

                # while input_mode_detect() == "中":
                keyboard.play([shift_down, shift_up]) # 切換輸入法
                time.sleep(0.1)

                if recorded[-1].name == "insert":
                    recorded = recorded[:-1]
                add = 0
                for i in range(len(recorded))[::-1]:
                    print(recorded[i].name)
                    if recorded[i].name not in ["shift", "home", "end", \
                        "left", "right", "up", "down", \
                        "delete", "backspace", "esc"]:
                        break
                    # else:
                    #     if recorded[-1].event_type == "up":
                    #         add += 1
                    #     else:
                    #         add -= 1
                add = max(add, 0) + 1
                recorded = recorded[:i + add]

                if len(recorded):
                    t = recorded[-1].time
                    for i in range(len(recorded))[::-1][1:]: # 移除時間過久的
                        dt = t - recorded[i].time
                        t = recorded[i].time
                        if dt > DETECTING_TIMEOUT_THRESHOLD:
                            recorded = recorded[i + 1:]
                            break

                    if len(recorded) // 2 > 30: # 保護機制
                        keyboard.play([shift_down, ])
                        time.sleep(0.001)
                        keyboard.play([Z_down, Z_up])
                        time.sleep(0.001)
                        keyboard.play([shift_up, ])
                    else:
                        for i in range(len(recorded)): # 加速自動 key in
                            recorded[i].time = 1. + 0.001 * i

                        if len(recorded):
                            keyboard.play(recorded)

                self.th.append(keyboard_recording_thread()) # 重新錄製
                time.sleep(0.5)
                self.th[-1].start()
                # break
            # print(j)
            # j = j+1

    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()

import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
# https://gist.github.com/for-l00p/3e33305f948659313127632ad04b4311
class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        def iconFromBase64(base64):
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(base64))
            icon = QIcon(pixmap)
            return icon
        self.trayIcon = QSystemTrayIcon(iconFromBase64(
            b"iVBORw0KGgoAAAANSUhEUgAAADwAAAA8CAIAAAC1nk4lAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAAiSURBVGhD7cGBAAAAAMOg+VNf4AhVAAAAAAAAAAAAAHDVACpsAAEYhy5EAAAAAElFTkSuQmCC"
            ), self)
        self.trayIcon.activated.connect(self.onTrayIconActivated)
        self.trayIcon.show()
        self.disambiguateTimer = QTimer(self)
        self.disambiguateTimer.setSingleShot(True)
        self.disambiguateTimer.timeout.connect(
                self.disambiguateTimerTimeout)
        self.language_switch = language_switch()
        self.language_switch.start()

    def onTrayIconActivated(self, reason):
        print("onTrayIconActivated:", reason)
        if reason == QSystemTrayIcon.Trigger:
            self.disambiguateTimer.start(qApp.doubleClickInterval())
        elif reason == QSystemTrayIcon.DoubleClick:
            self.disambiguateTimer.stop()
            # print("Tray icon double clicked")
            self.language_switch.RUN = False
            for th in self.language_switch.th:
                try:
                    th.stop()
                except:
                    pass
            for th in self.language_switch.th[::-1]:
                del th
            self.language_switch.stop()
            del self.language_switch
            sys.exit()

    def disambiguateTimerTimeout(self):
        print("Tray icon single clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    # w.show()
    sys.exit(app.exec_())
