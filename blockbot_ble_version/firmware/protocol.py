#names for the message number
OP_MOVE = 0x01
OP_SET_SPEED = 0x02
OP_STOP = 0x03
OP_SET_MODE = 0x04
OP_SET_LIMITS = 0x05
OP_PING = 0x06

#names for the messages sent by robot arm
EVENT_DONE = 0x81
EVENT_ERROR = 0x82
EVENT_POSITIONS = 0x83
EVENT_STATE = 0x84

#names of the errors codes (total 7)
ERROR_UNKNOWN_OPCODE = 1
ERROR_BAD_JOINT = 2
ERROR_OUT_OF_LIMITS = 3
ERROR_BAD_SPEED = 4
ERROR_STOP_ACTIVE = 5
ERROR_TOO_SHORT = 6
ERROR_WRONG_MODE = 7

#TWO MODE FOR BlockBot 0 == coding mode, 1 == joystick mode
MODE_CODE = 0
MODE_JOYSTICK =1

#list of how many bytes each message should have
COMMAND_LENGTHS = {
    OP_MOVE: 5, 
    OP_SET_SPEED: 3,
    OP_STOP: 2,
    OP_SET_MODE: 3,
    OP_SET_LIMITS: 5,
    OP_PING: 2
}

#problem for 2 kinds (error code and seq) for number of bad message
class ProtocolError(Exception):
    def __init__(self, code, seq):
        super().__init__(code)
        self.code = code
        self.seq = seq

#reads bytes, check, and return the opcode, the seq and other fields, if something wrong raise ProtocolError
def parse_command(data):
    
    if len(data)<2:
        raise ProtocolError(ERROR_TOO_SHORT, 0)
        
    opcode = data[0]
    seq = data[1]
    expected_length = COMMAND_LENGTHS.get(opcode)

    if expected_length is None:
        raise ProtocolError(ERROR_UNKNOWN_OPCODE, seq)

    if len(data) < expected_length:
        raise ProtocolError(ERROR_TOO_SHORT, seq)

    return opcode, seq, tuple(data[2:expected_length])


#3  functions to create the bytes the ar sends back
def build_done(seq):
    return bytes([EVENT_DONE, seq])

def build_error(seq, code):
    return bytes([EVENT_ERROR, seq, code])

def build_state(mode, stop_active):
    return bytes([EVENT_STATE, mode, stop_active])


#turn bytes into readable text for printing purpose
def describe_bytes(data):
    return " ".join("{:02x}".format(value) for value in data)

    
    























