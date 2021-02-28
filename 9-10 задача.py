import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMenuBar, QAction, QInputDialog

from geocoder import get_coordinates, geocode


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.coords = [37.622504, 55.753215]
        self.coords_pt = []
        self.adress = 'Россия, Москва'
        self.z = 10
        self.map_file = "map.png"
        self.types = ["map", "sat", "sat,skl"]
        self.type = self.types[0]
        self.flag = False
        self.initUi()

    def initUi(self):
        self.setGeometry(400, 400, 600, 450)
        self.setWindowTitle('Большая задача по Maps API')
        self.setFixedSize(self.size())

        self.map = QLabel("", self)
        self.map.setGeometry(0, 0, 600, 450)
        self.map.setPixmap(self.get_map())

        self.adressPt = QLabel("Россия, Москва", self)
        self.adressPt.setGeometry(50, 0, 300, 20)
        self.adressPt.setVisible(True)

        mainMenu = QMenuBar(self)
        setupMenu = mainMenu.addMenu('Setup')

        showbtn = QAction('Искать', self)
        showbtn.setShortcut('Ctrl+S')
        showbtn.triggered.connect(self.SHOw)

        mapTypeBtn = QAction("Сменить слой", self)
        mapTypeBtn.setShortcut('Ctrl+M')
        mapTypeBtn.triggered.connect(self.change_map_type)

        mapPtBtn = QAction("Сброс поискового результата", self)
        mapPtBtn.setShortcut('Ctrl+R')
        mapPtBtn.triggered.connect(self.clearPt)

        indBtn = QAction("Показать индекс", self)
        indBtn.setShortcut('Ctrl+I')
        indBtn.triggered.connect(self.indPt)

        setupMenu.addAction(showbtn)
        setupMenu.addAction(mapTypeBtn)
        setupMenu.addAction(mapPtBtn)
        setupMenu.addAction(indBtn)

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
        if self.adress == 'Россия, Москва':
            map_request = f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coords[0]},{self.coords[1]}'}" \
                          f"&l={self.type}&z={self.z}"
        else:
            point = f'{self.coords_pt[0]},{self.coords_pt[1]},pm2rdm'
            map_request = f"https://static-maps.yandex.ru/1.x/?ll={f'{self.coords[0]},{self.coords[1]}'}" \
                          f"&l={self.type}&pt={point}&z={self.z}"
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
            self.coords[1] += 0.05 / self.z
        elif event.key() == Qt.Key_S:
            self.coords[1] -= 0.05 / self.z
        elif event.key() == Qt.Key_A:
            self.coords[0] -= 0.05 / self.z
        elif event.key() == Qt.Key_D:
            self.coords[0] += 0.05 / self.z
        self.map.setPixmap(self.get_map())

    def SHOw(self):
        adres, ok_pressed = QInputDialog.getText(self, "Адрес", 'введите адрес: (Москва Гурьянова 2)')
        if ok_pressed:
            if adres:
                try:
                    self.coords_pt = list(get_coordinates(adres))
                except:
                    pass
                if self.coords_pt:
                    self.adress = geocode(adres)['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                    self.adressPt.setText(geocode(adres)['metaDataProperty']['GeocoderMetaData']['Address']
                                          ['formatted'])
                    self.flag = not self.flag
                    self.indPt()
                    self.map.setPixmap(self.get_map())

    def clearPt(self):
        self.coords_pt = []
        self.adress = 'Россия, Москва'
        self.adressPt.setText('Россия, Москва')
        self.flag = not self.flag
        self.indPt()
        self.map.setPixmap(self.get_map())

    def indPt(self):
        self.flag = not self.flag
        try:
            ind = geocode(self.adress)['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        except:
            ind = '(Нет почтового индекса)'
        if self.flag:
            if self.adressPt.text() == self.adress:
                self.adressPt.setText(f'{self.adressPt.text()} {ind}')
        else:
            if self.adressPt.text() == f'{self.adress} {ind}':
                self.adressPt.setText(self.adress)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
