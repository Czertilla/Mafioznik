import time


def now():
    moment = time.time()
    moment = time.localtime(moment)
    return f"{moment.tm_mday}.{moment.tm_mon}.{moment.tm_year} \
{moment.tm_hour}:{moment.tm_min}:{moment.tm_sec}"

print(now())