import time

def getLight(screenBrightnessFile="/sys/class/backlight/intel_backlight/brightness"):
    '''
    reads the brightness file and get the light value
    '''
    with open(screenBrightnessFile, "r") as bf:
        return bf.read().replace("\n","")
def changeLight(amount:str,screenBrightnessFile="/sys/class/backlight/intel_backlight/brightness"):
    '''
    changes the light value in the brightness file with the amount variable.
    Does require root!
    '''
    if int(amount) > int(852):
        return "amount cannot be heigher than 852!"
    elif int(amount) < int(0):
        return "amount cannot be smaller than 0!"
    else:
        try:
            with open(screenBrightnessFile, "w") as bf:
                bf.write(amount)    
        except PermissionError as e:
            return f"cannot read file \"{e.filename}\"\nare you sudo?"


currentLight = getLight()
while True:
    #if getLight() != currentLight:
        time.sleep(70)
        #print("light changed")
        #print(getLight())
        #time.sleep(1)
        changeLight(currentLight)
