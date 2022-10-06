# This is a sample Python script.
import time
import random
import sys

from phue import Bridge


def rainbow_hue(lamp):
    hue = b.get_light(lamp, 'hue')
    b.set_light(lamp, 'hue', hue + 1000)


def toggle_lamp(lamp):
    if b.get_light(lamp, 'on'):
        b.set_light(lamp, 'on', False)
    else:
        b.set_light(lamp, 'on', True)


def glimmer_lamp(lamp, bri, sat, hue):
    hue_glimmer = maxmin_glimmer_hue(hue + random.randint(-2000, 2000))
    bri_glimmer = maxmin_glimmer254(bri + random.randint(-30, 30))
    sat_glimmer = maxmin_glimmer254(sat + random.randint(-30, 30))
    command = {'transitiontime': 10, 'on': True, 'bri': bri_glimmer, 'sat': sat_glimmer, 'hue': hue_glimmer}
    b.set_light(lamp, command)


def maxmin_glimmer_hue(glimmer):
    max = 65500
    if glimmer < 0:
        return 0
    elif glimmer > max:
        return max
    else:
        return glimmer


def maxmin_glimmer254(glimmer):
    max = 254
    if glimmer <= 0:
        return 1
    elif glimmer > max:
        return max
    else:
        return glimmer


def init_bridge(ip):
    b = Bridge(ip)
    # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
    b.connect()

    # Get the bridge state (This returns the full dictionary that you can explore)
    b.get_api()

    return b


# Press the green button in the gutter to run the script.
def glimmer():
    i = 0
    for lamp in lamps:
        # toggleLamp(lamp)
        # time.sleep(1)
        glimmer_lamp(lamp, lampsBri[i], lampsSat[i], lampsHue[i])
        # toggleLamp(lamp)
        i = i + 1


def turn_off_all():
    # turn off lamps
    for lamp in lamps:
        command = {'transitiontime': 10, 'on': False}
        b.set_light(lamp, command)
    # turn off blacklight
    for bl in blackLight:
        command = {'transitiontime': 10, 'on': False}
        b.set_light(bl, command)


def black_light():
    for bl in blackLight:
        if random.randint(0, 100) > 979:
            toggle_lamp(bl)


def black_light_turn_on():
    for bl in blackLight:
        command = {'transitiontime': 10, 'on': True}
        b.set_light(bl, command)


def black_light_turn_off():
    for bl in blackLight:
        command = {'transitiontime': 10, 'on': False}
        b.set_light(bl, command)


def everything_off_effect(percentage):
    if random.randint(0, 100) > percentage:
        turn_off_all()
        return True
    return False


def just_blacklight(percentage):
    if random.randint(0, 100) > percentage:
        turn_off_all()
        black_light_turn_on()
        return True
    return False


def flash_light_effect(percentage):
    if random.randint(0, 100) > percentage:
        turn_off_all()
        circle = [1, 26, 17, 24, 53, 2, 52]
        for _ in range(random.randint(2, 5)):
            for lamp in lamps:
                command = {'on': True, 'bri': 254, 'sat': 254, 'hue': 10000}
                b.set_light(lamp, command)
                time.sleep(0.3)
                command = {'on': False}
                b.set_light(lamp, command)
                time.sleep(0.3)


# 1 -> Flur 2 -> Stehlampe, 15 -> hintersofa(LightStrip), 17 -> Wäschelampe, 24 -> hinter TV, 26 -> hinter sofa(bulb),
# 53 Pflanzenlampe 2, 42 weinkiste, 20 Deckenleuchte Wohnzimmer, 52 planze 1
if __name__ == '__main__':
    ip = sys.argv[1]
    b = init_bridge(ip)
    lamps = [15, 1, 24, 26, 42, 53, 2, 52]
    blackLight = [50, 48]
    lampsHue = []
    lampsBri = []
    lampsSat = []

    for lamp in lamps:
        lampsHue.append(b.get_light(lamp, 'hue'))
        lampsSat.append(b.get_light(lamp, 'sat'))
        lampsBri.append(b.get_light(lamp, 'bri'))

    while True:
        flash_light_effect(99)

        if just_blacklight(99):
            time.sleep(random.randint(30, 120))
            black_light_turn_off()

        if not everything_off_effect(99):
            glimmer()
            black_light()
            time.sleep(1)
        else:
            time.sleep(random.randint(5, 15))
            if just_blacklight(500):
                time.sleep(random.randint(10, 30))
                black_light_turn_off()
            else:
                flash_light_effect(500)


