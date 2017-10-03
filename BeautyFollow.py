#!/usr/bin/env python
# -- coding: utf-8 --

import os, sys, time, shutil, argparse
import re, json, chardet
import requests



def fileToJson(filename):
    f = file(filename)
    jStr = ''.join(f.readlines())
    jStr = jStr.decode(chardet.detect(jStr)['encoding'])
    # print jStr
    jObject = json.loads(jStr)
    return jObject

def getLatestChapter(url):
    regexps = fileToJson(reFile)
    for key in regexps.keys():
        if url.find(key)>-1:
            try:
                r = requests.get(url, timeout=timeout)
                rc = r.content
                regexp = regexps[key].encode('utf-8')
                matchObj2 = re.search(regexp, rc)
                latestChapter = matchObj2.group(1)
                return latestChapter.decode('utf-8')
            except Exception, e:
                error = str(e)
                if error.find('timed out')>-1:
                    error = 'time out'
                elif error.find('NoneType')>-1:
                    error = 'regexp can\'t match'
                print '[-] get %s latestChapter error: %s' % (url, error)
            return False

def test():
    print getLatestChapter('http://ac.qq.com/Comic/ComicInfo/id/526501')
    print getLatestChapter('http://www.dmzj.com/info/guiwang.html')
    print getLatestChapter('http://www.kuman.com/mh-1000254/')
    print getLatestChapter('http://www.manhuatai.com/zetianji/')
    print getLatestChapter('http://www.u17.com/comic/119612.html')
    print getLatestChapter('http://www.1kkk.com/manhua20874/')
    print getLatestChapter('http://www.57mh.com/118/')
    print getLatestChapter('http://www.ikanman.com/comic/18892/')
    print getLatestChapter('http://www.dm5.com/manhua-yaren/')


def chapterControl(action, updateId = 0):
    jObject = fileToJson(listFile)
    array = []
    for element in jObject:
        # time.sleep(0.2)
        id = element['id']
        url = element['url']
        name = element['name']
        oldChapter = element['oldChapter']
        latestChapter = element['latestChapter']
        if action == 'readAll':
            # read list
            print 'id: %s, \tname: %s,\n\t\turl: %s,\n\t\toldChapter: %s,\n\t\tlatestChapter: %s\n' % (id, name, url, oldChapter, latestChapter)
            if element == jObject[-1]:
                exit()
        elif action == 'updateAll':
            # update all: latestChapter
            latestChapterNew = getLatestChapter(url)
            if not (latestChapterNew == latestChapter):
                element['latestChapter'] = latestChapterNew
                print '[+] great: %s has been updated to %s' % (name, latestChapterNew)
            print 'id: %s, \tname: %s,\n\t\turl: %s,\n\t\toldChapter: %s,\n\t\tlatestChapter: %s\n' % (id, name, url, oldChapter, latestChapterNew)
        elif action == 'updateAny':
            # update anyone: oldChapter and latestChapter
            if updateId == id:
                latestChapterNew = getLatestChapter(url)
                if latestChapterNew:
                    element['oldChapter'] = latestChapterNew
                    element['latestChapter'] = latestChapterNew
                    print '[+] great: %s has been updated to %s' % (name, latestChapterNew)
        array.append(element)
    aJStr = json.dumps(array, ensure_ascii = False, indent = 4).encode('utf-8')
    # print aJStr
    copyListFile()
    write = open(listFile, 'w')
    write.write(aJStr)
    write.close()
    print '[+] success: save new list file in', listFile

def copyListFile():
    backupdir = 'backup'
    if not os.path.exists(backupdir):
        os.makedirs(backupdir)
    timestamp = str(int(time.time()))
    newFile = '%s/%s_%s' % (backupdir, timestamp, listFile)
    shutil.copy(listFile, newFile)

if __name__ == '__main__':
    listFile = 'list.txt'
    reFile = 're.txt'

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action='store_true',
                        dest='readall',
                        help='read list;')
    parser.add_argument('-U', action='store_true',
                        dest='updateall',
                        help='update all;')
    parser.add_argument('-u', action='store',
                        type=int,
                        dest='update',
                        help='update anyone by id;')
    parser.add_argument('-t', action='store',
                        type=int,
                        dest='timeout',
                        default=20,
                        help='request timeout (default: 20);')
    args = parser.parse_args()
    readall = args.readall
    updateall = args.updateall
    update = args.update
    timeout = args.timeout
    # test()
    if len(sys.argv) < 2:
        print 'usage: python', sys.argv[0], '-h'
        # chapterControl('readAll')
        # chapterControl('updateAll')
        # chapterControl('updateAny', 1)
        exit(0)

    if readall:
        chapterControl('readAll')
    elif updateall:
        chapterControl('updateAll')
    elif update:
        chapterControl('updateAny', update)


