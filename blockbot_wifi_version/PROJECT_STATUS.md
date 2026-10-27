# BlockBot Project Status

**Updated:** 2026-09-29

## Current stage

BlockBot has a browser-based Blockly interface, a Python/FastAPI relay, and
MicroPython firmware for an ESP32 robot arm. The current working tree includes
uncommitted changes across the backend, firmware, and frontend.

## Implemented in the current working tree

- Account sign-up and login with locally stored accounts and sessions.
- Per-account device and Blockly program state saved in SQLite.
- Device discovery and manual WebSocket device configuration.
- Browser-to-ESP32 command relay with command and joint-limit validation.
- ESP32 control of four PCA9685 servo channels and two physical joysticks.
- Browser STOP control for stopping a running Blockly program.
- Offline joystick operation: the joystick task starts in Wi-Fi setup mode,
  using firmware defaults until the browser supplies custom limits.
- VS Code/MicroPico guidance for transferring firmware files to the ESP32.

## Hardware setup

The documented build uses an ESP32, PCA9685 servo driver, four servos, and two
optional KY-023 joysticks. Servos require a separate regulated 5 V supply with
common ground. Joystick pins are GPIO 32–35; PCA9685 I2C uses GPIO 21 and 22.

## Validation status and next steps

- Offline joystick behavior has not been verified on ESP32 hardware.
- No automated `tests/` directory is present in this checkout.
- Upload the firmware and check startup output in a serial terminal.
- Test joystick calibration and movement with the arm clear and conservative
  joint limits.
- Test browser login, saved state, device connection, Blockly movement, STOP,
  and behavior when Wi-Fi disconnects.
- Confirm the exact board model and verify MicroPico serial upload. Its
  documentation describes ESP32-WROOM support as experimental.

## Known limitations

- If saved Wi-Fi credentials cannot connect, firmware startup waits up to
  20 seconds before entering setup mode; joystick control becomes available
  after startup and calibration.
- Browser-configured joint limits replace firmware defaults while running and
  are supplied again when the browser reconnects after a reboot.
- The browser and server are not required for local joystick movement, but are
  required for Blockly control and account/device management.
