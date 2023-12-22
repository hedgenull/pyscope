PyScope
=======

A Stellarium compatible telescope control server written in Python. I've updated it to be Python 3-compatible and improved the code a little. It's possible I will further modify this for personal use.

Details
=======

A simple server that is compatible with Stellarium (http://www.stellarium.org).
telescope control protocol. This is made as a foundation for a computer controller star finder- it doesn't control anything, but it allows you to issue commands via Stellarium and translates GoTo commands into RA and Dec coordinates. Feel free to use this- all you need to do to get it working is (1) start the program on whatever you want to run it on (for example a Raspberry Pi), (2) set up a "remote, unknown" telescope in Stellarium and give it the IP address of the host computer, and connect Stellarium to the server. You should be good to go then!

Again, this doesn't include code to actually point anything anywhere- it just makes it easy to work with Stellarium commands. You'd have to create your own motor controller.

For more information on Stellarium telescope control visit:

[(https://free-astro.org/images/b/b7/Stellarium_telescope_protocol.txt)https://free-astro.org/images/b/b7/Stellarium_telescope_protocol.txt](https://free-astro.org/images/b/b7/Stellarium_telescope_protocol.txt)https://free-astro.org/images/b/b7/Stellarium_telescope_protocol.txt
