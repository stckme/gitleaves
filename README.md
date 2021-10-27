# File names
leaves.<YYYY>.csv
extras.<YYYY>.csv

# Format

Leaves
DDMM [- DDMM], Name

Extra days
DDMM [- DDMM], Name

Lines starting with comments are ignored

# Process
- Apply for leave(s) by adding records to leaves.YYYY.csv
- Optionally mention details/reasons in commit message
- Raise a PR
- Leave is approved if the PR is merged

# Guidelines
- Do take leaves when necessary :)
- Make sure you spell your name same everywhere
- Generally try to add records in reverse chronological order
- When applying for leaves
    - make sure you take look at peers leave plans 
    - ensure that you have a collegue to cover your work while you are away
    - if necessary, do essential knowledge transfer to ensure that there are no dependencies on you
    - if you are a major contributor to an important release then avoid immediate leaves after the release

# Dev Guidelines
- Human Readable data files (as much possible)
