import sys
 
sys.path.insert(0, "blockbot_ble_version/firmware")
 
import protocol
 
 
def check(name, condition):
    if not condition:
        raise SystemExit("FAILED: " + name)
    print("ok:", name)
 
 
def parsed(*values):
    return protocol.parse_command(bytes(values))
 
 
def error_of(*values):
    try:
        parsed(*values)
    except protocol.ProtocolError as error:
        return error.code, error.seq
    return None
 
 
check("move", parsed(1, 7, 0, 90, 5) == (1, 7, (0, 90, 5)))
check("stop", parsed(3, 9) == (3, 9, ()))
check("set mode", parsed(4, 10, 1) == (4, 10, (1,)))
check("set limits", parsed(5, 11, 1, 40, 125) == (5, 11, (1, 40, 125)))
check("unknown opcode", error_of(0x99, 5) == (1, 5))
check("move too short", error_of(1, 6) == (6, 6))
check("empty message", error_of() == (6, 0))
check("build done", protocol.build_done(7) == bytes([0x81, 7]))
check("build error", protocol.build_error(8, 3) == bytes([0x82, 8, 3]))
check("build state", protocol.build_state(0, 1) == bytes([0x84, 0, 1]))
shown = protocol.describe_bytes(bytes([1, 7, 0, 90, 5]))
check("describe bytes", shown == "01 07 00 5a 05")
print("All protocol tests passed")
























