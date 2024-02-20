import pickle
import serial
import time
import requests
import logging
import configparser

logging.basicConfig(filename='my_logs.log',
                    format='%(levelname)s -> %(asctime)s: %(message)s',
                    level=logging.INFO)

try:
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг
    port = config["Connect"]["port"]
    speed = config["Connect"]["speed"]
    sp = int(config["Opros"]["sp"])  # Время ожидания в секундах

except Exception as e:
    print("Don't find settings.ini:", e)
    # input("Нажмите Enter для выхода")
    exit()


def connect():
    try:
        # print("sp: ", sp)
        print("Start program !!!")
        # port = "COM8"
        # ser = serial.Serial(port, speed, timeout=0.300)
        # ser = serial.Serial(port, 9600, timeout=0.300)
        print("Подключено к COM порту")
        print(f"port{port}")
        return serial.Serial(port, speed, timeout=0.300)

    except Exception as e:
        print("Can't connect to COM port!!!", e)
        # input("Нажмите Enter для выхода")
        exit()


ser = connect()


def status_module(key):
    try:
        request_status = b'\x01\x02\x00\x00\x00\x10\x79\xC6'
        ser.write(request_status)
        print(f'Отправлен запрос на состояние модуля ')
        answer = read_answer_module(True)
        print(f'Получен ответ от модуля {answer}')
        i = 0
        d = b''
        g = b''
        for c in answer:
            i = i + 1
            if i == 4:
                d = c & 0b11111111
            if i == 5:
                g = c & 0b11111111
        di_01 = (d & 0b00000001) >> 0
        di_02 = (d & 0b00000010) >> 1
        di_03 = (d & 0b00000100) >> 2
        di_04 = (d & 0b00001000) >> 3
        di_05 = (d & 0b00010000) >> 4
        di_06 = (d & 0b00100000) >> 5
        di_07 = (d & 0b01000000) >> 6
        di_08 = (d & 0b10000000) >> 7

        di_09 = (g & 0b00000001) >> 0
        di_10 = (g & 0b00000010) >> 1
        di_11 = (g & 0b00000100) >> 2
        di_12 = (g & 0b00001000) >> 3
        di_13 = (g & 0b00010000) >> 4
        di_14 = (g & 0b00100000) >> 5
        di_15 = (g & 0b01000000) >> 6
        di_16 = (g & 0b10000000) >> 7
        current_time = str(time.asctime())
        print("Состояние КУ на: ", current_time)
        print("     №1  №2  №3  №4  №5  №6  №7  №8")
        print("ВКЛ: ", di_01, " ", di_02, " ", di_03, " ", di_04, " ", di_05, " ", di_06, " ", di_07, " ", di_08)
        print("ЗАГ: ", di_09, " ", di_10, " ", di_11, " ", di_12, " ", di_13, " ", di_14, " ", di_15, " ", di_16)
        print("*************************************************************************************************")
        # logging.info("added %s and %s to get %s" % (bin(data), 99, 88))
        if key:
            logging.info("Состояние КУ на: %s" % current_time)
            logging.info("     №1  №2  №3  №4  №5  №6  №7  №8")
            di_01_str = str(di_01)
            di_02_str = str(di_02)
            di_03_str = str(di_03)
            di_04_str = str(di_04)
            di_05_str = str(di_05)
            di_06_str = str(di_06)
            di_07_str = str(di_07)
            di_08_str = str(di_08)
            di_09_str = str(di_09)
            di_10_str = str(di_10)
            di_11_str = str(di_11)
            di_12_str = str(di_12)
            di_13_str = str(di_13)
            di_14_str = str(di_14)
            di_15_str = str(di_15)
            di_16_str = str(di_16)
            logging.info("ВКЛ:  %s   %s   %s   %s   %s   %s   %s   %s"
                         % (di_01_str, di_02_str, di_03_str, di_04_str, di_05_str, di_06_str, di_07_str, di_08_str))
            logging.info("ЗАГ:  %s   %s   %s   %s   %s   %s   %s   %s"
                         % (di_09_str, di_10_str, di_11_str, di_12_str, di_13_str, di_14_str, di_15_str, di_16_str))
            logging.info(
                "*************************************************************************************************")

        return [d, g]
    except Exception as er:
        print("Donn't find COM port or no data!", er)
        i = 0
        while i < 3:
            time.sleep(2)
            connect()
        # input("Нажмите Enter для выхода")
        exit()


def read_answer_module(key):
    if key:
        count = 8
    else:
        count = 6
    data_sum = b''
    ser.flush()
    ser.timeout = 0.1
    while count != 0:
        data = ser.read()
        count = count - 1
        data_sum += data
    ser.flush()
    return data_sum


def get_request(data):
    d = data[0]
    di_01 = (d & 0b00000001) >> 0
    di_02 = (d & 0b00000010) >> 1
    di_03 = (d & 0b00000100) >> 2
    di_04 = (d & 0b00001000) >> 3
    di_05 = (d & 0b00010000) >> 4
    di_06 = (d & 0b00100000) >> 5
    di_07 = (d & 0b01000000) >> 6
    di_08 = (d & 0b10000000) >> 7

    g = data[1]
    di_09 = (g & 0b00000001) >> 0
    di_10 = (g & 0b00000010) >> 1
    di_11 = (g & 0b00000100) >> 2
    di_12 = (g & 0b00001000) >> 3
    di_13 = (g & 0b00010000) >> 4
    di_14 = (g & 0b00100000) >> 5
    di_15 = (g & 0b01000000) >> 6
    di_16 = (g & 0b10000000) >> 7

    try:
        get_request = f'http://open-monitoring.online/get?cid=2225&key=FxidjO&p1={di_01}&p2={di_02}' \
                      f'&p3={di_03}&p4={di_04}&p5={di_05}&p6={di_06}&p7={di_07}&p8={di_08}&p9={di_09}&p10={di_10}' \
                      f'&p11={di_11}&p12={di_12}&p13={di_13}&p14={di_14}&p15={di_15}&p16={di_16}'
        # print(get_request)
        requests.get(get_request)
    except Exception as e:
        print("Error OM:", e)
        # input("Нажмите Enter для выхода")
        exit()


def write_file(data):
    with open("user.dat", "wb") as file:
        pickle.dump(data, file)


def status_poll_module(sp):
    try:
        key = False
        data_start = status_module(key)
        while True:
            data = status_module(key)
            write_file(data)
            if data_start != data:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("Произошло изменение в состоянии компрессоров")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                data_start = status_module(True)
            get_request(data)
            time.sleep(sp)
    except Exception as er:
        print("Error status module!!!", er)
        #  input("Нажмите Enter для выхода")
        exit()


def main():
    status_poll_module(sp)


if __name__ == '__main__':
    main()
