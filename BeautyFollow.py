#!/usr/bin/env python
# -- coding: utf-8 --

import os, sys, time, shutil, argparse, _winreg
import re, json, chardet, collections
import requests


def showByHtml(resultDict, source = ''):
    global showHtmlTmp
    htmlResult = u''
    for name, value in resultDict.items():
        htmlResult += u'<tr><td>%s</td><td><a target="_blank" href="%s">%s</a></td><td>%s</td><td>%s</td></tr>\n' % (value['id'], value['url'], name, value['oldChapter'], value['latestChapter'])
    showDemo = '''<html><head><title>BeautyFollow show</title><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><style>body{width:600px;margin:40px auto;font-family:'trebuchet MS','Lucida sans',Arial;font-size:14px;color:#444;}table{*border-collapse:collapse;border-spacing:0;width:100%;border:solid #ccc 1px;-moz-border-radius:6px;-webkit-border-radius:6px;border-radius:6px;-webkit-box-shadow:0 1px 1px #ccc;-moz-box-shadow:0 1px 1px #ccc;box-shadow:0 1px 1px #ccc;}tr:hover{background:#fbf8e9;}td,th{border-left:1px solid #ccc;border-top:1px solid #ccc;padding:10px;text-align:left;}th{background-color:#dce9f9;}</style></head><body><h2>BeautyFollow show</h2><table><thead><tr><th>id</th><th>name</th><th>oldChapter</th><th>latestChapter</th></tr></thead>[result]</table></body></html>'''
    showDemo = showDemo.replace('[result]', htmlResult.encode('utf-8'))
    file('show_%s.html' % source, 'wb').write(showDemo)
    print '[+] save as: show_%s.html' % source

    if showHtml:
        if not (getBookmark and (readall or updateall or update)):
            os.system('start show_%s.html' % source)
        else:
            if showHtmlTmp:
                os.system('start show_%s.html' % source)
    showHtmlTmp = True

def compatible360se():
    #'X:\\Program Files\\360se\\360se6\\User Data\\Default\\XXXX\\Bookmarks'
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, r"360seURL\\DefaultIcon")
    except Exception,e:
        print str(e)
        if '[Error 2]' in str(e):
            print '[-] error: There are no 360 browsers.'
        else:
            print '[-] error: There are other errors.'
        exit()
    regValue, regType = _winreg.QueryValueEx(key,"")
    userData360se = regValue[0:regValue.rfind('Application')] + 'User Data\\'
    # print userData360se
    localState = userData360se + 'Local State'
    userid = json.loads(file(localState, 'rb').read())['sync_login_info']['filepath']
    bookmarksFile = userData360se + 'Default\\' + userid + '\\Bookmarks'
    # print bookmarksFile
    bookmarks = json.loads(file(bookmarksFile, 'rb').read(), object_pairs_hook=collections.OrderedDict)
    bookmarks = bookmarks['roots']['bookmark_bar']['children']
    resultDict = collections.OrderedDict()
    for bookmark in bookmarks:
        if bookmark['name'] == u'Comics':
            for value in bookmark['children']:
                name = value['name']
                url = value['url']
                resultDict[name] = {
                    'id': value['id'],
                    'url': url,
                    'oldChapter': '',
                    'latestChapter': ''
                }
            break
    rdStr = json.dumps(resultDict, ensure_ascii = False, indent = 4).encode('utf-8')
    file(listFile, 'wb').write(rdStr)
    print '[+] save as:', listFile
    showByHtml(resultDict, listFile)

def fileToJson(filename):
    jStr = file(filename, 'rb').read()
    jStr = jStr.decode(chardet.detect(jStr)['encoding'])
    # print jStr
    jObject = json.loads(jStr, object_pairs_hook=collections.OrderedDict)
    return jObject

def getCharset(rc):
    charset_re = re.compile(r"<meta.*?charset\s*=\s*([\"']*)([^\"'>]*).*?>", re.I|re.M)
    charset=charset_re.search(rc[:1000])
    if charset:
        charset = charset.group(2)
    else:
        charset = 'utf-8'
    return charset

def clearChapter(chapter):
    chapter3 = re.sub(r'\d{4}-\d{2}-\d{2}', '', chapter)
    chapter2 = chapter3.replace(u'（', u'(').replace(u'）', u')').replace(u'：', u':').replace(u'。', u'.').replace(u'第', u'<').replace(u'、', u'>').replace(u'回', u'>').replace(u'话', u'>').replace(u'集', u'>').replace(u'【', u'').replace(u'】', u'')
    r = re.search(r'<?(.+?)[-|:|,|.|\s|>]', chapter2)
    if r:
        chapter2 = r.group(1)
    for l2 in chapter2:
        if not l2 in u'0123456789〇一二三四五六七八九零壹贰叁肆伍陆柒捌玖两①②③④⑤⑥⑦⑧⑨㈠㈡㈢㈣㈤㈥㈦㈧㈨⑴⑵⑶⑷⑸⑹⑺⑻⑼⒈⒉⒊⒋⒌⒍⒎⒏⒐十拾百佰千仟万':
            chapter2 = chapter3
            break
    return chapter2

def getLatestChapter(url, testRegexp = ''):
    regexps = fileToJson(reFile)
    enumReFlag = True
    for key in regexps.keys():
        if testRegexp:
            key = url
            regexps[key] = testRegexp
            if enumReFlag:
                enumReFlag = False
            else:
                break
        if url.find(key)>-1:
            try:
                r = requests.get(url, timeout=timeout)
                rc = r.content
                #print rc
                regexp = regexps[key].encode('utf-8')
                matchObj2 = re.search(regexp, rc)
                latestChapter = matchObj2.group('chapter').strip().decode(getCharset(rc))
                latestChapter2 = clearChapter(latestChapter)
                return latestChapter + u'<br><hr>' + latestChapter2
            except Exception, e:
                error = str(e)
                if error.find('timed out')>-1:
                    error = 'time out'
                elif error.find('NoneType')>-1:
                    error = 'regexp can\'t match'
                print '[-] get %s latestChapter error: %s' % (url, error)
            return ''
    print '[-]', url, 'not found in regexps'
    return ''

def test():
    print getLatestChapter('http://www.kuman.com/mh-1000254/')
    print getLatestChapter('http://www.dmzj.com/info/guiwang.html')
    print getLatestChapter('http://ac.qq.com/Comic/ComicInfo/id/526501')
    print getLatestChapter('http://www.u17.com/comic/119612.html')
    print getLatestChapter('http://www.57mh.com/118/')
    print getLatestChapter('http://www.manhuatai.com/zetianji/')
    print getLatestChapter('http://www.1kkk.com/manhua20874/')
    print getLatestChapter('http://www.manhuagui.com/comic/18892/')
    print getLatestChapter('http://www.dm5.com/manhua-yaren/')
    print getLatestChapter('http://www.iyouman.com/4342/')
    print getLatestChapter('http://www.pufei.net/manhua/288/')
    print getLatestChapter('http://www.buka.cn/detail/220570')
    print getLatestChapter('http://www.kanman.com/9308/')
    exit(0)


def chapterControl(action, updateId = 0):
    jObject = fileToJson(listFile)
    resultDict = collections.OrderedDict()
    for name in jObject:
        # time.sleep(0.2)
        element = jObject[name]
        id = element['id']
        url = element['url']
        oldChapter = element['oldChapter']
        latestChapter = element['latestChapter']
        resultDict[name] = {
            'id': id,
            'url': url,
            'oldChapter': oldChapter,
            'latestChapter': latestChapter
        }
        if action == 'readAll':
            # read list
            print 'id: %s, \tname: %s,\n\t\turl: %s,\n\t\toldChapter: %s,\n\t\tlatestChapter: %s\n' % (id, name, url, oldChapter, latestChapter)
        elif action == 'updateAll':
            # update all: latestChapter
            latestChapterNew = getLatestChapter(url)
            if not (latestChapterNew == latestChapter) and latestChapterNew:
                resultDict[name]['latestChapter'] = latestChapterNew
                print '[+] great: %s has been updated to %s' % (name, latestChapterNew)
            print 'id: %s, \tname: %s,\n\t\turl: %s,\n\t\toldChapter: %s,\n\t\tlatestChapter: %s\n' % (id, name, url, oldChapter, latestChapterNew)
        elif action == 'updateAny':
            # update anyone: oldChapter and latestChapter
            if updateId == id:
                latestChapterNew = getLatestChapter(url)
                if latestChapterNew:
                    resultDict[name]['oldChapter'] = latestChapterNew
                    resultDict[name]['latestChapter'] = latestChapterNew
                    print '[+] great: %s has been updated to %s' % (name, latestChapterNew)
    if not action == 'readAll':
        rdStr = json.dumps(resultDict, ensure_ascii = False, indent = 4).encode('utf-8')
        # print rdStr
        copyListFile(listFile)
        file(listFile, 'wb').write(rdStr)
        print '[+] success: save new list file in', listFile
    showByHtml(resultDict, listFile)

def copyListFile(listFile):
    backupdir = 'backup'
    if not os.path.exists(backupdir):
        os.makedirs(backupdir)
    timestamp = str(int(time.time()))
    newFile = '%s/%s_%s' % (backupdir, timestamp, listFile)
    shutil.copy(listFile, newFile)

if __name__ == '__main__':
    reFile = 're.txt'

    help = '''example: python {0} -h
         python {0} -R
         python {0} -U
         python {0} -u 2
         python {0} -f list_360se.txt -U
         python {0} -b 360se -U -s'''.format(os.path.basename(sys.argv[0]))
    parser = argparse.ArgumentParser(epilog = help, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-R', action='store_true',
                        dest='readall',
                        help='read list?')
    parser.add_argument('-U', action='store_true',
                        dest='updateall',
                        help='update all?')
    parser.add_argument('-u', action='store',
                        type=int,
                        dest='update',
                        help='update anyone by id;')
    parser.add_argument('-t', action='store',
                        type=int,
                        dest='timeout',
                        default=20,
                        help='request timeout (default: 20);')
    parser.add_argument('-b', action='store',
                        dest='getBookmark',
                        help='get bookmark by Mainstream browsers;')
    parser.add_argument('-f', action='store',
                        dest='listFile',
                        default='list.txt',
                        help='list file;')
    parser.add_argument('-s', action='store_true',
                        dest='showHtml',
                        default=False,
                        help='show result by html?')
    args = parser.parse_args()
    readall = args.readall
    updateall = args.updateall
    update = args.update
    timeout = args.timeout
    getBookmark = args.getBookmark
    listFile = args.listFile
    showHtml = args.showHtml
    # test()
    
    if len(sys.argv) < 2:
        print help
        # chapterControl('readAll')
        # chapterControl('updateAll')
        # chapterControl('updateAny', 1)
        exit(0)

    showHtmlTmp = False
    if getBookmark == '360se':
        listFile = 'list_360se.txt'
        compatible360se()
    if readall:
        chapterControl('readAll')
    elif updateall:
        chapterControl('updateAll')
    elif update:
        chapterControl('updateAny', update)

