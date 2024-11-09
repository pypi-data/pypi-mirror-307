def seconds_to_human_string(seconds: float):

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    format_string = ''

    if days > 0:
        format_string = f'{days}d'

    if hours > 0:
        format_string = f'{format_string}{hours}h '

    if minutes > 0:
        format_string = f'{format_string}{minutes}m '

    formatted_seconds = '{s:.2f}'.format(
        s=seconds
    )

    format_string = f'{format_string}{formatted_seconds}s'

    return format_string