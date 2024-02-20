import time
import pickle
import requests

FILENAME = "user.dat"

name = ''
age = 3

with open(FILENAME, "rb") as file:
    name = pickle.load(file)
    age = pickle.load(file)

file.close()
print("Ожидате отправки даных в течении 61 секунд!")
while True:
    time.sleep(61)
    try:
        with open(FILENAME, "rb") as file:
            name = pickle.load(file)
            age = pickle.load(file)
            tt = str(time.ctime(time.time()))
            # print(tt)
            print('Время:', tt, "\tСостояние:", name, "\tКод:", age)
            # get_request = f'http://open-monitoring.online/get?cid=2224&key=ZATUCE&p1=00&p2={name}&p3={age}'
            get_request = f'http://open-monitoring.online/get?cid=2225&key=FxidjO&p1=ЗНАЧ1&p2=ЗНАЧ2' \
                          f'&p3=ЗНАЧ3&p4=ЗНАЧ4&p5=ЗНАЧ5&p6=ЗНАЧ6&p7=ЗНАЧ7&p8=ЗНАЧ8&p9=ЗНАЧ9&p10=ЗНАЧ10' \
                          f'&p11=ЗНАЧ11&p12=ЗНАЧ12&p13=ЗНАЧ13&p14=ЗНАЧ14&p15=ЗНАЧ15&p16=ЗНАЧ16'
            print(get_request)
            requests.get(get_request)
        file.close()

    except Exception as e:
        print('Error get request OM: ', e)


