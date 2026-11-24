# Acelerometro y giroscopio MPU6050 (GY-521) por I2C.
#
#   from machine import I2C, Pin
#   from mpu6050 import MPU6050
#   i2c = I2C(0, sda=Pin(21), scl=Pin(22))
#   imu = MPU6050(i2c)
#   ax, ay, az = imu.aceleracion()
#
# Conexion: VCC a 3.3 V, GND, SDA y SCL a los pines I2C. Direccion 0x68 (0x69 si AD0 va a 3.3 V).
import struct
from math import atan2, sqrt, pi


class MPU6050:
    def __init__(self, i2c, direccion=0x68):
        self._i2c = i2c
        self._dir = direccion
        self._i2c.writeto_mem(direccion, 0x6B, b"\x00")   # sale del modo de reposo
        self._i2c.writeto_mem(direccion, 0x1C, b"\x00")   # acelerometro +-2 g
        self._i2c.writeto_mem(direccion, 0x1B, b"\x00")   # giroscopio +-250 grados/s

    def _leer(self, registro, n):
        return self._i2c.readfrom_mem(self._dir, registro, n)

    def aceleracion(self):
        """(x, y, z) en g (1.0 = la gravedad). Quieto y plano, z vale cerca de 1."""
        x, y, z = struct.unpack(">hhh", self._leer(0x3B, 6))
        return (x / 16384, y / 16384, z / 16384)

    def giro(self):
        """(x, y, z) en grados por segundo."""
        x, y, z = struct.unpack(">hhh", self._leer(0x43, 6))
        return (x / 131, y / 131, z / 131)

    def temperatura(self):
        """Temperatura del chip en grados Celsius."""
        (t,) = struct.unpack(">h", self._leer(0x41, 2))
        return t / 340 + 36.53

    def inclinacion(self):
        """(cabeceo, alabeo) en grados, calculados con la gravedad. Solo sirve con la placa quieta."""
        ax, ay, az = self.aceleracion()
        cabeceo = atan2(-ax, sqrt(ay * ay + az * az)) * 180 / pi
        alabeo = atan2(ay, az) * 180 / pi
        return (cabeceo, alabeo)
