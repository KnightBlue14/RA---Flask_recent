# RetroAchievements - Recent unlock webserver
This is a browser utility tool for RetroAchievements, showing recent unlocks in a number of classic games on popular console emulators

## Description
This project utilises one of multiple APIs from RetroAchievements, a community-based project for integrating achievements (such as those on Steam and Xbox, or Playstation trophies) into popular emulators, such as PCSX2, Dolphin and Duckstation. In order to use it, you will need to create a free account, as well as activate the integration in your emulator of choice. That done, the webserver will output to a port on your host machine's network, which can be accessed via any browser. It will update in near real-time, displaying the game you most recently played, and the achievement you most recently unlocked. In the example shown below, I had just finished the planet Umbris in Ratchet and Clank. 

The integration does have a pop-up appear on-screen, but this was intended to serve as a more prominent version that can stay in place beyond the limits of the integration.

## Technologies used
* Python - The server is based in Flask, and also uses additional files to validate your account, as well as update the image files stored.
* HTML - This project makes some use of HTML to build the webpage, and updates every 10 seconds. This is enough for my purposes, but you can edit this, which will be outlined in the next section

## How to use
The files are mostly complete, but there are some changes that can be made to suit your needs.

### .env
This is the file needed to validate your access to the RetroAchievements server. You will need a username, and a web API key, which can be found in the settings for your free account.

https://retroachievements.org/createaccount.php

https://retroachievements.org/settings

### cache.json
This file is used as a long-term storage solution. By default, the API will only look back 1 hour for your most recent progress. Beyond that, a null result is returned. This file will store the most recent unlock while the server is running, allowing it to be displayed beyond that limit.

### server.py
The file used to orchestrate your server, as well as collect the game title and achievement data. This file is functionally complete, and will automatically load or update the cache file when triggered, as well as loading variables to be used by the html file.

### templates/index.html
The template for the server webpage. This can be edited as you see fit to meet your preferences - the background colour, the size of text, the placement of text and images, can all be edited. Also, there is a variable on line 4 -
```
meta http-equiv="refresh" content="10; URL=http://localhost:5000"
```
The number before the URL controls how frequently the webpage reloads, In this case, it updates very 10 seconds. You can make this period shorter or longer, though be aware that RA does limit how frequently the API can be accessed

### static/images/badge or cover.png
These are used to display relevant images, and are collected by other files. These do not need to be altered in any way

## Docker

After some tinkering, I've managed to get this app running in a Docker container, which makes it much easier to spin up and down at a moment's notice. If this is of interest to you, read on. It's similar to other projects on my profile, with some extra caveats to account for the webpage component.

### Dockerfile

This is all you need in addition to the other files to spin up a container. It uses the 3.11-slim variant of the python image, making it much more lightweight than the default version. Of note is the networking component - by default, flask will run on port 5000 of the local machine's IP address. If you are not using docker, simply use a browser and open the address listed in the terminal when you start the server. 
By contrast, if you use docker, you will need to specify in the app the address to use, as well as map the port of the container to one used by your machine.

To build the container, simply use the command
```
docker build -t raflask .
```
Then, either run it via the command line with
```
docker run --name raflask -p 5000:5000 -d raflask
```
or run it via Docker Desktop using the same variables. The number on the left is the port your machine will use, and can be set to whatever you wish. The one on the right is used by the container, and should be left alone unless you change it in the Flask app config, which there isn't really a reason to do here. That done, simply use the same address as the container -
```
127.0.0.1:5000
```
to see the webpage