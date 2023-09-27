from pynput import keyboard
import psutil
import threading


class CounterKeys:
    """
    Keystroke counter
    """
    def __init__(self):
        self.__name = "CounterKeys"
        self.__value = 0
        self.__listener = keyboard.Listener(on_press=self.__incrementation, on_release=None, suppress=False)

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


class IndicatorFrequency:
    """
    Processor frequency indicator
    """
    def __init__(self):
        self.__name = "IndicatorFrequency"
        self.__value = 0
        self.__collecting_flag = False
        self.__thread = None

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
            self.__thread.join()
            self.__thread = None
            self.__collecting_flag = False