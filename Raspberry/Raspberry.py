from mfrc522 import SimpleMFRC522
import relay_ft245r
import wiringpi
import requests
import time
import json
import sys

reader = SimpleMFRC522()
rb = relay_ft245r.FT245R()
dev_list = rb.list_dev()
dev = dev_list[0]
rb.connect(dev)
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(12, 1) #rot
wiringpi.pinMode(16, 1) #gruen
wiringpi.pinMode(20, 1)


schrank_id = 1
facher = 4

while True:
    wiringpi.digitalWrite(12, 0)
    wiringpi.digitalWrite(16, 0)
    wiringpi.digitalWrite(20, 0)
    id = reader.read_id()
    payload = {"id": hex(id)}
    r = requests.post("http://192.168.178.21:5000/checkID", json=payload)

    if r.status_code == 200:
        permissions = json.loads(r.text)
        if "*" in permissions:
            print("Opening all dors for admin")
            wiringpi.digitalWrite(16, 1)
            for fach in range(1, facher+1):
                rb.switchon(fach)
            time.sleep(1)
            for fach in range(1, facher+1):
                rb.switchoff(fach)
                
        else:
            mypermissions = []
            for per in permissions:
                per = per.split("X")
                if int(per[0]) == schrank_id:
                    mypermissions.append(int(per[1]))
            if mypermissions:
                for fach in range(1, facher+1):
                    if fach in mypermissions:
                        print("Opening door " + str(fach))
                        wiringpi.digitalWrite(16, 1)
                        rb.switchon(fach)
                        time.sleep(1)
                        rb.switchoff(fach)
                        break
            else:
                wiringpi.digitalWrite(12, 1)   
    else:
        wiringpi.digitalWrite(12, 1)
    time.sleep(3)
