from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QGraphicsColorizeEffect
from PyQt5.QtGui import QFont, QPixmap, QColor
from functools import partial
import requests
import sys
import json



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 1000, 600)
        
        self.uiComponents()
        
        with open("env.json","r") as file:
            self.api_key = json.load(file)
            
        
    def uiComponents(self):
        
        self.title = QLabel("Search Weather Of City",self)
        self.title.setFont(QFont("Times font",15))
        self.title.setGeometry(300,30,300,30)

        self.textbox = QLineEdit("Enter The City",self)
        self.textbox.setFont(QFont("Arial",15))
        self.textbox.setGeometry(280,90,250,40)
        
        self.button = QPushButton("Get The Weather",self)
        self.button.clicked.connect(partial(self.weatherAPI,self.textbox))
        self.button.setGeometry(300,150,200,40)

        self.pixmap = QPixmap("sun.png")
        self.pixmapLabel = QLabel(self)
        self.pixmapLabel.setPixmap(self.pixmap)
        self.pixmapLabel.setGeometry(600,30,30,30)
        self.pixmapLabel.adjustSize()
        
        self.temp = QLabel("Temp:",self)
        self.temp.setFont(QFont("Time font",13))
        self.temp.setGeometry(160,200,100,30)
        
        self.tempblank = QLabel("Temp:",self)
        self.tempblank.setFont(QFont("Time font",13))
        self.tempblank.setGeometry(240,200,100,30)
        self.tempblank.setText("...")
        
        self.feels_like = QLabel("Feel Like:",self)
        self.feels_like.setFont(QFont("Time font",13))
        self.feels_like.setGeometry(160,240,100,30)
        
        self.feels_likeblank = QLabel("Temp:",self)
        self.feels_likeblank.setFont(QFont("Time font",13))
        self.feels_likeblank.setGeometry(240,240,100,30)
        self.feels_likeblank.setText("...")
        
        self.temp_min = QLabel("Temp Min:",self)
        self.temp_min.setFont(QFont("Time font",13))
        self.temp_min.setGeometry(160,280,100,30)
        
        self.temp_minblank= QLabel("Temp:",self)
        self.temp_minblank.setFont(QFont("Time font",13))
        self.temp_minblank.setGeometry(250,280,100,30)
        self.temp_minblank.setText("...")
        
        self.temp_max = QLabel("Temp Max:",self)
        self.temp_max.setFont(QFont("Time font",13))
        self.temp_max.setGeometry(160,320,100,30)
        
        self.temp_maxblank= QLabel("Temp:",self)
        self.temp_maxblank.setFont(QFont("Time font",13))
        self.temp_maxblank.setGeometry(250,320,100,30)
        self.temp_maxblank.setText("...")
        
        self.pressure = QLabel("Pressure:",self)
        self.pressure.setFont(QFont("Time font",13))
        self.pressure.setGeometry(160,360,100,30)
        
        self.pressureblank= QLabel("Pressure:",self)
        self.pressureblank.setFont(QFont("Time font",13))
        self.pressureblank.setGeometry(250,360,100,30)
        self.pressureblank.setText("...")
        
        self.humidity = QLabel("Humidty:",self)
        self.humidity.setFont(QFont("Time font",13))
        self.humidity.setGeometry(160,400,100,30)
        
        self.humidityblank= QLabel("Pressure:",self)
        self.humidityblank.setFont(QFont("Time font",13))
        self.humidityblank.setGeometry(250,400,100,30)
        self.humidityblank.setText("...")
        
        self.description = QLabel("Description:",self)
        self.description.setFont(QFont("Time font",13))
        self.description.setGeometry(160,440,100,30)
        
        self.descriptionblank= QLabel("Pressure:",self)
        self.descriptionblank.setFont(QFont("Time font",13))
        self.descriptionblank.setGeometry(270,440,100,30)
        self.descriptionblank.setText("...")
        
        self.errorlabel = QLabel("",self)
        self.errorlabel.setFont(QFont("Time font",14))
        effect = QGraphicsColorizeEffect(self)
        effect.setColor(QColor(255,0,0))
        self.errorlabel.setGraphicsEffect(effect)
        self.errorlabel.setGeometry(300,480,500,40)
    
    
    def weatherAPI(self,textbox):
        city = textbox.text()
        
        try:
                
            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=tr&appid={self.api_key['API_KEY']}&units=metric")
            res = response.json()
            
            coord = ((res['coord'])["lon"],(res['coord'])["lat"])
            temp,feels_like,temp_min,temp_max = (res['main'])['temp'],(res['main'])['feels_like'],(res['main'])['temp_min'],(res['main'])['temp_max']
            pressure = (res['main'])['pressure']
            humidity = (res['main'])['humidity']
            description = ((res['weather'])[0])["description"]
        
            self.updateComponents(str(temp), str(feels_like), str(temp_min), str(temp_max), str(pressure), str(humidity), str(description))
            
        except:
            self.errorlabel.setText(f"There is not a \"{city}\" named city!")
            print(f"There is not a \"{city}\" named city !")
        
    def updateComponents(self,temp,feels_like,temp_min,temp_max,pressure,humidity,description):
        self.tempblank.setText(temp)
        self.feels_likeblank.setText(feels_like)
        self.temp_minblank.setText(temp_min)
        self.temp_maxblank.setText(temp_max)
        self.pressureblank.setText(pressure)
        self.humidityblank.setText(humidity)
        self.descriptionblank.setText(description)
        self.errorlabel.setText("")
        
app = QApplication(sys.argv)

window = MainWindow()
window.show()


app.exec()