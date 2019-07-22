## Description

This program will watch a directory for a certain file extension and a certain magic text string

## Setup

enter the directory to be watched and the text to search for in the files.
ex:

python watcher.py /dirctory MagicText

optional arguments:

-i, --interval: amount of time between default=1.0

-e, --ext: custom extention to use default=txt

## Sample output

user@computer:~/dir_watcher\$ python watcher.py ~/dirwatch/ magic -i 2.0 --ext txt
2019-07-22 09:45:30,536 - **main** - INFO -

    --------------------------------

    Starting up, time = 2019-07-22 09:45:30.531901

    --------------------------------

2019-07-22 09:45:30,536 - **main** - INFO - Searching=/dirwatch/ for text=magic in files with ext=txt every sec=2.0
2019-07-22 09:45:30,537 - **main** - INFO - File=file.txt found, adding to watched list
2019-07-22 09:45:30,537 - **main** - INFO - Text =magic found in file=/dirwatch/file.txt at line=5
2019-07-22 09:46:01,573 - **main** - WARNING - Received SIGINT
2019-07-22 09:46:01,573 - **main** - INFO -

    --------------------------------

    Shutting down. Uptime = 0:00:31.041785

    --------------------------------
