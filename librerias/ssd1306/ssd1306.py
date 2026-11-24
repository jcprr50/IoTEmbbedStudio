# Pantalla OLED SSD1306 (128x64 o 128x32) por I2C.
#
#   from machine import I2C, Pin
#   from ssd1306 import SSD1306
#   i2c = I2C(0, sda=Pin(21), scl=Pin(22))
#   oled = SSD1306(i2c)
#   oled.texto("Hola", 0, 0)
#   oled.mostrar()
#
# Todo lo que se dibuja queda en memoria hasta llamar a mostrar().
# Conexion: VCC a 3.3 V, GND, SDA y SCL a los pines I2C. Direccion 0x3C (a veces 0x3D).
import framebuf


class SSD1306:
    def __init__(self, i2c, ancho=128, alto=64, direccion=0x3C):
        self._i2c = i2c
        self._dir = direccion
        self.ancho = ancho
        self.alto = alto
        self._buf = bytearray(ancho * alto // 8)
        self._fb = framebuf.FrameBuffer(self._buf, ancho, alto, framebuf.MONO_VLSB)
        for c in (0xAE, 0x20, 0x00, 0x40, 0xA1, 0xA8, alto - 1, 0xC8, 0xD3, 0x00,
                  0xDA, 0x02 if alto == 32 else 0x12, 0xD5, 0x80, 0xD9, 0xF1, 0xDB, 0x30,
                  0x81, 0xCF, 0xA4, 0xA6, 0x8D, 0x14, 0xAF):
            self._cmd(c)
        self.limpiar()
        self.mostrar()

    def _cmd(self, c):
        self._i2c.writeto(self._dir, bytes([0x80, c]))

    def limpiar(self, color=0):
        """Borra todo (color 0 = apagado, 1 = encendido)."""
        self._fb.fill(color)

    def texto(self, texto, x, y, color=1):
        """Escribe texto de 8x8 pixeles en la posicion x, y (0,0 es la esquina de arriba a la izquierda)."""
        self._fb.text(str(texto), x, y, color)

    def pixel(self, x, y, color=1):
        self._fb.pixel(x, y, color)

    def linea(self, x1, y1, x2, y2, color=1):
        self._fb.line(x1, y1, x2, y2, color)

    def rect(self, x, y, ancho, alto, color=1, relleno=False):
        if relleno:
            self._fb.fill_rect(x, y, ancho, alto, color)
        else:
            self._fb.rect(x, y, ancho, alto, color)

    def contraste(self, valor):
        """Brillo de 0 a 255."""
        self._cmd(0x81)
        self._cmd(max(0, min(255, int(valor))))

    def invertir(self, si=True):
        self._cmd(0xA7 if si else 0xA6)

    def apagar(self):
        self._cmd(0xAE)

    def encender(self):
        self._cmd(0xAF)

    def mostrar(self):
        """Pasa lo dibujado a la pantalla."""
        for c in (0x21, 0, self.ancho - 1, 0x22, 0, self.alto // 8 - 1):
            self._cmd(c)
        self._i2c.writeto(self._dir, b"\x40" + self._buf)
