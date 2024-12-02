import sys
import paho.mqtt.client as mqtt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import QTimer

class MqttClient:
    def __init__(self, broker, port, topic, on_message_callback):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = on_message_callback
        self.broker = broker
        self.port = port
        self.topic = topic

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.client.subscribe(self.topic)

    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mqtt_client = MqttClient("broker.hivemq.com", 1883, "test/topic", self.on_message)
        self.mqtt_client.connect()

    def initUI(self):
        self.setWindowTitle("MQTT Data Acquisition")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("MQTT Messages:", self)
        self.layout.addWidget(self.label)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        self.connect_button = QPushButton("Connect", self)
        self.connect_button.clicked.connect(self.connect_mqtt)
        self.layout.addWidget(self.connect_button)

        self.disconnect_button = QPushButton("Disconnect", self)
        self.disconnect_button.clicked.connect(self.disconnect_mqtt)
        self.layout.addWidget(self.disconnect_button)

        self.setLayout(self.layout)

    def connect_mqtt(self):
        self.mqtt_client.connect()

    def disconnect_mqtt(self):
        self.mqtt_client.disconnect()

    def on_message(self, client, userdata, msg):
        message = f"Topic: {msg.topic}\nMessage: {msg.payload.decode()}\n"
        self.text_edit.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
