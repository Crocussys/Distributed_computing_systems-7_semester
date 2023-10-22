from pynput import keyboard
from abc import ABC, abstractmethod
import psutil
import threading
import requests


class Metric(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def start_collect(self):
        pass

    @abstractmethod
    def get_current_state(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @abstractmethod
    def stop_collect(self):
        pass


class CounterKeys(Metric):
    """
    Keystroke counter
    """
    def __init__(self):
        self.__name = "CounterKeys"
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
        """
        Start collecting metrics
        :return: None
        """
        if self.__listener.is_alive() is False:
            self.__listener.start()

    def get_current_state(self):
        """
        Get a name and value
        :return: name, value
        """
        return self.__name, self.__value

    def cleanup(self):
        """
        Reset to default value
        :return: None
        """
        self.__value = 0

    def stop_collect(self):
        """
        Stop collecting metrics
        :return: None
        """
        if self.__listener.is_alive():
            self.__listener.stop()


class IndicatorFrequency(Metric):
    """
    Processor frequency indicator
    """
    def __init__(self):
        self.__name = "IndicatorFrequency"
        self.__value = 0
        self.__collecting_flag = False
        self.__thread = None

    def __str__(self):
        return "Processor frequency indicator"

    def __collecting(self):
        """
        Collection of values
        :return: None
        """
        while self.__collecting_flag:
            self.__value = psutil.cpu_freq().current

    def start_collect(self):
        """
        Start collecting metrics
        :return: None
        """
        if self.__collecting_flag is False:
            self.__collecting_flag = True
            self.__thread = threading.Thread(target=self.__collecting, daemon=True)
            self.__thread.start()

    def get_current_state(self):
        """
        Get a name and value
        :return: name, value
        """
        return self.__name, self.__value

    def cleanup(self):
        """
        Reset to default value
        :return: None
        """
        self.__value = 0

    def stop_collect(self):
        """
        Stop collecting metrics
        :return: None
        """
        if self.__collecting_flag:
            self.__thread = None
            self.__collecting_flag = False


class USD(Metric):
    """
    Obtaining USD quote
    """
    def __init__(self):
        self.__name = "USD"
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
        while self.__collecting_flag:
            result = requests.get('https://www.cbr-xml-daily.ru/daily.xml').text
            result = result[result.find('<Valute ID="R01235">') + 20:]
            result = result[:result.find('</Valute>')]
            result = result[result.find('<Value>') + 7:result.find('</Value>')].replace(",", ".")
            self.__value = float(result)

    def start_collect(self):
        """
        Start collecting metrics
        :return: None
        """
        if self.__collecting_flag is False:
            self.__collecting_flag = True
            self.__thread = threading.Thread(target=self.__collecting, daemon=True)
            self.__thread.start()

    def get_current_state(self):
        """
        Get a name and value
        :return: name, value
        """
        return self.__name, self.__value

    def cleanup(self):
        """
        Reset to default value
        :return: None
        """
        self.__value = None

    def stop_collect(self):
        """
        Stop collecting metrics
        :return: None
        """
        if self.__collecting_flag:
            self.__thread = None
            self.__collecting_flag = False
