from pynput import keyboard
from abc import ABC, abstractmethod
import psutil
import threading
import requests
import time


class Metric(ABC):
    @abstractmethod
    def __str__(self):
        """
        Should output a description of the metric
        :return: str
        """
        pass

    @abstractmethod
    def start_collect(self):
        """
        Start collecting metric
        :return: None
        """
        pass

    @abstractmethod
    def get_current_state(self):
        """
        Get a name and value
        :return: name, value
        """
        pass

    @abstractmethod
    def cleanup(self):
        """
        Reset to default value
        :return: None
        """
        pass

    @abstractmethod
    def stop_collect(self):
        """
        Stop collecting metric
        :return: None
        """
        pass


class CounterKeys(Metric):
    def __init__(self):
        self.__value = 0
        self.__listener = keyboard.Listener(on_press=self.__incrementation, on_release=None, suppress=False)

    def __str__(self):
        return "Keystroke counter"

    def __incrementation(self, _):
        """
        Called when the key is pressed
        :param _: key
        :return: None
        """
        self.__value += 1

    def start_collect(self):
        if self.__listener.is_alive() is False:
            self.__listener.start()

    def get_current_state(self):
        return "CounterKeys", self.__value

    def cleanup(self):
        self.__value = 0

    def stop_collect(self):
        if self.__listener.is_alive():
            self.__listener.stop()


class RAM(Metric):
    def __init__(self):
        self.__value = 0.
        self.__collecting_flag = False
        self.__thread = None

    def __str__(self):
        return "Calculates the amount of RAM usage in megabytes"

    def __collecting(self):
        """
        Collection of values
        :return: None
        """
        while self.__collecting_flag:
            self.__value = psutil.virtual_memory().used / 1_048_576
            time.sleep(1)

    def start_collect(self):
        if self.__collecting_flag is False:
            self.__collecting_flag = True
            self.__thread = threading.Thread(target=self.__collecting, daemon=True)
            self.__thread.start()

    def get_current_state(self):
        return "RAM", self.__value

    def cleanup(self):
        self.__value = 0.

    def stop_collect(self):
        if self.__collecting_flag:
            self.__collecting_flag = False
            self.__thread.join()
            self.__thread = None


class USD(Metric):
    def __init__(self):
        self.__value = None
        self.__collecting_flag = False
        self.__thread = None

    def __str__(self):
        return "Obtaining USD quote"

    def __collecting(self):
        """
        Collection of values
        :return: None
        """
        time_freeze = time.time() - 60
        while self.__collecting_flag:
            if time.time() - time_freeze >= 60:  # Condition of use
                result = requests.get('https://www.cbr-xml-daily.ru/daily.xml')
                if result.status_code == 200:
                    result = result.text
                    result = result[result.find('<Valute ID="R01235">') + 20:]
                    result = result[:result.find('</Valute>')]
                    result = result[result.find('<Value>') + 7:result.find('</Value>')].replace(",", ".")
                    self.__value = float(result)
                else:
                    self.__value = None
                time_freeze = time.time()

    def start_collect(self):
        if self.__collecting_flag is False:
            self.__collecting_flag = True
            self.__thread = threading.Thread(target=self.__collecting, daemon=True)
            self.__thread.start()

    def get_current_state(self):
        return "USD", self.__value

    def cleanup(self):
        pass

    def stop_collect(self):
        if self.__collecting_flag:
            self.__collecting_flag = False
            self.__thread.join()
            self.__thread = None
