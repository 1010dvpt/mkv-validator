# mkv-validator

**mkv-validator.py** a MKV validator wrapper written in [Python](https://www.python.org/downloads/) for [mkvalidator.exe](https://www.matroska.org/downloads/mkvalidator.html)

recursively validate the integrity of your mkv file library and store the results in a log file.

## Dependencies
- mkvalidator.exe from matroska.org [download](https://www.matroska.org/downloads/mkvalidator.html)
- python 3.5.2 from python.org [download](https://www.python.org/downloads/)

## Setup
- Install [Python](https://www.python.org/downloads/) 3.5.3
- Download or clone mkv-validator.py from this repo
```
git clone git@github.com:1010dvpt/mkv-validator.git
```
- Place matroska's mkvalidator.exe file in the mkv-validator directory
```
C:\Users\Media\Downloads\mkv-validator\>ls
LICENSE.md README.md mkv-validator.py mkvalidator.exe
```
## Usage
Works in these Windows 10 command line environments
- Git Bash [download](https://git-for-windows.github.io/)
- cmd
- powershell

### help
```
C:\Users\Media\Downloads\mkv-validator\>python mkv-validator.py -h
usage: mkv-validator.py [-h] [-o OPTIONS] -s SOURCE

example: python mkv-validator.py -o details -s E:\\mkvs\\movies

optional arguments:
-h, --help            show this help message and exit
-o OPTIONS, --options OPTIONS
                      no-warn   only output errors, no warnings
                      live      only output errors/warnings relevant to live streams
                      details   show details for valid files
                      divx      assume the file is using DivX specific extensions
                      quiet     don't output progress and file info
-s SOURCE, --source SOURCE
                      E:\\mkvs\\movies
                      E:/mkvs/movies
                      E:/mkvs/"Best Movies"
```
### Output
```
C:\Users\Media\Downloads\mkv-validator\>python mkv-validator.py -o details -s E:\\mkvs

Checking: E:\\mkvs\A\a-great-movie.mkv
mkvalidator 0.5.0: the file appears to be valid

Checking: E:\\mkvs\B\b-bad-movie.mkv
ERR042: The segment's size 8211979374 doesn't match the position where it ends 398673472
ERR066: The SeekPoint at 87 references an unknown Cues at 8211952374
WRN800: The segment has Clusters but no Cues section (bad for seeking)
WRN0D0: There are 5244 bytes of void data

Checking: e:\\mkvs\T\tv-great-show.mkv
mkvalidator 0.5.0: the file appears to be valid
```
### Logging
a log file is written as mkv_results.log.  Here you will find the complete output of what was found for each mkv file.
```
[2016/09/23 11:04:08] - Title E:\\mkvs\A\a-great-movie.mkv [...
...
[2016/09/23 11:06:17] - Title E:\\mkvs\B\b-bad-movie.mkv [....
...
```
### Pro Tip (requires Git bash)
Capture the screen output as a log file too
```
C:\Users\Media\Downloads\mkv-validator\>python mkv-validator.py -o details -s E:\\mkvs | tee -a mkv_screen.log
```
```
C:\Users\Media\Downloads\mkv-validator\>ls
LICENSE.md README.md mkv-validator.py mkv_results.log mkv_screen.log mkvalidator.exe
```
### License
[Apache License](http://apache.org/licenses/LICENSE-2.0.html)
