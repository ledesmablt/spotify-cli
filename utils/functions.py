from datetime import timedelta
def format_duration_ms(ms):
    def _format(d):
        d = str(d)
        if len(d) == 1:
            d = '0' + d
        return d

    s = int(ms / 1000)
    if s < 60:
        return f'00:{_format(s)}'

    m, s = divmod(s, 60)
    return f'{_format(m)}:{_format(s)}'
