from datetime import datetime
from random import randrange
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import serial
import re


cred = credentials.Certificate("./firebase.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
ser = serial.Serial(
    port="COM3",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
)

print("connected to: " + ser.portstr)

while True:
    # delay 0.2 seconds

    #data = ser.read(9999)
    # db.collection("arduino").add(
    #     {
    #         "voltage": randrange(0, 10),
    #         "current": randrange(0, 10),
    #         "power": randrange(0, 10),
    #         "timestamp": str(datetime.now().timestamp()),
    #     }
    # )
    # time.sleep(0.5)
    time.sleep(.001)                    # delay of 1ms
    val = ser.readline()                # read complete line from serial output
    while not '\r\n' in str(val.decode("utf-8")):         # check if full data is received. 
        # This loop is entered only if serial read value doesn't contain \n
        # which indicates end of a sentence. 
        # str(val) - val is byte where string operation to check `\\n` 
        # can't be performed
        time.sleep(.001)                # delay of 1ms 
        temp = ser.readline()           # check for serial output.
        if not not temp.decode("utf-8"):       # if temp is not empty.
            val = (val.decode("utf-8")+temp.decode("utf-8")).encode()
            # requrired to decode, sum, then encode because
            # long values might require multiple passes
    val = val.decode("utf-8")                  # decoding from bytes
    print(val, end="")                         # print the value
    
    # remove everthing except numbers and comma
    val = re.sub("[^0-9^,]", "", val.strip()).split(",")                  # stripping leading and trailing spaces.
    
    if len(val) != 3:
        continue
    
    db.collection("arduino").add(
        {
            "voltage": int(val[1])/10,
            "current": int(val[2])*5,
            "power": int(val[0])/2,
            "timestamp": str(datetime.now().timestamp()),
        }
    )