def encode_move(seq, joint, angle, speed):
    return bytes([0x01, seq, joint, angle, speed])
 
 
def encode_set_mode(seq, mode):
    return bytes([0x04, seq, mode])
 
 
def decode_event(data):
    opcode = data[0]
    if opcode == 0x81:
        return {"name": "DONE", "seq": data[1]}
    if opcode == 0x82:
        return {"name": "ERROR", "seq": data[1], "code": data[2]}
    if opcode == 0x83:
        return {"name": "POSITIONS", "angles": list(data[1:5])}
    if opcode == 0x84:
        return {"name": "STATE", "mode": data[1], "stop": data[2]}
    return {"name": "UNKNOWN"}
 
 
print(encode_move(7, 0, 90, 5).hex())
print(decode_event(bytes([0x81, 7])))
print(decode_event(bytes([0x82, 7, 3])))
print(encode_set_mode(10, 1).hex())
print(decode_event(bytes([0x84, 0, 1])))
