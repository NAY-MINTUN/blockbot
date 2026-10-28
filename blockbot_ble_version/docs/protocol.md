# BlockBot Bluetooth Protocol (version 1)

## A. Names and addresses

- Device name : BlockBot-01 
- Service (the room) : 34584cb7-05bf-4681-b563-54ed1c91e225
- Command (app writes to arm) : 4c2623f2-143b-4c9d-a8a8-3975a0c4cbf2
- Events (arm notifies app) : 393f559f-5843-446b-81d6-0323fba9b913
- Manifest (app reads parts list) : 2ab93832-1350-40bf-a2b6-aa87881dd88b

## B. Joint numbers

| Number | Joint | Servo channel |
|--------|-------|---------------|
| 0 | Base | 0 | 
| 1 | In / Out | 1 | 
| 2 | Up / Down | 2 | 
| 3 | Gripper | 3 | 


## C. Messages from the app to the arm

### MOVE (0x01)
Bytes : 0x01, seq, joint, angle, speed
- joint : 0 to 3
- angle : 0 to 180
- speed : 0 to 10
Only works in code mode, and when STOP is not active
Reply : DONE (same seq) when the move finishes, or ERROR

### SET_SPEED (0x02) 
Bytes : 0x02, seq, speed
- speed : 1 to 10
Set the default speed for later moves
Reply : ERROR code 4 if the speed is invalid. Otherwise no reply

### Stop (0x03)
Bytes : 0x03, seq
Cancel every active move at once. New moves are refused until the STOP is reset
Reply : STATE with stop = 1 now, and STATE with stop = 0 when the 5 seconds end.

### SET_MODE (0x04)
Bytes : 0x04, seq, mode
- mode: 0 = code mode, 1 = joystick mode
In code mode, blocks control the arm and the joysticks are ignored.
In joystick mode, the joysticks control the arm and every MOVE is refused.
Switching mode cancels any move in progress. The arm holds its position.
Reply: STATE with the new mode.


### SET_LIMITS (0x05)
Bytes : 0x05, seq, joint, min, max
- joint : 0 to 3
- min and max : 0 to 180, and min must be smaller than max
The app sends this once for each joint (four messages) right after connecting. 
Reply : ERROR code 2 for a bad joint, ERROR code 6 if the message is too short. Otherwise no reply

### PING (0x06)
Bytes : 0x06, seq
Heartbeat. The app send it about once per second so that the arm knows the app is alive. 
Reply : none

### Speed table
| Speed | Degrees per second | 
|-------|--------------------|
| 1 | 10 |
| 2 | 20 |
| 3 | 30 |
| 4 | 40 |
| 5 | 60 |
| 6 | 80 |
| 7 | 100 |
| 8 | 120 |
| 9 | 150 |
| 10 | 180 |



## D. Messages from the arm to to app

Events use opcodes from 0x81 upward, so they can never be confused with messages from the app.
 
### DONE (0x81)
Bytes: 0x81, seq
Sent when the move with that seq has finished
 
### ERROR (0x82)
Bytes: 0x82, seq, code
Sent when the arm refuses a message
 
### POSITIONS (0x83)
Bytes: 0x83, base, in_out, up_down, gripper
The current angle of each joint, in the order of section B
Sent about 5 times per second while the arm is moving
 
### STATE (0x84)
Bytes: 0x84, mode, stop
- mode: 0 = code mode, 1 = joystick mode
- stop: 1 = STOP is active (moves are ignored), 0 = normal
Sent when the app connects, when the mode changes, when STOP starts, and when STOP ends after 5 seconds.
The app uses it to show the mode button and to enable the Run button again.


## E. Error codes

| Code | Meaning | What the app tells the user |
|------|---------|--------------------------------|
| 1 | Unknown opcode | Something went wrong. Please update the app. |
| 2 | Bad joint number | That joint does not exist. |
| 3 | Angle outside the limits | That joint cannot go that far. Check its limits. |
| 4 | Bad speed | Speed must be from 1 to 10. |
| 5 | Stop is active | The program was stopped. Wait a few seconds, then run again. |
| 6 | Message too short | The message was damaged. Try again. |
| 7 | Wrong mode | The arm is in joystick mode. Switch to code mode to run blocks. |



## F. Parts list (manifest)

{
  "v": 1,
  "type": "arm",
  "parts": [
    {"t": "servo", "id": 0, "name": "base"},
    {"t": "servo", "id": 1, "name": "in/out"},
    {"t": "servo", "id": 2, "name": "up/down"},
    {"t": "servo", "id": 3, "name": "gripper"},
    {"t": "joystick", "id": 0, "mode": "local"},
    {"t": "joystick", "id": 1, "mode": "local"}
  ]
}

## G. Safety rules

1. The arm must refuse a MOVE outside the joint's limits and reply ERROR code 3. It never changes the angle quietly.
2. The arm must keep its limits in its own memory, so they survive a restart.
3. The app sends PING about once per second. If the arm hears nothing for 1.5 seconds, it must stop moving.
4. If the Bluetooth connection drops, the arm must stop moving, go back to joystick mode and start advertising again.
5. Only one controller works at a time. In code mode the joysticks are ignored. In joystick mode every MOVE is refused with ERROR code 7.
6. Changing the mode cancels any move in progress, and the arm holds its position.
7. STOP stops the program. It is not an emergency stop and not a safety device.
8. After STOP, the arm ignores every MOVE for 5 seconds (ERROR code 5), then resets by itself and sends STATE with stop = 0.
9. The joysticks must still obey the joint limits.
10. The arm must refuse a MOVE or SET_SPEED with a speed outside 1 to 10 (ERROR code 4).



## H. Worked examples

### A good move
1. A student's block says: move base to 90 degrees at speed 5.
2. The app picks message number 7 and sends: 01 07 00 5a 05
3. The arm moves the base slowly toward 90 degrees.
4. When it arrives, the arm sends: 81 07
5. The app sees DONE with seq 7 and runs the next block.
 
### A refused move
1. A block asks In / Out to go to 170 degrees, but its limit is 125.
2. The app picks message number 8 and sends: 01 08 01 aa 05
3. The arm refuses and sends: 82 08 03 (message 8, code 3, outside the limits)
4. The app shows: That joint cannot go that far. Check its limits.
5. The arm did not move at all.
 
### Pressing STOP
1. The student presses STOP. The app stops sending the blocks below it and sends: 03 09
2. The arm cancels its move and replies: 84 00 01 (code mode, stop active)
3. If a stray MOVE still arrives, the arm answers ERROR code 5 and does not move.
4. After 5 seconds the arm resets by itself and sends: 84 00 00
5. The app enables the Run button again.
 
### Switching to joystick mode
1. The student presses the mode button. The app sends: 04 0a 01
2. The arm cancels any move in progress and replies: 84 01 00 (joystick mode)
3. The joysticks now move the arm. Blocks are refused with ERROR code 7.
4. Pressing the button again sends 04 0b 00. The arm replies 84 00 00 and the joysticks are ignored.
