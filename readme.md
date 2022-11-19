# Global Entry Checker
Specify your preferred enrollment center (id) and your last availability date for the Global Entry interview, and let the checker finds whether there are spots available.

## Prerequisites and Install
- python3, virtualenv, pip
```bash
# create virtual environment
python3 -m virtualenv venv
source venv/bin/activate

# install packages
python -m pip install -r requirement.txt
```

## Usage
1. Specify your preferred location id and your last available date in `preference.json`. 
  - datebefore: the last day to look for appointment. Date string format is "YYYY-MM-DD".
  - locations: a list of Enrollment Center IDs.
  - Enrollment center IDs can be found at `locations/all_locations.json`. If the file does not exist, generate it by running `python3 get_all_locations.py` (and format the json on your own).
2. run `python3 ge_checker.py`
3. It will list the available slots ordered by date/time. If no slot is available, it will list all locations that currently have available slots.

## Todo
- Automatically check every 60 seconds and send notifications (email?) to users when a slot is available.
