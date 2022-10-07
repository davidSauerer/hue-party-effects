# hue-party-effects
This project is controlling your hue bridge and enables some party effects

## How to get started
Start the application with the ip address as Command-Line Argument. Then you need to press the button of the Hue bridge.
 + --ip (IP of Hue Bridge)
 + --bulbs (list of bulbs for the most effects)
   + provides included bulbs for the most effects
 + --bulbs-cycle (List of bulbs for Light cycle effect)
   + provides included bulbs
   + provides order for Light cycle effect
 + --blacklight (Sockets for blacklight)
   

Example: --ip 192.168.1.100 --bulbs 15 1 24 26 42 53 2 52 --bulbs-cycle 1 26 17 24 53 2 52 --blacklight 50 48 
## Limitations
 + The used bulbs are hardcoded
 + You could not turn specific effects on or off
 + hue bridge needed

## Supported effects
### Flickering of bulbs
The bulbs are changing a little bit the color and brightness 

### Everything out
All lights are turning off at the same time

### Lights cycle
All lights are going off and then on after the another is blinking in a cycle

### Turn hue sockets on and off
Its allowing you to turn two sockets on and off in addition to the other effects. I use this for dark light.
