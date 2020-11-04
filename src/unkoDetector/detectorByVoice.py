# coding: utf-8
from measure import measure
from util import spiModule, voicePlay
import RPi.GPIO as GPIO
import time

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.OUT)
    GPIO.setup(22,GPIO.OUT)

    ch0 = 0x00
    spi = spiModule.setup()
    trial = 50
    outlier = 10
    threshold_list = [0.0]*trial
    scaling = 0.05
    
    # Warming up to remove outliers．
    print("ウォームアップを開始します")
    for i in range(20):
        GPIO.output(22,True)
        GPIO.output(17,True)
        time.sleep(0.050)
        GPIO.output(22,False)
        GPIO.output(17,False)
        time.sleep(0.050)
    for i in tqdm(range(outlier)):
        GPIO.output(22,True)
        time.sleep(0.100)
        
        GPIO.output(22,False)
        time.sleep(0.100)
            
        GPIO.output(17,True)
        time.sleep(0.100)

        GPIO.output(17,False)
        time.sleep(0.100)
    print("ウォームアップが終了しました")

    # Trials for Threshold Determination.
    print("基準値の測定を開始します")
    for i in range(20):
        GPIO.output(22,True)
        GPIO.output(17,True)
        time.sleep(0.050)
        GPIO.output(22,False)
        GPIO.output(17,False)
        time.sleep(0.050)
    for i in tqdm(range(trial)):
        GPIO.output(22,True)
        time.sleep(0.100)

        ch0_val = measure(spi, ch0)
        val = 1023 - ch0_val
        threshold_list[i] = val
        
        GPIO.output(22,False)
        time.sleep(0.100)
            
        GPIO.output(17,True)
        time.sleep(0.100)

        GPIO.output(17,False)
        time.sleep(0.100)
    threshold = sum(threshold_list) / len(threshold_list)
    #bot.send(message = "基準値を" + str(threshold) + "に決定しました．")
    print("基準値を" + str(threshold) + "に決定しました")

    try:
        while 1:
            GPIO.output(22,True)
            time.sleep(0.500)

            ch0_val = measure(spi, ch0)
            val = 1023 - ch0_val
            print(val)
            if val > threshold*(1.0+scaling):
                # When a fecal scent is detected, an audio file is played back.
                # You can choose how to play it back according to your own environment.
                voice = "うんこのにおいがします．はやくかたづけてください"
                voicePlay(voice)

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