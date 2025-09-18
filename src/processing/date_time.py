from datetime import datetime, timedelta


def convert_to_dateString(date_object, format):
    """
    Convert a date object to a string in the given format
    """
    return datetime.strftime(date_object, format)


def convert_to_dateObject(date_string, format):
    """
    Convert a string to a date object in the given format
    """
    return datetime.strptime(date_string, format)
