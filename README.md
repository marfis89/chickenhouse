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

To build your own Vibrodoser you will need the following parts. Feel free to use other brands with similar specifications:

### List of electrical parts

- Raspberry pi 3, 4, 5 (price ~50€)
- [Raspberry Pi 8-ch Relay Expansion Board from waveshare](https://www.waveshare.com/rpi-relay-board-b.htm) (price ~25€)
- [1kg load cell with a hx711 A/D hx711](https://www.ebay.de/sch/i.html?_from=R40&_trksid=p2553889.m570.l1313&_nkw=hx+711+loadcell&_sacat=0) (price ~5€)
- [10A Power regulator from kemo](https://www.kemo-electronic.de/en/Transformer-Dimmer/M240-Power-Control-230-V-AC-10-A-Multifunction.php) (price ~50€)
- [Linear feeder from Afag](https://www.afag.com/en/products/detail/linear-feeder-hlf-m-3.html) (get a used one from ebay ~350€)
- [5v ~5a DIN rail power supply HDR-60-5](https://www.meanwell-web.com/en-gb/ac-dc-ultra-slim-din-rail-power-supply-input-range-hdr--60--5) (price ~20€)  
- [13a fuse 1p+N, C-13A](https://www.hager.at/produktkatalog/energieverteilung-und-schutz-schaltgeraete/reiheneinbaugeraete/leitungsschutzschalter/ls-schalter-6ka/mcn513/19391.htm) (price 15€)
- 600mm x 400mm x 200mm control cabinet (price ~80€)
- stuff like cabels, DIN-Rail, wire ducts etc. (price ~50€)

### List of 3D models and mechanical parts

- 10m 40mmx40mm steel pipes (price ~200€)
- 5mm steel plate (price ~200€)
  - 2x 600mmx 800mm
  - 1x 280mm x 600mm  

optional for wlan / lan connection of the raspberry (You don't have to create a separate network, you can use your normal network too):

- a cheap wlan router (mostly they have 12v input voltage, choose a power supply that fits the router)  
- [12v ~5a DIN rail power supply HDR-60-12](https://www.meanwell-web.com/en-gb/ac-dc-ultra-slim-din-rail-power-supply-input-range-hdr--60--12) (price ~20€)  

## Hardware-Setup


## Electrical-Setup

WARNING electrical installation are dangerous. If you don't know how to handel this task, ask a professional to do the job for you ! Liability for damages is excluded !

Make three inputs for phase, neutral and earth. Place the 13a input fuse (1p+N) onto the DIN rail and hook phase, neutral to it. Then make a connection from the fuse to the power supplies. 

### Wiring diagrams and schematics of the control cabinet

follow soon

## Software Setup

### Raspberry Pi Configuration

Try to use a good quality usb stick, instead of a simple sd card. There's a lot of tutorials to boot the pi 3 from a usb stick. The pi 4 and up, support usb boot out of the box. Flash the latest raspberry pi os to the stick and power up the pi.  

#### Steps to set up Raspberry Pi

1. Create a directory with ```mkdir /home/pi/vibrodoser```  
2. Copy [hx7111](hx711/hx711.py) and [vibrodoser.py](./hx711/vibroDoser.py) to the pi /home/pi/vibrodoser/
3. Make vibrodoser.py executable ```chmod +x /home/pi/vibroDoser/vibroDoser.py```  
4. Add the content of the [vibrodoser.service](./service/vibrodoser.service) file to /etc/systemd/system/vibrodoser.service
5. Enable the service with ```sudo systemctl enable vibroDoser.service```
6. Start the service with ```sudo systemctl start vibroDoser.service```
7. Check the service with ```sudo systemctl status vibroDoser.service```

The service execute the vibroDoser.py script on boot and take care of a reboot is necessary.

#### Installation of Node-RED and necessary packages

[official tutorial](https://nodered.org/docs/getting-started/raspberrypi)  

```console
sudo apt-get update && sudo apt-get upgrade && \
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered) && \
sudo systemctl enable nodered.service && \
sudo reboot
```

When browsing from another machine you should use the hostname or IP-address of the Pi: http://<hostname>:1880. You can find the IP address by running hostname -I on the Pi.  

Now install the following pallets for nodered dashboard and mqtt broker

-[node-red-contrib-aedes](https://flows.nodered.org/node/node-red-contrib-aedes)  
-[node-red-dashboard](https://flows.nodered.org/node/node-red-dashboard)  

Now import the [flow](./flow/flow.json) to nodered. See this instructions [Importing and Exporting Flows](https://nodered.org/docs/user-guide/editor/workspace/import-export)

#### Node-RED Flow

The flow provides a mqqt broker to communication with the scale service. The flow listening on ```vibroDoser/scale/load``` and sending the tare command on ```vibroDoser/scale/tare``` to the scale. While there is active, all measurements from the scale are blocked.

## Usage Guide


## License  

This project is licensed under the GNU GENERAL PUBLIC LICENSE. Please refer to the [LICENSE](LICENSE) file for more details.

If you distribute copies of such a program, whether gratis or for a fee, you must pass on to the recipients the same freedoms that you received. You must make sure that they, too, receive or can get the source code. And you must show them these terms so they know their rights as Outlined in the GPLv3 License.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  
