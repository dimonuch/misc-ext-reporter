import random
import datetime

config = dict()
config["exts_file"] = "./exts.csv"
config["history_file"] = "./calls.csv"
config["file_separator"] = ";"

config["exts_total"] = 1000
config["history_total"] = 6*31*10000


def main(config):

    # Файл с номерами
    # Возможные дубли в exts_file нас не волнуют
    # Это допустимо по условиям задачи и даже хорошо для тестов

    with open(config["exts_file"], 'w') as file:
        file.write("ext\n")  # шапка
        i = 0
        while (i < config["exts_total"]):
            file.write("{0}\n".format(random.randrange(100, 999)))
            i = i + 1

    # Файл с журналом звонков
    # Возможные отсутствующие номера (по первому файлу) нас не волнуют
    # Это допустимо по условиям задачи и даже хорошо для тестов

    start = datetime.datetime(year=2016, month=1, day=1)
    stop = datetime.datetime(year=2019, month=9, day=14)

    with open(config["history_file"], 'w') as file:
        file.write("ext{0}datetime\n".format(
            config["file_separator"]))  # шапка
        i = 0
        while (i < config["history_total"]):
            file.write("{0}{1}{2}\n".format(
                random.randrange(100, 980),     # Верхнее значение 980 - не ошибка! так надо
                config["file_separator"],
                random_date(start, stop)))
       
            i = i + 1


def random_date(start, end):

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


if __name__ == "__main__":
    main(config)
