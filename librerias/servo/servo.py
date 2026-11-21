# Servomotor de posicion (SG90, MG90S, MG996R y parecidos) con PWM a 50 Hz.
#
#   from servo import Servo
#   s = Servo(pin=13)
#   s.angulo(90)
#
# Conexion: cable cafe/negro a GND, rojo a 5 V (de una fuente aparte si el servo es grande:
# el USB de la placa no alcanza), naranja/amarillo (senal) al pin. Une el GND de la fuente
# con el GND de la placa.
from machine import Pin, PWM

_PERIODO_US = 20000   # 50 Hz


class Servo:
    def __init__(self, pin, min_us=500, max_us=2400, grados_max=180):
        # min_us/max_us: el pulso que lleva el servo a 0 y a grados_max. Si tu servo no llega al
        # final o choca con el tope, ajusta estos dos (los SG90 suelen andar entre 500 y 2400).
        self._pwm = PWM(Pin(pin), freq=50)
        self._min = min_us
        self._max = max_us
        self._grados_max = grados_max
        self._angulo = None

    def pulso_us(self, us):
        """Manda un pulso de `us` microsegundos (lo normal es usar angulo())."""
        us = max(self._min, min(self._max, int(us)))
        self._pwm.duty_u16(us * 65535 // _PERIODO_US)

    def angulo(self, grados):
        """Lleva el servo al angulo indicado (0 a grados_max; si te pasas, se queda en el tope)."""
        grados = max(0, min(self._grados_max, grados))
        self._angulo = grados
        self.pulso_us(self._min + (self._max - self._min) * grados / self._grados_max)

    def leer(self):
        """El ultimo angulo que se pidio (None si todavia no se movio)."""
        return self._angulo

    def apagar(self):
        """Suelta el servo: deja de mandar pulsos (no hace fuerza ni vibra). angulo() lo vuelve a mover."""
        self._pwm.duty_u16(0)
