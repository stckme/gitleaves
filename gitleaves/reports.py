import arrow
import calendar
import csv
import datetime
import glob
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
if not os.path.exists(ghwiki_reports_dir):
    os.makedirs(ghwiki_reports_dir)

today = datetime.date.today()
leaves_csv_path_pat = os.path.join('data', 'leaves.{YYYY}.csv')
extras_csv_path_pat = os.path.join('data', 'extras.{YYYY}.csv')
extras_csv_path = extras_csv_path_pat.format(YYYY=today.year)

leaves_csv_paths = {int(path.split('leaves.')[1][:-4]): path
                    for path in
                    glob.glob(os.path.join('data', 'leaves.*.csv'))}


def ddmm2date(s):
    return arrow.get(f'{today.year}{s.strip()}')


def range2dates(daterange):
    """
    '1307 - 2907' →  [date(2021, 7, 13), ....]
    Except weekends
    """
    if '-' in daterange:
        start, end = [ddmm2date(d) for d in daterange.split('-')]
        dates = [start] if start == end else arrow.Arrow.range('day', start, end)
    elif '–' in daterange:
        start, end = [ddmm2date(d) for d in daterange.split('–')]
        dates = [start] if start == end else arrow.Arrow.range('day', start, end)
    else:
        dates = [ddmm2date(daterange)]
    return [d.date() for d in dates]


def load_csv(csv_path):
    bydates = defaultdict(list)
    bynames = defaultdict(list)
    bymonths = defaultdict(lambda: defaultdict(list))
    bymonthnames_groupedby_applicants = defaultdict(lambda: defaultdict(list))
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
            bymonthnames_groupedby_applicants[calendar.month_name[date.month]][applicant].append(date)

    return {'bydates': bydates, 'bynames': bynames, 'bymonths': bymonths, 'bymonthnames_groupedby_applicants': bymonthnames_groupedby_applicants}


def get_next_leaves_by_month(bydates):
    nextbymonths = defaultdict(lambda: defaultdict(list))
    for date, applicants in bydates.items():
        if date > today:
            nextbymonths[date.month][date] = applicants
    return nextbymonths


def gen_for_year(year, data):
    people_by_month = data['bymonthnames_groupedby_applicants']

    template = templates.get_template('ghwiki/Monthwise.md')
    with open(f'{ghwiki_reports_dir}/Monthwise.{year}.md', 'w') as report:
        report.write(template.render(people_by_month=people_by_month))


def gen_ghwiki_reports():
    for year, path in leaves_csv_paths.items():
        yr_data = load_csv(leaves_csv_path_pat.format(YYYY=year))
        gen_for_year(year, yr_data)
        if year == today.year:
            c_yr_data = yr_data  # current year data

    today_leaves = c_yr_data['bydates'][datetime.date.today()]
    _ = get_next_leaves_by_month(c_yr_data['bydates'])
    next_leaves_by_month = ((calendar.month_name[month], leaves)
                            for month, leaves
                            in _.items())

    template = templates.get_template('ghwiki/Home.md')
    with open(f'{ghwiki_reports_dir}/Home.md', 'w') as report:
        report.write(template.render(today_leaves=today_leaves,
                                     next_leaves_by_month=next_leaves_by_month,
                                     ))

    template = templates.get_template('ghwiki/_Sidebar.md')
    earlier_years = sorted(leaves_csv_paths.keys(), reverse=True)
    with open(f'{ghwiki_reports_dir}/_Sidebar.md', 'w') as report:
        report.write(template.render(today_leaves=today_leaves,
                                     next_leaves_by_month=next_leaves_by_month,
                                     earlier_years=earlier_years,
                                     c_year=today.year
                                     ))

    return ghwiki_reports_dir


def upload_ghwiki_reports():
    raise NotImplementedError
