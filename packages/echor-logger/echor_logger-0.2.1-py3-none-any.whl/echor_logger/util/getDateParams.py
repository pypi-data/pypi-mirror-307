from datetime import datetime


def convert_to_two_digit(digit):
    return f"{digit:02}"


def getDateParams(given_date=None):
    date = given_date or datetime.utcnow()
    month = convert_to_two_digit(date.month)
    day = convert_to_two_digit(date.day)
    year = date.year
    seconds = convert_to_two_digit(date.second)
    minutes = convert_to_two_digit(date.minute)
    hour = convert_to_two_digit(date.hour)

    return {
        "year": year,
        "month": month,
        "day": day,
        "seconds": seconds,
        "minutes": minutes,
        "hour": hour,
    }
