<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h1 align="center">Cool Hangman</h1>

  <p align="center">
    A Streamlabs Chatbot script to let your users win points guessing letters and words, while everything is reflected in your OBS with a customizable overlay.
    <br />
    <a href="https://github.com/LuisSanchez-Dev/cool-hangman/archive/master.zip">Download</a>
    ·
    <a href="https://github.com/LuisSanchez-Dev/cool-hangman/issues">Report Bug</a>
    ·
    <a href="https://github.com/LuisSanchez-Dev/cool-hangman/issues">Request Feature</a>
  </p>
</p>

If you need a custom script that fit your needs, don't hesitate to contact me on Fiverr: https://fiverr.com/luissanchezdev

Or if you need Twitch emotes, sub badges, chanel point images or logos, contact Tecno_Diana: https://fiverr.com/tecno_diana

## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Overlay installation](#overlay-installation)
* [Usage](#usage)
* [Contact](#contact)
* [License](#license)

## About The Project

A client told me that the hangman script already in the #scripts channel on the Streamlabs Chatbot Discord server was not good enough, so I made this.

Every 10 minutes or when you issue a command, all the users can try to guess a letter or the entire word, if they find letters or guess the entire word they get points for each letter they guessed!

You have easy access to a text file so you can add your own words.

It also has a simple overlay for your OBS, a text file that gets updated everytime a game starts or someone guesses the word and a simple 8 images animation that represent the tries left, just as the real hangman!

## Getting Started

Setting this up so you can use it is super straightforward.

### Prerequisites

Have an installation of Streamlabs Chatbot, already logged in to your accounts.
* [Download Streamlabs Chatbot](https://streamlabs.com/chatbot)

Follow this tutorial to prepare your Streamlabs Chatbot installation to accept scripts.
* [[Streamlabs Chatbot] Scripts Explained by Castorr91](https://www.youtube.com/watch?v=l3FBpY-0880&t=3s)
### Installation

1. Download the latest version of the script [**here**](https://github.com/LuisSanchez-Dev/cool-hangman/archive/master.zip).
2. If you haven't already, open your Streamlabs Chatbot and log in to your Streamer and Bot accounts.
3. On the left side, wait for the `Scripts` tab to pop up and click it.
4. On the top right corner of the window, next to the reload button is an import script button (Arrow pointing right to a box) and select the script downloaded before.
5. You will receive a message box confirming the import, accept it.
6. The window will update and show the `Cool Hangman` script, make sure to ✔️ enable the script on the right hand side.
7. Click on the `Cool Hangman` name to see the configuration pane.

### Overlay installation
After doing the step 7 of last steps, click on the OPEN UI FOLDER button and copy the folder path, then open OBS
* For the text:
  1. Add a new Text GDI+ source in your scene
  2. ✅ Check the local file checkbox
  3. Click `Browse`, on the address at the top, paste the path copied before
  4. Select the hangman.txt file, this will update automatically
* For the images:
  1. Add a new Image source
  2. Click on browse and paste the path on the address bar
  3. Select the main.png file

Now, to install your own images:
  * Click the OPEN UI FOLDER button 
  * Here you will find 10 PNG files and 1 TXT file, ignore the TXT file.
    * `0.png` must be an empty image 100% tranwsparent
    * `1-8.png` are the animation frames, change them as you please. Must be 8 frames!
    * `main.png` must be a copy of the 0.png file the first time you install the script, this image will be replaced by the script to achieve a simple animation
  
<!-- USAGE EXAMPLES -->
## Usage

Every 10 minutes or by doing `!starthang` command, a game will start showing instructions on how to play.
* `!guess <letter>` To try to guess a letter
* `!guessword` To try to guess the entire word

## Contact

* Discord - luissanchezdev#6247
* Fiverr - [luissanchezdev](https://fiverr.com/luissanchezdev)
* luis.sanchez.dev@hotmail.com

Remember to join the [Streamlabs Chatbot Discord server](https://discordapp.com/invite/S2d4KGg) for sfx, scripts, commands and a lot more!

## License
Licensed under GPL v3
Copyright (C) 2020 Luis Sanchez