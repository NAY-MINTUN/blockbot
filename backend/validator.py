LIMITS = { 0: (0, 180), 1:(65, 125), 2: (30, 120), 3: (90, 150) }

def check(channel, angle):
    if channel not in LIMITS:
        return False, 'unknown channel'
    low, high = LIMITS[channel]
    if not low <= angle <= high:
        return False, 'angle out of range'
    return True, 'ok'