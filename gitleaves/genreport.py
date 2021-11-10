import arrow
import calendar
import csv
import datetime

from collections import defaultdict

today = datetime.date.today()
leaves_csv_path = f'leaves.{today.year}.csv'
extras_csv_path = f'leaves.{today.year}.csv'


def ddmm2date(s):
    return arrow.get(f'{today.year}{s.strip()}')


def range2dates(daterange):
    """
    '1307 - 2907' →  [date(2021, 7, 13), ....]
    Except weekends
    """
    if '-' in daterange:
        start, end = [ddmm2date(d) for d in daterange.split('-')]
        dates = arrow.Arrow.range('day', start, end)
    else:
        dates = [ddmm2date(daterange)]
    return [d.date() for d in dates]


def load_csv(csv_path):
    bydates = defaultdict(list)
    bynames = defaultdict(list)
    csv_f = csv.reader(open(csv_path))
    next(csv_f)
    for row in csv_f:
        daterange, applicant, *_ = row
        applicant = applicant.split('#')[0].strip()
        dates = range2dates(daterange)
        for date in dates:
            bydates[date].append(applicant)
            bynames[applicant].append(date)

    return {'bydates': bydates, 'bynames': bynames}


def filter(data, start=None, end=None, name=None):
    for row in data:
        if name and name != applicant:
            continue
            if start and (date < start):
                continue
            if end and (date > start):
                continue

month = None
for d, names in load_csv(leaves_csv_path)['bydates'].items():
    if month != d.month:
        month_name = calendar.month_name[d.month]
        print(f'{month_name}\n===========')
    print(d, names)
    month = d.month
for d, names in load_csv(leaves_csv_path)['bynames'].items():
    print(d, len(names))
