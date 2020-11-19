import random
import time
import datetime
from PyQt5.QtCore import QDateTime, QDate, QTime


#   随机间隔
def randomSleep():
    ret = random.uniform(0.3, 1.8)
    time.sleep(ret)


#   获取随机数
def randInt(a, b):
    return random.randint(a, b)


#  年月日获取时间戳
def dateToUix(year, moth, day):
    date = QDate(year, moth, day)
    qtime = QTime(0, 0)
    return QDateTime(date, qtime).toTime_t()


#   获取开始结束日期
def timeLag(daylag: int = 5, timetype: str = 'uix'):  # 日期间隔  类型 uix时间戳 day日期
    res = False
    endday = datetime.date.today()
    enduix = int(time.mktime(time.strptime(str(endday), '%Y-%m-%d')))
    startday = endday - datetime.timedelta(days=daylag)  # 默认最近几天
    startuix = int(time.mktime(time.strptime(str(startday), '%Y-%m-%d')))
    if timetype == 'uix':
        res = (startuix, enduix)
    else:
        res = (startday, endday)
    return res


#   生成最近n天日期
def dateDayList(dateAry: tuple):
    start, end = dateAry
    res = []
    cur_day = start
    res.append(cur_day.toString('yyyy-MM-dd'))
    while cur_day < end:
        cur_day = cur_day.addDays(+1)
        res.append(cur_day.toString('yyyy-MM-dd'))
    return res


#   近几日时间戳
def dateUixList(dateAry: tuple):
    start, end = dateAry
    qtime = QTime(0, 0)
    res = []
    cur_day = start
    res.append(QDateTime(cur_day, qtime).toTime_t())
    while cur_day < end:
        cur_day = cur_day.addDays(+1)
        res.append(QDateTime(cur_day, qtime).toTime_t())
    return res


#   QDate 转时间戳
def dateToStamps(dateAry: tuple):
    start, end = dateAry
    qtime = QTime(0, 0)
    start = QDateTime(start, qtime)
    end = QDateTime(end, qtime)
    return (start.toTime_t(), end.toTime_t())


#   时间戳转日期字符串
def uixToDateStr(uix):
    qdatetime = QDateTime.fromTime_t(uix)
    return qdatetime.toString('yyyy-MM-dd')


#   获取前几日时间戳
def targetDateUix(diff: int, tdate: object = None):
    if not tdate:
        tdate = QDate.currentDate()
    tdate = tdate.addDays(diff)
    time = QTime(0, 0)
    return QDateTime(tdate, time).toTime_t()


def logFile(strings: str, file='debug-log.log'):
    """
    字符串写入文件
    """
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open(file, 'a+') as f:
        f.write('\n')
        f.write(now)
        f.write('\n')
        f.write(strings)
        f.write('\n')