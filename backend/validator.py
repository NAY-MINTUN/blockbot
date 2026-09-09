LIMITS = {0: (0, 180), 1: (40, 125), 2: (30, 130), 3: (90, 150)}
JOINT_NAMES = {
    0: 'Base',
    1: 'In/Out',
    2: 'Up/Down',
    3: 'Gripper',
}

def check(channel, angle):
    if isinstance(channel, bool) or not isinstance(channel, int):
        return False, 'channel must be an integer'
    if channel not in LIMITS:
        return False, 'unknown channel'
    if isinstance(angle, bool) or not isinstance(angle, (int, float)):
        return False, 'angle must be a number'
    low, high = LIMITS[channel]
    joint = JOINT_NAMES[channel]
    if angle < low:
        return False, (
            f'{joint} joint angle {angle}° is below its minimum limit of {low}°.'
        )
    if angle > high:
        return False, (
            f'{joint} joint angle {angle}° exceeds its maximum limit of {high}°.'
        )
    return True, 'ok'
