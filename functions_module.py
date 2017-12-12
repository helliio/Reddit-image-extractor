import urllib.request
import urllib.error
import json
import os

download_count = 0
error_count = 0

def get_json(url):
    header={"User-agent": "Image-extractor 1.2.0"}
    req = urllib.request.Request(url=url, headers=header)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print("HTTP Error: "+str(e.code) + "\n")
    except urllib.error.URLError as e:
        print("URL Error: "+str(e.reason) + "\n")
    else:
        data = json.loads(response.read().decode("utf-8"))
        return data

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
                print("HTTP Error: "+ str(e.code) + " for file: " + key + "\n")
                error_count += 1
                download_count -= 1
            except urllib.error.URLError as e:
                print("URL Error: "+ str(e.reason) + " for file: " + key + "\n")
                error_count += 1
                download_count -= 1

def mk_save_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir + "/"
