# Python Alarm Clock
A **Python 3** & **PHP** powered alarm clock running on a Raspberry Pi 3 that wakes you up with a random selection of nature sounds.
Wake up gently as the alarm slowly adds different layers of sounds. One time the alarm goes off with a small creek flowing , some birds chirping and a little bit of rain. Another time you're at the beach with the sound of the waves, seagulls and maybe a campfire.

## Features
- Random selection of sounds everytime the alarm goes off
- Web interface to set and cancel alarm, and see when the alarm is set
- GPIO button to cancel alarm when it goes off
- Disables speaker overnight and enables it only when starting the alarm. This to prevent static noise from the speaker when trying to sleep
- Choose & organize your own sounds
- Blacklist folders so they don't play as the first sound
- Choose fade-in length of sounds
- Choose how quickly the next sound should be played
- Maximum time for alarm to play

## Components used
The GPIO aspect of this alarm can be left out completely. It's perfectly possible to just plug in any speaker with a 3,5mm audio jack into the Pi and just leave it at that. However, i couldn't stand the noise the speakers made when left on overnight. That's why i extended the alarm with some extra hardware.

The main components used in this project are a [small speaker](https://www.adafruit.com/product/1314) (3W, 4Ohm) and a [small mono amplifier](https://www.adafruit.com/product/2130) (2,5W).
The amplifier i used comes with a handy shutdown pin so i didn't need a relay to switch the speaker on and off. This is great because the click of a relay is pretty loud and it doesn't require extra wires.

To connect the amplifier to the Raspberry Pi, I cut a regular audio jack (AUX) cord and used the ground and right channel wires. The rest of the cable was used to connect the speaker to the amplifier, also using the ground and right channel wires.

I also implemented a button to cancel the alarm when it is playing. This is an easier way than cancelling it via the web interface on your phone. I used this [button](https://www.kiwi-electronics.nl/arcade-drukknop-33mm-blauw) but any regular button should do.

## Installation
I didn't keep track of everything i did to get this alarm running correctly, but i'll put everything i remember down here.
If i forgot something or if you have a problem with something, let me know!

- Install Apache webserver & PHP
- Clone this repo into the webserver folder. Most of the time this folder is located at `/var/www/html`
- Give the Apache/PHP user the permission to play sounds. In my case this is user `www-data`. This can be done by adding the user to the `audio` group: ```sudo usermod -a -G audio www-data```
- Make sure Apache/PHP has the rights to make and delete files in the `/var/www/html` folder
- Make the pigpio daemon run on startup. I did this by adding the startup command `pigpiod` to the `/etc/rc.local` file. Put the command at the end of the file, but before `exit 0`. This will run the command every time on startup.

- Connect the A+ pin of the PAM8302 amplifier to the left or right channel wire of the stereo audio jack. If your cable is mono, just use the one audio cable.
- Connect the A- pin to the ground wire of the aux.
- The Vin pin is connected to a 5V GPIO pin on the Raspberry, and the Gnd pin is connected to a ground pin on the Raspberry.
- The SD (shutdown) should be connected to GPIO pin 2 (Broadcom numbering). This can be changed in the code so you can connect it to a different pin.
- Connect the button to GPIO pin 18 (Broadcom numbering) and to a ground pin on the Raspberry
