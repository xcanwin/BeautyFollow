# BeautyFollow
## 简介
```
这是一款用于追剧、追漫、追小说的小工具，原理是通过事先配置好的正则表达式来匹配最新章节，并且输出界面较为友好的html展示页面。目前支持解析360浏览器的书签。
```

## 用法
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
