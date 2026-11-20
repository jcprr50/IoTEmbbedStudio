# Sensor ultrasónico de distancia HC-SR04 (y compatibles: HY-SRF05, JSN-SR04T).
#
#   from hcsr04 import HCSR04
#   sensor = HCSR04(trig=5, echo=18)
#   cm = sensor.distancia_cm()
#
# Conexión: VCC a 5 V, GND, TRIG a un pin de salida y ECHO a un pin de entrada.
# OJO: el ECHO del HC-SR04 responde a 5 V y los pines del ESP32 aguantan 3,3 V:
# pon un divisor de voltaje (1 k + 2 k ohmios) entre ECHO y el pin, o usa un HC-SR04 de 3,3 V.
from machine import Pin, time_pulse_us
from time import sleep_us


class HCSR04:
    def __init__(self, trig, echo, espera_us=30000):
        # espera_us: cuánto esperar el eco. 30000 us ~ 5 m; si no hay eco, devuelve None.
        self._trig = Pin(trig, Pin.OUT, value=0)
        self._echo = Pin(echo, Pin.IN)
        self._espera = espera_us

    def _pulso_us(self):
        self._trig.value(0)
        sleep_us(5)
        self._trig.value(1)
        sleep_us(10)
        self._trig.value(0)
        try:
            t = time_pulse_us(self._echo, 1, self._espera)
        except OSError:
            return None
        return None if t < 0 else t

    def distancia_cm(self):
        """Distancia en centímetros, o None si no hubo eco (nada enfrente o demasiado lejos)."""
        t = self._pulso_us()
        # El sonido recorre ida y vuelta: 343 m/s = 0,0343 cm/us, dividido entre 2.
        return None if t is None else t * 0.01715

    def distancia_mm(self):
        """Distancia en milímetros, o None si no hubo eco."""
        cm = self.distancia_cm()
        return None if cm is None else cm * 10
