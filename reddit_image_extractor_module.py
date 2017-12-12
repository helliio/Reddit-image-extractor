import time
import functions_module
import menu_module
import config

def gen_reddit_url(subreddit, sort_type, sort_arg, after):
    if sort_type != "":
        sort_type = "/" + sort_type
    if sort_arg != "":
        sort_arg = "&" + sort_arg
    url = "https://www.reddit.com/r/" + subreddit + sort_type + "/.json?limit=100" + sort_arg + "&after=" + after
    return url

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

def run_reddit_downloader():
    menu_module.ini_menu()
    if config.subreddit:
        for subreddit in config.subreddit:
            functions_module.download_count = 0
            functions_module.error_count = 0
            print("--------------------------------------------------")
            print("Starting downloads for: " + subreddit)
            print("--------------------------------------------------" + "\n")
            after = ""
            while functions_module.download_count < config.down_limit and after != None:
                time.sleep(3)
                url = gen_reddit_url(subreddit, config.sort_type, config.sort_arg, after)
                json_file = functions_module.get_json(url)
                img_dict = extract_reddit_image_url(json_file)
                functions_module.download_img(img_dict, subreddit, config.down_limit)
                after = json_file["data"]["after"]
            print("--------------------------------------------------")
            print("Done downloading " + subreddit + " Error Count: " + str(functions_module.error_count))
            print("--------------------------------------------------" + "\n")
    else:
        print("no subreddit entered")
