from getDateParams import getDateParams


def formatTimestamp(timestamp=None):
    date_params = getDateParams(timestamp)
    return f"{date_params['year']}{date_params['month']}{date_params['day']}/{date_params['hour']}{date_params['minutes']}{date_params['seconds']}"
