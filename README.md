## BlockBot

## Hardware

-ESP32 + PCA9685 servo driver
- 1x MG996R (base), 3x MG90s (joints, and gripper)
- ** Servos runs from a SEPERATE 5V supply into PCA9685's V+ --**

Wiring (ESP32 -> PCA9685): 3.3V -> VCC, GND -> GND,
GPIO 21 -> SDA, GPIO 22 -> SCL. All grounds common. 

| Channel | Joint     | Servo  | Range    |
|---------|-----------|--------|----------|
| 0       | Base      | MG996R | 0-180    |
| 1       | Up/down   | MG90s  | 65-125   |
| 2       | In/out    | MG90s  | 30-120   |
| 3       | Gripper   | MG90s  | 93-150   |

