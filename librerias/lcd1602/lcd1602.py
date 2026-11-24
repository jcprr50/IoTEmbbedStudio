# Pantalla LCD de caracteres (1602 o 2004) con la mochila I2C PCF8574.
#
#   from machine import I2C, Pin
#   from lcd1602 import LCD1602
#   i2c = I2C(0, sda=Pin(21), scl=Pin(22))
#   lcd = LCD1602(i2c)              # direccion 0x27 (si no funciona, prueba 0x3F)
#   lcd.escribir("Hola", 0, 0)
#
# Conexion: VCC a 5 V, GND, SDA y SCL a los pines I2C de la placa.
from time import sleep_ms, sleep_us

_RS = 0x01
_E = 0x04
_LUZ = 0x08


class LCD1602:
    def __init__(self, i2c, direccion=0x27, columnas=16, filas=2):
        self._i2c = i2c
        self._dir = direccion
        self.columnas = columnas
        self.filas = filas
        self._luz = _LUZ
        sleep_ms(50)
        # Secuencia de arranque en modo de 4 bits.
        for _ in range(3):
            self._nibble(0x30, 0)
            sleep_ms(5)
        self._nibble(0x20, 0)
        self._comando(0x28)   # 4 bits, 2 lineas
        self._comando(0x0C)   # pantalla encendida, sin cursor
        self._comando(0x06)   # el cursor avanza a la derecha
        self.limpiar()

    def _poner(self, dato):
        self._i2c.writeto(self._dir, bytes([dato | self._luz]))

    def _nibble(self, valor, modo):
        v = (valor & 0xF0) | modo
        self._poner(v)
        self._poner(v | _E)
        sleep_us(1)
        self._poner(v)
        sleep_us(50)

    def _byte(self, valor, modo):
        self._nibble(valor & 0xF0, modo)
        self._nibble((valor << 4) & 0xF0, modo)

    def _comando(self, c):
        self._byte(c, 0)

    def limpiar(self):
        """Borra toda la pantalla."""
        self._comando(0x01)
        sleep_ms(2)

    def cursor(self, columna, fila):
        """Pone el cursor en la columna y fila indicadas (empiezan en 0)."""
        fila = min(fila, self.filas - 1)
        base = (0x00, 0x40, self.columnas, 0x40 + self.columnas)[fila]
        self._comando(0x80 | (base + columna))

    def escribir(self, texto, columna=None, fila=None):
        """Escribe texto. Con columna y fila lo pone ahi; sin ellas sigue donde quedo el cursor."""
        if columna is not None:
            self.cursor(columna, fila or 0)
        for c in str(texto):
            n = ord(c)
            self._byte(n if n < 256 else 63, _RS)

    def linea(self, fila, texto):
        """Reemplaza una fila completa (rellena con espacios para borrar lo anterior)."""
        t = str(texto)[:self.columnas]
        self.escribir(t + " " * (self.columnas - len(t)), 0, fila)

    def luz(self, encendida=True):
        """Enciende o apaga la luz de fondo."""
        self._luz = _LUZ if encendida else 0
        self._poner(0)

    def cursor_visible(self, visible=True):
        self._comando(0x0E if visible else 0x0C)
