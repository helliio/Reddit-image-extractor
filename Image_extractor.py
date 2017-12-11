import urllib.request
import urllib.error
import json
import os
import time
import config

downloadCount = 0
errorCount = 0

def genRedditUrl(subreddit, sortType, sortArg, after):
    if sortType != "":
        sortType = "/" + sortType
    if sortArg != "":
        sortArg = "&" + sortArg
    url = "https://www.reddit.com/r/" + subreddit + sortType + "/.json?limit=100" + sortArg + "&after=" + after
    return url

def getJson(url):
    header={"User-agent": "Image-extractor 1.1"}
    req = urllib.request.Request(url=url, headers=header)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print("HTTPError: "+str(e.code) + "\n")
    except urllib.error.URLError as e:
        print("URLError: "+str(e.reason) + "\n")
    else:
        data = json.loads(response.read().decode("utf-8"))
        return data

def extractImageUrl(jsonFile):
    ret = {}
    posts = jsonFile["data"]["children"]
    for element in posts:
        url = element["data"]["url"]
        title = element["data"]["title"]
        asciistr = title.encode("ascii", errors="ignore").decode()
        unclean = str(asciistr)
        cleantitle = unclean.translate(str.maketrans(" ","_","/.\\?#:;*<>\"'|"))
        if (".jpg" in url or ".jpeg" in url or ".png" in url or ".gif" in url) and (not ".gifv" in url and not ".mp4" in url):
            ret[cleantitle] = url
    return ret

def downloadImg(urls,category):
    global downloadCount
    global errorCount
    saveDir = mkSaveDir(category)
    for key, value in urls.items():
        extentionLocation = value.rfind(".")
        fileName = (saveDir + key + value[extentionLocation: extentionLocation + 4]).encode("utf-8")
        if (not os.path.exists(fileName)) and (downloadCount < config.downLimit):
            downloadCount += 1
            try:
                urllib.request.urlretrieve(value, fileName)
                print("Saving img no." + str(downloadCount)+ ": " + fileName.decode("utf-8") + "\n")
            except urllib.error.HTTPError as e:
                print("Img no." + str(downloadCount) + " HTTPError: "+ str(e.code) + "\n")
                errorCount += 1
            except urllib.error.URLError as e:
                print("Img no." + str(downloadCount) + " URLError: "+ str(e.reason) + "\n")
                errorCount += 1
            
def mkSaveDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir + "/"

def runDownloader():
    for item in config.subreddit:
        global downloadCount
        global errorCount
        print("--------------------------------------------------")
        print("Starting downloads for: " + item)
        print("--------------------------------------------------" + "\n")
        after = ""
        while downloadCount < config.downLimit and after != None:
            time.sleep(3)
            url = genRedditUrl(item, config.sortType, config.sortArg, after)
            jsonFile = getJson(url)
            imgDict = extractImageUrl(jsonFile)
            downloadImg(imgDict,item)
            after = jsonFile["data"]["after"]
        print("--------------------------------------------------")
        print("Done downloading " + item + " Error Count: " + str(errorCount))
        print("--------------------------------------------------" + "\n")
        downloadCount = 0
        errorCount = 0

def main():
    runDownloader()

if __name__ == "__main__":
    main()
