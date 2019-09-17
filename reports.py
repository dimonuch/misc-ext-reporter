import pandas as pd

# Секция с настройками. Тут даже что-то менять можно. Удалять строки нельзя, иначе будет больно
config = dict()
# файл со списком номеров
config["exts_file"] = "./exts.csv"
# файл с журналом звонков
config["history_file"] = "./calls.csv"
# разделитель в CSV файлах
config["file_separator"] = ","
# Сколько показывать отсутствующих в журнале номеров
config["top_missed"] = 1000
# Сколько показывать самых старых звонков
config["top_oldest"] = 30


# А вот дальше лучше не смотреть. Там говнокод, который "как-то работает"

def main(config):

    print("Поехали")

    try:
        all_exts = pd.read_csv(
            config["exts_file"], sep=config["file_separator"], dtype={'ext': str})
        history = pd.read_csv(
            config["history_file"], sep=config["file_separator"], parse_dates=["calldate"],
            usecols=['calldate', 'src', 'dst'], dtype={'src': str, 'dst': str})
    except Exception as e:
        print(e)
        return

    # маленькая проверка - загрузились ли данные именно как "дата"?
    if (pd.core.dtypes.common.is_datetime_or_timedelta_dtype(history.calldate) != True):
        print("Ошибка: в колонке 'дата' журнала какой-то мусор.")
        return

    counter = dict()
    counter["all_ext"] = all_exts.count().ext

    exts = all_exts.drop_duplicates(subset="ext")
    counter["ext"] = exts.count().ext

    counter["history_all"] = history.count().src
    counter["history_ext_all"] = history["src"].append(history["dst"]).nunique()
    counter["history_mindate"] = history.calldate.min()
    counter["history_maxdate"] = history.calldate.max()

    # Усекаем журнал, оставляем только записи с номерами из "списка номеров"
    history = history[history['src'].isin(exts["ext"]) | history['dst'].isin(exts["ext"])]

    counter["history"] = history.count().src
    counter["history_ext"] = history["src"].append(history["dst"]).nunique()

    print("\n== Статистика")
    print(
        "Номеров (всего / уникальных): {0} / {1}".format(counter["all_ext"], counter["ext"]))
    print("Журнальных записей (всего / отобрано по номерам): {0} / {1}".format(
        counter["history_all"], counter["history"]))
    print("Номеров в журнале (всего / в отобранных) : {0} / {1}".format(
        counter["history_ext_all"], counter["history_ext"]))
    print(
        "Журнал за период с {0:%Y-%m-%d} по {1:%Y-%m-%d}".format(counter["history_mindate"], counter["history_maxdate"]))

    print("\n== Аналитика")

    print("Номера отсутствуют в журнале (не звонили) ТОП({0}):".format(
        config["top_missed"]))

    missed_exts = exts[~exts['ext'].isin(
        history["src"]) & ~exts['ext'].isin(history["dst"])]

    print(", ".join(map(str, missed_exts["ext"].head(
        config["top_missed"]).tolist())))
    return
    print("")

    print("Наиболее старые последние звонки ТОП({0}):".format(
        config["top_oldest"]))

    oldest_calls = history.groupby("ext").agg({"datetime": ["max"]}).sort_values(
        [("datetime", "max")], ascending=True).head(config["top_oldest"])

    print(oldest_calls)


if __name__ == "__main__":
    main(config)
