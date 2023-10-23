from metrics import *
import threading
import argparse
import csv
import time


def usage():
    """
    Processing command line arguments
    :return: args
    """
    parser = argparse.ArgumentParser(description='Metrics collector')
    parser.add_argument('-m', '--metrics_help', help='Show information about available metrics and exit', action="store_true")
    parser.add_argument('-l', '--metrics', nargs='+', help='Metrics to be collected. If not specified, all available metrics will be collected.')
    parser.add_argument('-p', '--out_path', type=str, help='Output path', default='./')
    parser.add_argument('-f', '--out_file_name', type=str, help='Output file name', default='out.csv')
    parser.add_argument('-t', '--timer', type=int, help='How many seconds do you have to wait between collections?', default=60)
    return parser.parse_args()


def metrics_help():
    """
    Display information about available metrics
    :return: None
    """
    for name, obj in metric_objects.items():
        print(f"{name}: {obj}")


def save_thread(sleep):
    """
    Every [sleep] seconds writes the metrics values to csv
    :param sleep: int
    :return: None
    """
    time_freeze = time.time()
    while t_console.is_alive():
        if time.time() - time_freeze >= sleep:
            with open(f"{args.out_path}{args.out_file_name}", 'a') as file:
                for obj in collecting_metrics:
                    name, value = obj.get_current_state()
                    obj.cleanup()
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
        print(f"Started collecting {obj.get_current_state()[0]}")


def stop_collect(objs):
    """
    obj.stop_collect() for each of the lists
    :param objs: list of objects
    :return: None
    """
    for obj in objs:
        if collecting_metrics.count(obj) > 0:
            obj.stop_collect()
            print(f"Stopped collecting {obj.get_current_state()[0]}")


def menu():
    """
    Console control
    :return: None
    """
    print(">start: Start collecting metrics")
    print(">stop: Stop collecting metrics")
    print(">exit: Quit the program", end="\n\n")
    inp = input(">")
    while inp != "exit":
        if inp == "start":
            start_collect(collecting_metrics)
        elif inp == "stop":
            stop_collect(collecting_metrics)
        else:
            print("Invalid command!")
        inp = input(">")


if __name__ == '__main__':
    args = usage()
    _metric_classes = [CounterKeys, RAM, USD]  # Here, list the classes that control the metrics
    metric_objects = dict()  # Class instances and their names
    for _class in _metric_classes:
        _obj = _class()
        _name = _obj.get_current_state()[0]
        if _name == "all":
            raise "The name 'all' is not available for metrics"
        metric_objects.update({_name: _obj})
    if args.metrics_help:
        metrics_help()
        exit()
    collecting_metrics = list()  # Metrics that collect data
    if args.metrics is None:
        collecting_metrics = list(metric_objects.values())
    else:
        for metric_inp in args.metrics:
            _obj = metric_objects.get(metric_inp)
            if _obj is None:
                print(f"Metric {metric_inp} was not found!")
                continue
            collecting_metrics.append(_obj)
    # Threads
    t_console = threading.Thread(target=menu, daemon=True)
    t_save = threading.Thread(target=save_thread, args=(args.timer,), daemon=True)
    t_console.start()
    t_save.start()
    t_console.join()
    t_save.join()
