from metrics import *
import threading
import csv
import time


def save_thread(sleep=60):
    """
    Every [sleep] seconds writes the metrics values to csv
    :param sleep: int
    :return: None
    """
    time_freeze = time.time()
    while t_console.is_alive():
        if time.time() - time_freeze >= sleep:
            with open("out.csv", "a") as file:
                for obj in collecting_metrics:
                    name, value = obj.get_current_state()
                    csv.writer(file, lineterminator="\r").writerow([time.ctime(), name, value])
            time_freeze = time.time()


def start_collect(objs):
    """
    obj.start_collect() for each of the lists
    :param objs: list of objects
    :return: None
    """
    for obj in objs:
        obj.start_collect()
        collecting_metrics.append(obj)
        print(f"Started collecting {obj.get_current_state()[0]}")


def stop_collect(objs):
    """
    obj.stop_collect() for each of the lists
    :param objs: list of objects
    :return: None
    """
    for obj in objs:
        obj.stop_collect()
        collecting_metrics.remove(obj)
        print(f"Stopped collecting {obj.get_current_state()[0]}")


def cleanup(objs):
    """
    obj.cleanup() for each of the lists
    :param objs: list of objects
    :return: None
    """
    for obj in objs:
        obj.cleanup()
        print(f"{obj.get_current_state()[0]} is reset to default values")


def args_in_list(inp):
    """
    Converts a list of names to a list of objects
    :param inp: list arguments
    :return: list of objects
    """
    argc = len(inp)
    if argc < 2:
        print("Insufficient arguments!")
        return list()
    if inp[1] == "all":
        return list(metric_objects.values())
    objs_list_arg = list()
    for arg_i in range(1, argc):
        arg = inp[arg_i]
        obj = metric_objects.get(arg)
        if obj is None:
            print(f"Metric {arg} was not found!")
            continue
        objs_list_arg.append(obj)
    return objs_list_arg


def menu():
    """
    Console control
    :return: None
    """
    inp = input().split(" ")
    while inp[0] != "exit":
        if inp[0] == "start":
            start_collect(args_in_list(inp))
        elif inp[0] == "stop":
            stop_collect(args_in_list(inp))
        elif inp[0] == "clean":
            cleanup(args_in_list(inp))
        elif inp[0] == "collecting":
            out = ""
            for obj in collecting_metrics:
                out += obj.get_current_state()[0] + ", "
            print(out[:-2])
        else:
            print("Invalid command!")
        inp = input().split(" ")


if __name__ == '__main__':
    _metric_classes = [CounterKeys, IndicatorFrequency]  # Here, list the classes that control the metrics
    collecting_metrics = list()  # Metrics that collect data at the moment
    metric_objects = dict()  # Class instances and their names
    for _class in _metric_classes:
        _obj = _class()
        _name = _obj.get_current_state()[0]
        if _name == "all":
            raise "The name 'all' is not available for metrics"
        metric_objects.update({_name: _obj})
    # Threads
    t_console = threading.Thread(target=menu, daemon=True)
    t_save = threading.Thread(target=save_thread, args=(5,), daemon=True)
    t_console.start()
    t_save.start()
    t_console.join()
    t_save.join()
