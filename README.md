# Google Meet Class Bot

## Overview

A bot created for the sole purpose of following a schedule and joining google meetings with pre-provided links, allowing for the user to be away and have the bot manage attendance.

## Setup

Download the gmeetclass folder, the gmeet.py file or the gmeet.exe file, and make sure that the folder and the file is in the same directory.

Upon launching first time, begins the setup process which prompts for the number of periods in a day, the times at which these periods will end, the names of the subjects you do, the google meet lookup links for each one, and finally, your timetable.

## Usage
Download either the gmeet.exe file or the gmeet.py file with the chromedriver.exe file and the gmeetclass folder. Using the app differs based on method.

### gmeet.exe

Simply double tap the file.

### gmeet.py

Open your cmd and navigate to the folder where the gmeet.py file is, and simply run the command "python gmeet.py" (windows) or your os equivalent.

## Extra Notes:

When setting up your time table, note that everysubject must have a google meet link. Therefore, take into account stuff like registration, lunch and non-contact periods if viable. For the non-contact / lunch periods, I don't have any special functionality, so just put in any of your other subjects as a place holder.

## Requirements
You need to have either the gmeet.py file or the gmeet.exe file, in addition to the chromedriver.exe file and the gmeetclass folder.
Check requirements.txt (For developers)