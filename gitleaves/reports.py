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
if not os.path.exists(ghwiki_reports_dir):
    os.makedirs(ghwiki_reports_dir)

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


def gen_ghwiki_reports():
    data = load_csv(leaves_csv_path)
    today_leaves = data['bydates'][datetime.date.today()]
    next_leaves_by_month_temp_jar = get_next_leaves_by_month(data['bydates'])
    next_leaves_by_month = ((calendar.month_name[month], leaves)
                            for month, leaves
                            in next_leaves_by_month_temp_jar.items())
    people_by_month = data['bymonthnames_groupedby_applicants']

    template = templates.get_template('ghwiki/Monthwise.md')
    with open(f'{ghwiki_reports_dir}/Monthwise.md', 'w') as report:
        report.write(template.render(people_by_month=people_by_month))

    template = templates.get_template('ghwiki/Home.md')
    with open(f'{ghwiki_reports_dir}/Home.md', 'w') as report:
        report.write(template.render(today_leaves=today_leaves,
                                     next_leaves_by_month=next_leaves_by_month))

    with open(f'{ghwiki_reports_dir}/_Sidebar.md', 'w') as sidebar_file:
        sidebar_file.write(open(f'{templates_dir}/ghwiki/_Sidebar.md').read())

    return ghwiki_reports_dir


def upload_ghwiki_reports():
    raise NotImplementedError
