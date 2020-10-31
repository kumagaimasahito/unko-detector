import spidev

def setup():
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz=1000000
    spi.bits_per_word=8
    return spi