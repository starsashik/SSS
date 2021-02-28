import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMenuBar, QAction


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.coords = [37.622504, 55.753215]
        self.z = 9
        self.map_file = "map.png"
        self.types = ["map", "sat", "sat,skl"]
        self.type = self.types[0]
        self.initUi()

    def initUi(self):
        self.setGeometry(400, 400, 600, 450)
        self.setWindowTitle('Большая задача по Maps API')
        self.setFixedSize(self.size())

        self.map = QLabel("", self)
        self.map.setGeometry(0, 0, 600, 450)
        self.map.setPixmap(self.get_map())

        mainMenu = QMenuBar(self)
        setupMenu = mainMenu.addMenu('Setup')

        # showbtn = QAction('Искать', self)
        # showbtn.setShortcut('Ctrl+S')
        # showbtn.triggered.connect(self.SHOs)

        mapTypeBtn = QAction("Сменить слой", self)
        mapTypeBtn.setShortcut('Ctrl+M')
        mapTypeBtn.triggered.connect(self.change_map_type)

        # setupMenu.addAction(showbtn)
        setupMenu.addAction(mapTypeBtn)

    def change_map_type(self):
        if self.type == self.types[0]:
            self.type = self.types[1]
            self.map_file = "map.jpeg"
        elif self.type == self.types[1]:
            self.type = self.types[2]
            self.map_file = "map.jpeg"
        else:
            self.type = self.types[0]
            self.map_file = "map.png"
        self.map.setPixmap(self.get_map())

    def get_map(self):
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coords[0]},{self.coords[1]}'}" \
                      f"&l={self.type}&z={self.z}"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        pixmap = QPixmap(self.map_file)
        os.remove(self.map_file)
        return QPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.z < 17:
                self.z += 1
        elif event.key() == Qt.Key_PageDown:
            if self.z > 4:
                self.z -= 1
        elif event.key() == Qt.Key_W:
            self.coords[1] += 0.050 / self.z
        elif event.key() == Qt.Key_S:
            self.coords[1] -= 0.050 / self.z
        elif event.key() == Qt.Key_A:
            self.coords[0] -= 0.050 / self.z
        elif event.key() == Qt.Key_D:
            self.coords[0] += 0.050 / self.z
        self.map.setPixmap(self.get_map())

    # def SHOs(self):
    #     self.map.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
