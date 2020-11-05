# coding: utf-8
from measure import measure
from util import spiModule, LINENotifyBot
import RPi.GPIO as GPIO
import time
import os
from tqdm import tqdm
import requests

def main():
    # Execute the following command in advance on the shell.
    # export "LINE_NOTIFY_KEY"=<YOUR_ACCESS_TOKEN>
    access_token = os.environ["LINE_NOTIFY_KEY"]
    bot = LINENotifyBot(access_token=access_token)
    bot.send(message = "においの検出を開始しました")
    
    # Setting up a Google spreadsheet to enter sensor data
    # export "GAS_URL"=<YOUR_GAS_URL>
    gas_url = os.environ["GAS_URL"]

    # Setting of GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.OUT)
    GPIO.setup(22,GPIO.OUT)

    ch0 = 0x00
    spi = spiModule.setup()
    judge = False
    trial = 100
    outlier = 20
    threshold_list = [0]*trial
    scaling = 0.25

    # Warming up to remove outliers．
    print("ウォームアップを開始します")
    for i in tqdm(range(outlier)):
        GPIO.output(22,True)
        time.sleep(0.005)
        GPIO.output(22,False)
        GPIO.output(17,True)
        time.sleep(0.008)
        GPIO.output(17,False)
        time.sleep(0.237)
    print("ウォームアップが終了しました")

    # Trials for Threshold Determination.
    print("基準値の測定を開始します")
    for i in tqdm(range(trial)):
        GPIO.output(22,True)
        time.sleep(0.005)
        ch0_val = measure(spi, ch0)
        GPIO.output(22,False)
        GPIO.output(17,True)
        time.sleep(0.008)
        GPIO.output(17,False)
        time.sleep(0.237)
        val = 1023 - ch0_val
        threshold_list[i] = val
    threshold = sum(threshold_list) / len(threshold_list)
    #bot.send(message = "基準値を" + str(threshold) + "に決定しました．")
    print("基準値を" + str(threshold) + "に決定しました")

    try:
        while 1:
            GPIO.output(22,True)
            time.sleep(0.005)
            ch0_val = measure(spi, ch0)
            val = 1023 - ch0_val
            GPIO.output(22,False)
            GPIO.output(17,True)
            time.sleep(0.008)
            GPIO.output(17,False)
            time.sleep(0.237)
            print(val)
            requests.get(gas_url + "?data=" + str(val))
            if val > threshold*(1.0+scaling) and judge == False:
                judge = True
                bot.send(
                    message = "出たよ！！",
                    image = "/home/pi/Laboratory/unkoDetector/src/unkoDetector/photo/mafuyu.jpeg"
                )
            elif val < threshold*(1.0+scaling) and judge == True:
                judge = False
                bot.send(
                    message = "片付けてくれてありがとう！！",
                    image = "/home/pi/Laboratory/unkoDetector/src/unkoDetector/photo/latte.jpeg"
                )

    except KeyboardInterrupt:
        GPIO.output(22,False)
        GPIO.output(17,False)

    spi.close()

if __name__ == "__main__":
    main()
