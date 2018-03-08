# BeautyFollow
## Purpose
```
This is a tool for getting updates like comics, books and TV series.
```

## usage:
```
usage: BeautyFollow.py [-h] [-R] [-U] [-u UPDATE] [-t TIMEOUT]
                       [-b GETBOOKMARK] [-f LISTFILE] [-s]

optional arguments:
  -h, --help      show this help message and exit
  -R              read list?
  -U              update all?
  -u UPDATE       update anyone by id;
  -t TIMEOUT      request timeout (default: 20);
  -b GETBOOKMARK  get bookmark by Mainstream browsers;
  -f LISTFILE     list file;
  -s              show result by html?

example: python BeautyFollow.py -h
         python BeautyFollow.py -R
         python BeautyFollow.py -U
         python BeautyFollow.py -u 2
         python BeautyFollow.py -f list_360se.txt -U
         python BeautyFollow.py -b 360se -U -s
```
