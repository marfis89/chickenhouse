# chickenhouse - automate your chicken house with a rpi  

## Introduction  

[Deutsche Anleitung](./GERMANREADME.md)

## Features

## Table of Contents

1. [Parts](#parts)
2. [Hardware Setup](#hardware-setup)
3. [Electrical Setup](#electrical-setup)
4. [Software Setup](#software-setup)
5. [Usage Guide](#usage-guide)
6. [License](#license)

## Parts

To build your own chicken house control you will need the following parts. Feel free to use other brands with similar specifications:

### List of electrical parts

- Raspberry pi 3, 4, 5 (price ~50€)
- [Raspberry Pi 8-ch Relay Expansion Board from waveshare](https://www.waveshare.com/rpi-relay-board-b.htm) (price ~25€)
- [Linear motor 12V dc with endstops](https://www.ebay.de/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=12v+linear+motor+&_sacat=0&_odkw=12v+linear+morot&_osacat=0) (price ~100€)
- [13a fuse 1p+N, C-13A](https://www.hager.at/produktkatalog/energieverteilung-und-schutz-schaltgeraete/reiheneinbaugeraete/leitungsschutzschalter/ls-schalter-6ka/mcn513/19391.htm) (price 15€)
- [12v ~5a DIN rail power supply HDR-60-12](https://www.meanwell-web.com/en-gb/ac-dc-ultra-slim-din-rail-power-supply-input-range-hdr--60--12) (price ~20€)  
- [5v ~5a DIN rail power supply HDR-60-5](https://www.meanwell-web.com/en-gb/ac-dc-ultra-slim-din-rail-power-supply-input-range-hdr--60--5) (price ~20€)  
- 600mm x 400mm x 200mm control cabinet (price ~80€)
- stuff like cabels, DIN-Rail, wire ducts etc. (price ~50€)  

optional sensors:

- 1x [Temperature/Moisture Sensor](https://blog.adafruit.com/2013/03/14/new-product-soil-temperaturemoisture-sensor-sht10/) 

or

- 1x [Temperature Sensor](https://www.ebay.de/sch/i.html?_from=R40&_trksid=p2332490.m570.l1313&_nkw=ds18b20&_sacat=0)  

optional webcam:

- 1x [Full HD webcam](https://www.ebay.de/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=webcam&_sacat=0&_odkw=ds18b20&_osacat=0)

## Hardware-Setup

Just connect the linear dc motor to the flap door of your chicken home. For safety reasons you can use a rope between the motor and the door. If a chicken falls and gets stuck while closing, it will not be crushed by the force of the motor. Mount the lamps and infrared lamps.  

## Electrical-Setup

WARNING electrical installation are dangerous. If you don't know how to handel this task, ask a professional to do the job for you ! Liability for damages is excluded !

Make three inputs for phase, neutral and earth. Place the 13a input fuse (1p+N) onto the DIN rail and hook phase, neutral to it. Then make a connection from the fuse to the power supply. Power the pi or the board with 5v and GND from the power supply. Also wire the phase to relay 1 - 5 of the raspberry relay board. Use the NC connection of the relays, so the power is normally cut off. Wire the output of relay 1 to the 12v power supply. Wire the output of relay 2-5 to the separate terminal block, for switching light and heater. Connect the 12V output of the power supply to relay 7 and 8. Check [invertDc](./docs/invertdc.jpg) to see how to invert the rotation of the linear dc motor (USE RELAY 7 and 8).

### Wiring diagrams and schematics of the control cabinet

follow soon

## Software Setup

### Raspberry Pi Configuration

Try to use a good quality usb stick, instead of a simple sd card. There's a lot of tutorials to boot the pi 3 from a usb stick. The pi 4 and up, support usb boot out of the box. Flash the latest raspberry pi os to the stick and power up the pi.  

#### Steps to set up Raspberry Pi

1. Create a directory with ```mkdir /home/pi/chickenhouse```  
2. Copy [chickenhouse.py](./script/chickenhouse.py) to the pi /home/pi/chickenhouse/
3. Make chickenhouse.py executable ```chmod +x /home/pi/chickenhouse/chickenhouse.py```  
4. Create the file and copy the content of the [chickenhouse.service](./service/chickenhouse.service) with ```sudo nano /etc/systemd/system/chickenhouse.service```  
5. Enable the service with ```sudo systemctl enable chickenhouse.service```
6. Start the service with ```sudo systemctl start chickenhouse.service```
7. Check the service with ```sudo systemctl status chickenhouse.service```

The service execute the chickenhouse.py script on boot and take care if a reboot is necessary.

#### Installation of Node-RED and necessary packages

[official tutorial](https://nodered.org/docs/getting-started/raspberrypi)  

```console
sudo apt-get update && sudo apt-get upgrade && \
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered) && \
sudo systemctl enable nodered.service && \
sudo systemctl start nodered.service 
```

#### Hostname

When browsing from another machine you should use the hostname or IP-address of the Pi: ```http://<hostname>:1880```

Set a custom hostname to reach the pi without the ip address ```sudo hostname -b chickenhouse```  
Now reboot the pi and check the hostname with the ```hostname``` command. Now you can use [http://chickenhouse.local:1880](http://chickenhouse.local:1880) to reach noderred from your local network.

#### Installation of Node-RED packages  

Now install the following pallets for nodered dashboard and mqtt broker

-[node-red-contrib-aedes](https://flows.nodered.org/node/node-red-contrib-aedes)  
-[node-red-dashboard](https://flows.nodered.org/node/node-red-dashboard)  

Now import the [flow](./flow/flow.json) to nodered. See this instructions [Importing and Exporting Flows](https://nodered.org/docs/user-guide/editor/workspace/import-export)

#### Node-RED Flow

The flow provides a mqqt broker to communication with the chicken house service. The flow listening on ```chickenhouse/temperature``` and ```chickenhouse/humidity``` to receive the temperature and humidity from the sersors. The flow also listen to ```chickenhome/img``` to receive the webcam image, while the ui is active. To activate the "stream" the flow request a image from the script by posting on ```chickenhome/sendImg```.

## Usage Guide

Set the timer for the flap door and the lamps.  

## License  

This project is licensed under the GNU GENERAL PUBLIC LICENSE. Please refer to the [LICENSE](LICENSE) file for more details.

If you distribute copies of such a program, whether gratis or for a fee, you must pass on to the recipients the same freedoms that you received. You must make sure that they, too, receive or can get the source code. And you must show them these terms so they know their rights as Outlined in the GPLv3 License.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  
