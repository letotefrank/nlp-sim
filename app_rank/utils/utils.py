from datetime import datetime


def date_deal(date):
    if len(date) < 11:
        date = date + ' ' + '00:00:00'
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return date
    else:
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return date
