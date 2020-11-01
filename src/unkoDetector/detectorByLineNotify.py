# coding: utf-8
from measure import measure
from util import spiModule, LINENotifyBot
import RPi.GPIO as GPIO
import time
import os

def main():
    # Execute the following command in advance on the shell.
    # export "LINE_NOTIFY_KEY"=<YOUR_ACCESS_TOKEN>
    access_token = os.environ["LINE_NOTIFY_KEY"]
    bot = LINENotifyBot(access_token=access_token)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.OUT)
    GPIO.setup(22,GPIO.OUT)

    ch0 = 0x00
    spi = spiModule.setup()
    threshold = 160

    try:
        while 1:
            GPIO.output(22,True)
            time.sleep(0.500)

            ch0_val = measure(spi, ch0)
            val = 1023 - ch0_val
            print(val)
            if val > threshold:
                bot.send(
                    message = "うんちをしました！！"
                )

            GPIO.output(22,False)
            time.sleep(0.500)
            
            GPIO.output(17,True)
            time.sleep(0.500)

            GPIO.output(17,False)
            time.sleep(0.500)

    except KeyboardInterrupt:
        pass

    spi.close()

if __name__ == "__main__":
    main()