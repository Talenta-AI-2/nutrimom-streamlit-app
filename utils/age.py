from datetime import timezone, datetime

import dateutil

def age_years(date):
    # Get the current date
    now = datetime.now(timezone.utc)
    now = now.date()

    # Get the difference between the current date and the birthday
    age = dateutil.relativedelta.relativedelta(now, date)
    age = age.years

    return age

def age_months(date):
    # Get the current date
    now = datetime.now(timezone.utc)
    now = now.date()

    # Get the difference between the current date and the birthday
    age = dateutil.relativedelta.relativedelta(now, date)
    age = age.years * 12 + age.months

    return age