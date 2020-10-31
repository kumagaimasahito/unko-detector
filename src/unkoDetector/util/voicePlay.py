import os

def voicePlay(voice):
    os.system('echo ' + voice + ' | sh ~/Laboratory/voice/voicePlay.sh')