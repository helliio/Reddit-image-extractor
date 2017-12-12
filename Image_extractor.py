import urllib.request
import urllib.error
import json
import os
import time
import config

download_count = 0
error_count = 0

def gen_reddit_url(subreddit, sort_type, sort_arg, after):
    if sort_type != "":
        sort_type = "/" + sort_type
    if sort_arg != "":
        sort_arg = "&" + sort_arg
    url = "https://www.reddit.com/r/" + subreddit + sort_type + "/.json?limit=100" + sort_arg + "&after=" + after
    return url

def get_json(url):
    header={"User-agent": "Image-extractor 1.1.1"}
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

def extract_reddit_image_url(json_file):
    ret = {}
    posts = json_file["data"]["children"]
    for element in posts:
        url = element["data"]["url"]
        title = element["data"]["title"]
        asciistr = title.encode("ascii", errors="ignore").decode()
        unclean = str(asciistr)
        clean_title = unclean.translate(str.maketrans(" ","_","/.\\?#:;*<>\"'|"))
        if (".jpg" in url or ".jpeg" in url or ".png" in url or ".gif" in url):
            if (not ".gifv" in url and not ".mp4" in url):
                ret[clean_title] = url
    return ret

def download_img(urls, category, down_limit):
    global download_count
    global error_count
    save_dir = mk_save_dir(category)
    for key, value in urls.items():
        extention_location = value.rfind(".")
        file_name = (save_dir + key + value[extention_location: extention_location + 4]).encode("utf-8")
        if (not os.path.exists(file_name)) and (download_count < down_limit):
            download_count += 1
            try:
                urllib.request.urlretrieve(value, file_name)
                print("Saving img no." + str(download_count)+ ": " + file_name.decode("utf-8") + "\n")
            except urllib.error.HTTPError as e:
                print("HTTPError: "+ str(e.code) + "\n")
                error_count += 1
                download_count -= 1
            except urllib.error.URLError as e:
                print("URLError: "+ str(e.reason) + "\n")
                error_count += 1
                download_count -= 1
            
def mk_save_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir + "/"

def run_reddit_downloader():
    for subreddit in config.subreddit:
        global download_count
        global error_count
        print("--------------------------------------------------")
        print("Starting downloads for: " + subreddit)
        print("--------------------------------------------------" + "\n")
        after = ""
        while download_count < config.down_limit and after != None:
            time.sleep(3)
            url = gen_reddit_url(subreddit, config.sort_type, config.sort_arg, after)
            json_file = get_json(url)
            img_dict = extract_reddit_image_url(json_file)
            download_img(img_dict, subreddit, config.down_limit)
            after = json_file["data"]["after"]
        print("--------------------------------------------------")
        print("Done downloading " + subreddit + " Error Count: " + str(error_count))
        print("--------------------------------------------------" + "\n")
        download_count = 0
        error_count = 0

def main():
    run_reddit_downloader()

if __name__ == "__main__":
    main()
