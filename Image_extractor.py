import urllib.request
import urllib.error
import json
import os
import config

def genRedditUrl(subreddit, sort, postLimit):
    if sort != "":
        sort = "/" + sort
    url = 'https://www.reddit.com/r/' + subreddit + sort + '/.json?limit=' + str(postLimit)
    return url

def getJson(url):
    header={'User-agent': 'Image-extractor 1.0'}
    req = urllib.request.Request(url=url, headers=header)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print('HTTPError: '+str(e.code))
    except urllib.error.URLError as e:
        print('URLError: '+str(e.reason))
    else:
        data = json.loads(response.read().decode("utf-8"))
        return data

def extractImageUrl(jsonFile):
    ret = {}
    posts = jsonFile['data']['children']
    for element in posts:
        url = element['data']['url']
        title = element['data']['title']
        asciistr = title.encode("ascii", errors="ignore").decode()
        unclean = str(asciistr)
        cleantitle = unclean.translate(str.maketrans(" ","_","/.\\?#:;*<>\"'|"))
        if (".jpg" in url or ".jpeg" in url or ".png" in url or ".gif" in url) and (not ".gifv" in url and not ".mp4" in url):
            ret[cleantitle] = url
    return ret

def downloadImg(urls,category):
    saveDir = mkSaveDir(category)
    for key, value in urls.items():
        extentionLocation = value.rfind(".")
        fileName = (saveDir + key + value[extentionLocation: extentionLocation + 4]).encode("utf-8")
        if not os.path.exists(fileName):
            print("Saving: " + fileName.decode("utf-8") + '\n')
            urllib.request.urlretrieve(value, fileName)


def mkSaveDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir + '/'

def runDownloader():
    for item in config.subreddit:
        print("--------------------------------------------------" + '\n')
        print("Starting downloads for: " + item + '\n')
        print("--------------------------------------------------" + '\n')
        url = genRedditUrl(item, config.sort ,config.postLimit)
        jsonFile = getJson(url)
        imgDict = extractImageUrl(jsonFile)
        downloadImg(imgDict,item)
        print("--------------------------------------------------" + '\n')
        print("Done downloading: " + item+ '\n')
        print("--------------------------------------------------" + '\n')

def main():
    runDownloader()


if __name__ == "__main__":
    main()
