def measure(spi, ch):
    start = 0x47
    sgl = 0x20
    msbf = 0x08
    dummy = 0xff

    ad = spi.xfer2( [ (start + sgl + ch + msbf), dummy ] )
    val = ((ad[0] & 0x03) << 8) + ad[1]

    return val

def main():
    from util import spiModule

    ch0 = 0x00
    spi = spiModule.setup()

    print(measure(spi, ch0))
    
if __name__ == "__main__":
    main()