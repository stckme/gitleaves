import arrow
import calendar
import csv
import datetime
import os
import os.path
import pathlib


from collections import defaultdict

from jinja2 import FileSystemLoader, Environment

srcdir = pathlib.Path(__file__).parent.resolve()
reports_dir = 'reports'
templates_dir = os.path.join(srcdir, 'templates')
ghwiki_reports_dir = os.path.join(reports_dir, 'ghwiki')
templates = Environment(loader=FileSystemLoader(templates_dir),
                        trim_blocks=True)

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
    nextbymonths = defaultdict(lambda: defaultdict(list))
    csv_f = csv.reader(open(csv_path))
    next(csv_f)
    for row in csv_f:
        daterange, applicant, *_ = row
        applicant = applicant.split('#')[0].strip()
        dates = range2dates(daterange)
        for date in dates:
            bydates[date].append(applicant)
            bynames[applicant].append(date)
            if date > today:
                nextbymonths[date.month][date].append(applicant)

    return {'bydates': bydates, 'bynames': bynames, 'bymonths': nextbymonths}


def gen_ghwiki_reports():
    data = load_csv(os.path.join('data', leaves_csv_path))
    today_leaves = data['bydates'][datetime.date.today()]
    this_month = datetime.date.today().month
    next_leaves_by_month = ((calendar.month_name[month], leaves)
                            for month, leaves in data['bymonths'].items()
                            if month >= this_month)
    template = templates.get_template('ghwiki/Home.md')
    if not os.path.exists(ghwiki_reports_dir):
        os.makedirs(ghwiki_reports_dir)
    with open(f'{ghwiki_reports_dir}/Home.md', 'w') as report:
        report.write(template.render(today_leaves=today_leaves,
                                     next_leaves_by_month=next_leaves_by_month))
    return ghwiki_reports_dir


def upload_ghwiki_reports():
    raise NotImplementedError
