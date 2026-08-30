LIMITS = {0: (0, 180), 1: (65, 125), 2: (30, 120), 3: (90, 150)}

def check(channel, angle):
    if isinstance(channel, bool) or not isinstance(channel, int):
        return False, 'channel must be an integer'
    if channel not in LIMITS:
        return False, 'unknown channel'
    if isinstance(angle, bool) or not isinstance(angle, (int, float)):
        return False, 'angle must be a number'
    low, high = LIMITS[channel]
    if not low <= angle <= high:
        return False, f'angle must be between {low} and {high} degrees'
    return True, 'ok'
