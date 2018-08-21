import requests
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QListWidgetItem, QLabel, QListWidget, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QMainWindow):

    def weatherSearch(self, woeid):
        responseWeatherSearch = requests.get("https://www.metaweather.com/api/location/" + woeid + "/")
        dataWeather = responseWeatherSearch.json()
        return dataWeather

    def locationSearch(self, textboxValue):
        responseLocationSearch = requests.get("https://www.metaweather.com/api/location/search/?query=" + textboxValue)
        responseLocationList = responseLocationSearch.json()
        return responseLocationList

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 textbox - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 350

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label = QLabel("Type location:", self)
        self.label.move(40, 0)
        self.label.resize(280, 40)

        self.textbox = QLineEdit(self)
        self.textbox.move(40, 40)
        self.textbox.resize(280, 40)

        self.button = QPushButton('Search weather for location', self)
        self.button.move(40, 80)
        self.button.resize(280, 40)

        self.button.clicked.connect(self.findLocations)

        self.show()

        self.locationListWidget = QListWidget(self)
        self.locationListWidget.move(40, 120)
        self.locationListWidget.resize(280, 120)

        self.weatherLabel = QLabel(self)
        self.weatherLabel.move(40, 250)
        self.weatherLabel.resize(280, 100)


    @pyqtSlot()
    def findLocations(self):
        textboxValue = self.textbox.text()
        responseLocationList = self.locationSearch(textboxValue)

        for i in range(len(responseLocationList)):
            itemLocation = QListWidgetItem()
            itemLocation.setText(str(responseLocationList[i]["title"]))
            self.locationListWidget.addItem(itemLocation)

        self.locationListWidget.show()

        self.locationListWidget.itemClicked.connect(self.itemActivated_FindWeather)


    def itemActivated_FindWeather(self, item):
        chosenCity = item.text()
        chosenCityLocationData = self.locationSearch(chosenCity)
        dataWeather = self.weatherSearch(str(chosenCityLocationData[0]["woeid"]))

        weather_state_name = dataWeather["consolidated_weather"][0]["weather_state_name"]
        the_temp = dataWeather["consolidated_weather"][0]["the_temp"]
        air_pressure = dataWeather["consolidated_weather"][0]["air_pressure"]
        wind_speed = dataWeather["consolidated_weather"][0]["wind_speed"]

        self.weatherLabel.setText(weather_state_name+"\n"+
                                  "Temperature "+str(the_temp)+
                                  "\n"+"Air pressure "+str(air_pressure)+
                                  "\n"+"Wind speed "+str(wind_speed))
        self.weatherLabel.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
