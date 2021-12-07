# gitleaves

*Git Based Leaves management system*

Project status: Still in early stage but we use it in production

## Features
- Pull requests based leaves management. Most natural for software development team
- Github friendly workflow
- Generates github wiki friendly markdown reports. Markdown can be used by different static site generators too

## Specifications

### File names

- leaves.\<YYYY\>.csv
- extras.\<YYYY\>.csv

### Format

### Leaves
MMDD [- MMDD], Name, Reason / Details [Optional]

### Extra days
MMDD [- MMDD], Name, Reason / Details [Optional]

### Example


```
1115 - 1126, Tony Stark, Hawaii
1129 - 1210, Peter Parker,
1129 - 1202, Bruce Wayne,
1220 - 1224, Loki Laufeyson, Smell the flowers
```

## Usage

### Organization setup

- Create a git repo for your organization's leaves data
```bash
mkdir leavesdata
cd leavesdata
git init
mkdir data
fname=data/leaves.`date +%Y`.csv
# example data 
echo `1129 - 1202, Bruce Wayne,` >> $fname
echo `1220 - 1224, Loki Laufeyson, Smell the flowers` >> $fname
git commit -a
git push origin main
```
 
- Install gitleaves
```bash
pip install gitleaves
```

- Generate reports
```bash
gitleaves genreports
ls reports/
```

- Automate report generation
<TODO> Document github actions based report generation

## Process

- Apply for leave(s) by adding records to leaves.YYYY.csv
- Raise a PR
- Leave is approved if the PR is merged

## Dev Guidelines
- Human Readable data files (as much possible)

## TODO

## Credits

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage` project template.

- Cookiecutter: https://github.com/audreyr/cookiecutter
- audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
