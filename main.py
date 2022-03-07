from receive_mqtt import mqtt_rec

app=mqtt_rec().recive('zwl', 0, '127.0.0.1', 1883, 'zwl', '123456')
print(app)