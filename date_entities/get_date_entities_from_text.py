import datefinder


def get_date_entities_from_text(text):
    dates = datefinder.find_dates(text)
    return [{"date": date} for date in dates]
