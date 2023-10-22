# Описание
Расширяемое решение для сборки метрик. Раз в `TIMER` секунд собирает числовые данные метрик и сохраняет их в файле `OUT_FILE_NAME` в формате csv. Формат данных: текущее время, название метрики, значение
# Системные требования
- Windows 10 или выше (Протестировано на Windows 11 22H2)
- Python 3.10 или выше (Протестировано на Python 3.11)
# Установка Windows
1. `git clone https://github.com/Crocussys/Distributed_computing_systems-7_semester.git` <br>
или по shh `git clone git@github.com:Crocussys/Distributed_computing_systems-7_semester.git`
2. `cd .\Distributed_computing_systems-7_semester\ `
3. `python -m venv .\venv`
4. `.\venv\Scripts\activate`
5. `pip install -r requirements.txt`
# Запуск
1. `.\venv\Scripts\activate`<br>
2. `python main.py`
# Параметры командной строки
usage: `main.py [-h] [-m] [-l METRICS [METRICS ...]] [-p OUT_PATH] [-f OUT_FILE_NAME] [-t TIMER]`<br>
options:<br>
  `-h`, `--help`            вывести это справочное сообщение и выйти<br>
  `-m`, `--metrics_help`    Показать информацию о доступных метриках и выйти<br>
  `-l METRICS [METRICS ...]`, `--metrics METRICS [METRICS ...]`<br>
                            Метрики, которые необходимо собирать. Если не указано, то будут собираться все доступные метрики.<br>
  `-p OUT_PATH`, `--out_path OUT_PATH`<br>
                        Путь до выходного файла<br>
  `-f OUT_FILE_NAME`, `--out_file_name OUT_FILE_NAME`<br>
                        Имя выходного файла<br>
  `-t TIMER`, `--timer TIMER`<br>
                        Сколько секунд надо ждать между сборками?<br>
# Доступные метрики
1. CounterKeys: Счетчик нажатий клавиш
2. IndicatorFrequency: Индикатор частоты процессора
3. USD: Получение котировок в долларах США
# Управление консолью
`start` Начать сбор метрик<br>
`stop` Прекратить сбор метрик<br>
`exit` Выйти из программы<br>