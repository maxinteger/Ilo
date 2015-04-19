# Ilo

This was my thesis project!

Ilo is a 3D graphic engine Programed in Python 2.6 programing language with OpenGL 3.0 graphics librily and QT4.5 framework.

How to run (Ubuntu Linux):

* Install basics
	* `sudo apt-get install aptitude`
	* `sudo aptitude install gcc freeglut3 libgle3 python-dev python-setuptools python-pygame python-numpy python-imaging`
	* `sudo aptitude install python-qt4`
* Create virtualenv: `vistualenv .venv --system-site-packages`
* Activate virtualenv: `. .venv/bin/activate`
* Install pip packages: `pip install -r requrements.txt`
* Install PIL: [install 1](http://stackoverflow.com/questions/13992214/how-to-import-a-globally-installed-package-to-virtualenv-folder) [install2](http://stackoverflow.com/questions/20060096/installing-pil-with-pip)
	* `sudo apt-get install python-dev libjpeg-dev libjpeg8-dev libpng3 libfreetype6-dev`
	* `sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib`
	* `sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib`
	* `sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib`
	* `sudo ln -s /usr/include/freetype2 /freetype`
	* `pip install PIL  --allow-unverified PIL --allow-all-external`

* Run... `python Ilo/src/game.py`

[Original repository](http://code.google.com/p/ilo/)
