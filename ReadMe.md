Repository for Swanton Pacific Ranch EE Senior Project. TinySA program to record frequency and power of peak in the spectrum (PlotScan.py). Other scripts are supplementary examples to show other functionalities of TinySA. Recommend creating a virtual environment and pip installing requirements.txt to get started.

Need: USB GPS antenna using u-blox 7 encoding. TinySA (Ultra was used, should work with any). Python 3.14.

You'll likely need to read the documentation below to learn the setup on your machine. The gist of it is that you need to have both the TinySA and GPS antenna connected, and find the ports they are connected to on your machine. Once that's done, you can start the gpsd daemon and gpsd client (client is optional, but it's nice to have a visuallization of the GPS data coming in), then can start PlotScan.py.

Documentation of some of the projects used for this:
[Connecting USB GPS to Raspberry Pi](https://www.crewdogelectronics.com/vk-162-usb-gps-aprs-raspberry-pi-direwolf/)
[GPSD Installation Instructions](https://gpsd.io/installation.html)
[GPSD Cleint Python Package](https://pypi.org/project/gpsdclient/)
[TinySA Python API](https://github.com/LC-Linkous/tinySA_python/tree/main)
[TinySA Wiki Page for PC Connections](https://tinysa.org/wiki/pmwiki.php?n=Main.PCSW) (Not used in this project per se, but still useful to get a hang of the device)