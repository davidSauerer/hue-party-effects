# This is a sample Python script.
import time
import random
import argparse

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
    hue_glimmer = maxmin_glimmer(hue + random.randint(-2000, 2000), 65500)
    bri_glimmer = maxmin_glimmer(bri + random.randint(-30, 30), 254)
    sat_glimmer = maxmin_glimmer(sat + random.randint(-30, 30), 254)
    command = {'transitiontime': 10, 'on': True, 'bri': bri_glimmer, 'sat': sat_glimmer, 'hue': hue_glimmer}
    b.set_light(lamp, command)


def maxmin_glimmer(glimmer, max_value):
    if glimmer <= 0:
        return 1
    elif glimmer > max_value:
        return max_value
    else:
        return glimmer


def do_glimmer():
    i = 0
    for lamp in lamps:
        glimmer_lamp(lamp, lampsBri[i], lampsSat[i], lampsHue[i])
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


def flash_light_effect(percentage, circle):
    if random.randint(0, 100) > percentage:
        turn_off_all()
        for _ in range(random.randint(2, 5)):
            for lamp in circle:
                command = {'on': True, 'bri': 254, 'sat': 254, 'hue': 10000}
                b.set_light(lamp, command)
                time.sleep(0.3)
                command = {'on': False}
                b.set_light(lamp, command)
                time.sleep(0.3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Personal information')
    parser.add_argument('--ip', dest='ip', type=str, help='IP of the hue bridge')
    parser.add_argument('--bulbs', dest='list_bulbs', nargs="+", type=int, help='List of bulbs the application should manage')
    parser.add_argument('--bulbs-cycle', dest='list_bulbs_cycle', nargs="+", type=int,
                        help='List of bulbs the application should call for the cycle blink mode')
    parser.add_argument('--blacklight', dest='list_blacklight', nargs="+", type=int,
                        help='List of bulbs the application should call for the cycle blink mode')

    args = parser.parse_args()
    b = Bridge(args.ip)
    # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
    b.connect()
    # Get the bridge state (This returns the full dictionary that you can explore) with b.get_api()

    lamps = args.list_bulbs
    cycle_lamps = args.list_bulbs_cycle
    blackLight = args.list_blacklight
    lampsHue = []
    lampsBri = []
    lampsSat = []

    #save the current color configuration of the bulbs
    for bulb in lamps:
        lampsHue.append(b.get_light(bulb, 'hue'))
        lampsSat.append(b.get_light(bulb, 'sat'))
        lampsBri.append(b.get_light(bulb, 'bri'))

    while True:
        flash_light_effect(99, cycle_lamps)

        if just_blacklight(99):
            time.sleep(random.randint(30, 120))
            black_light_turn_off()

        if not everything_off_effect(99):
            do_glimmer()
            black_light()
            time.sleep(1)
        else:
            time.sleep(random.randint(5, 15))
            if just_blacklight(500):
                time.sleep(random.randint(10, 30))
                black_light_turn_off()
            else:
                flash_light_effect(500, cycle_lamps)
