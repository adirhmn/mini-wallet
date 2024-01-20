import arrow

def formatted_datetime(datetime) -> str:
    # Parsing to arrow object
    arrow_datetime = arrow.get(datetime).shift(hours=7).replace(tzinfo='Asia/Jakarta')

    # change format and timezone
    formatted_datetime = arrow_datetime.format("YYYY-MM-DDTHH:mm:ssZZ")

    return formatted_datetime
