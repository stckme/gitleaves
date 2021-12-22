import shutil

import arrow
import calendar
import csv
import datetime
import os
import os.path
import pathlib

from shutil import copyfile
from collections import defaultdict

from jinja2 import FileSystemLoader, Environment

srcdir = pathlib.Path(__file__).parent.resolve()
reports_dir = 'reports'
templates_dir = os.path.join(srcdir, 'templates')
ghwiki_reports_dir = os.path.join(reports_dir, 'ghwiki')
templates = Environment(loader=FileSystemLoader(templates_dir),
                        trim_blocks=True)

today = datetime.date.today()
leaves_csv_path_pat = os.path.join('data', 'leaves.{YYYY}.csv')
extras_csv_path_pat = os.path.join('data', 'extras.{YYYY}.csv')
leaves_csv_path = leaves_csv_path_pat.format(YYYY=today.year)
extras_csv_path = extras_csv_path_pat.format(YYYY=today.year)


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
    bymonths = defaultdict(lambda: defaultdict(list))
    group_of_people_by_month = defaultdict(lambda: defaultdict(list))
    csv_f = csv.reader(open(csv_path))
    next(csv_f)
    for row in csv_f:
        daterange, applicant, *_ = row
        applicant = applicant.split('#')[0].strip()
        dates = range2dates(daterange)
        for date in dates:
            bydates[date].append(applicant)
            bynames[applicant].append(date)
            bymonths[date.month][date].append(applicant)
            group_of_people_by_month[calendar.month_name[date.month]][applicant].append(date)

    return {'bydates': bydates, 'bynames': bynames, 'bymonths': bymonths, 'group_of_people_by_month': group_of_people_by_month}


def get_next_leaves_by_month(bydates):
    nextbymonths = defaultdict(lambda: defaultdict(list))
    for date, applicants in bydates.items():
        if date > today:
            nextbymonths[date.month][date] = applicants
    return nextbymonths


# Shekhar’s original in case Jason messes up, — mjb 12/20/2021
# def export_month_csv(year, month):
#     leaves_csv_path = leaves_csv_path_pat.format(YYYY=year)
#     data = load_csv(leaves_csv_path)
#     outfile = f'/tmp/leaves.{year}.{month}.csv'
#     outdata = ((d.isoformat(), *names)
#                for d, names in
#                data['bymonths'][month].items())
#     csv.writer(open(outfile, 'w')).writerows(outdata)
#     print(f'Data exported to {outfile}')


def export_month_csv(some_group_of_people):
    people_by_month = some_group_of_people['group_of_people_by_month']
    template = templates.get_template('ghwiki/Monthwise.md')
    if not os.path.exists(ghwiki_reports_dir):
        os.makedirs(ghwiki_reports_dir)
    with open(f'{ghwiki_reports_dir}/Monthwise.md', 'w') as report:
        report.write(template.render(people_by_month=people_by_month))

def place_reports():
    """ Right now just copies the _sidebar. Later might use this to write all the reports """
    copyfile(f'{templates_dir}/ghwiki/_Sidebar.md', f'{ghwiki_reports_dir}/_Sidebar.md')

def gen_ghwiki_reports():
    data = load_csv(leaves_csv_path)
    today_leaves = data['bydates'][datetime.date.today()]
    next_leaves_by_month_temp_jar = get_next_leaves_by_month(data['bydates'])
    next_leaves_by_month = ((calendar.month_name[month], leaves)
                            for month, leaves
                            in next_leaves_by_month_temp_jar.items())
    export_month_csv(data)

    template = templates.get_template('ghwiki/Home.md')
    if not os.path.exists(ghwiki_reports_dir):
        os.makedirs(ghwiki_reports_dir)
    with open(f'{ghwiki_reports_dir}/Home.md', 'w') as report:
        report.write(template.render(today_leaves=today_leaves,
                                     next_leaves_by_month=next_leaves_by_month))

    place_reports()

    return ghwiki_reports_dir


def upload_ghwiki_reports():
    raise NotImplementedError
