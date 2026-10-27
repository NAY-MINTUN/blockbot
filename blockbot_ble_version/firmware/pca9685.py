import time
 
class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self._write(0x00, 0x00)
 
    def _write(self, reg, value):
        self.i2c.writeto_mem(self.address, reg, bytes([value]))
 
    def _read(self, reg):
        return self.i2c.readfrom_mem(self.address, reg, 1)[0]
 
    def freq(self, freq):
        prescale = int(25000000.0 / (4096.0 * freq) + 0.5) - 1
        old = self._read(0x00)
        self._write(0x00, (old & 0x7F) | 0x10)
        self._write(0xFE, prescale)
        self._write(0x00, old)
        time.sleep_ms(5)
        self._write(0x00, old | 0xA1)
 
    def channel(self, index, off):
        base = 0x06 + 4 * index
        self.i2c.writeto_mem(self.address, base,
                             bytes([0, 0, off & 0xFF, off >> 8]))
