import math

JOINT_NAMES = {0: 'Base', 1: 'In/Out', 2: 'Up/Down', 3: 'Gripper'}


def check(channel, angle, custom_limits=None):
    if isinstance(channel, bool) or not isinstance(channel, int):
        return False, 'channel must be an integer'
    if channel not in JOINT_NAMES:
        return False, 'unknown channel'
    if isinstance(angle, bool) or not isinstance(angle, (int, float)) or not math.isfinite(angle):
        return False, 'angle must be a finite number'
    if not isinstance(custom_limits, list) or len(custom_limits) != 4:
        return False, 'Set limits for all joints before moving the arm.'
    try:
        low, high = custom_limits[channel]['min'], custom_limits[channel]['max']
        if (isinstance(low, bool) or isinstance(high, bool)
                or not isinstance(low, (int, float))
                or not isinstance(high, (int, float))
                or not math.isfinite(low) or not math.isfinite(high)
                or low < 0 or high > 180 or low >= high):
            raise ValueError
    except (KeyError, IndexError, TypeError, ValueError):
        return False, 'Invalid calibration limits.'
    joint = JOINT_NAMES[channel]
    if angle < low:
        return False, f'{joint} joint angle {angle}° is below its minimum limit of {low}°.'
    if angle > high:
        return False, f'{joint} joint angle {angle}° exceeds its maximum limit of {high}°.'
    return True, 'ok'
