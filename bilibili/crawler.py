import requests
import json
import os

print("Set the following conditions. Program breaks if one of them is reached.")
valid_expected = eval(input("Number of info you expect(integer): "))
max_current_uid = eval(input("Max UserID you expect(integer): "))

files = os.listdir(os.getcwd())
if "error" in files:
    os.remove("error")
if "result" in files:
    os.remove("result")

header = {"user-agent":"Chrome/10"}
valid = 0
invalid = 0 # total number of videos and Bangumi is less than 10
current_uid = 1
f = open("result","a")
e = open("error", "a")
f.write("[{}")

true = "true"
false = "false"
null = []


def resolve_coding(data):
    try:
        text = eval(data) 
    except:
        text = ""
    return text


def get_info(user_id):
    global header
    header["Content-Type"] = "application/x-www-form-urlencoded"
    header["Referer"] = "http://space.bilibili.com/{}".format(user_id)
    data = {"mid": user_id}
    text = ""
    try:
        r = requests.post("http://space.bilibili.com/ajax/member/GetInfo", headers=header, data=data, timeout=2)
        text = resolve_coding(r.text)
    except:
        e.write("Timeout: get_info({})\r\n".format(user_id))
        return {}
    if text["status"] == "false":
        return {}

    text = text["data"]
    info = {}
    info["mid"] = text["mid"]
    info["name"] = text["name"]
    info["sex"] = text["sex"]
    try:
        info["birthday"] = text["birthday"]
    except:
        info["birthday"] = "Unknown"
    return info


def get_video_info(video):
    url = "http://api.bilibili.com/x/tag/archive/tags?aid={}".format(video["aid"])
    text = ""
    video_info = {}
    video_info["aid"] = video["aid"]
    video_info["title"] = video["title"]
    try:
        r = requests.get(url, timeout=2)
        text = resolve_coding(r.text)
    except:
        e.write("Timeout: get_video_info({})\r\n".format(video["aid"]))
        return video_info

    video_info["tags"] = []
    for tag in text["data"]:
        video_info["tags"].append(tag["tag_name"])
    return video_info


def get_submit_videos(user_id):
    url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid={}".format(user_id)
    text = ""
    try:
        r = requests.get(url, timeout=2)
        text = resolve_coding(r.text)
    except:
        e.write("Timeout: get_submit_videos({})\r\n".format(user_id))
        return []
    submit_videos = text["data"]["vlist"]
    return submit_videos


def get_bangumi_info(bangumi):
    url = "http://bangumi.bilibili.com/jsonp/seasoninfo/{}.ver?callback=seasonListCallback".format(bangumi["season_id"])
    text = ""
    bangumi_info = {}
    bangumi_info["season_id"] = bangumi["season_id"]
    bangumi_info["title"] = bangumi["title"]
    try:
        r = requests.get(url, timeout=2)
        text = resolve_coding(r.text[19:-2])
    except:
        e.write("Timeout: get_bangumi_info({})\r\n".format(bangumi["season_id"]))
        return bangumi_info
    bangumi_info["tags"] = []
    for tag in text["result"]["tags"]:
        bangumi_info["tags"].append(tag["tag_name"])

    return bangumi_info


def get_bangumi_list(user_id):
    url = "http://space.bilibili.com/ajax/Bangumi/getList?mid={}".format(user_id)
    text = ""
    try:
        r = requests.get(url, timeout=2)
        text = resolve_coding(r.text)
    except:
        e.write("Timeout: get_bangumi_list({})\r\n".format(user_id))
        return []
    if text["status"] == "false":
        e.write("Error: get_bangumi_list({})\r\n".format(user_id))
        return []
    bangumi_list = text["data"]["result"]
    return bangumi_list


def get_favorite_list(user_id):
    url = "http://api.bilibili.com/x/v2/fav/video?vmid={}".format(user_id)
    text = ""
    try:
        r = requests.get(url, timeout=2)
        text = resolve_coding(r.text)
    except:
        e.write("Timeout: get_favorite_list({})\r\n".format(user_id))
        return []
    if text["code"] != 0:
        e.write("Error: get_favorite_list({})\r\n".format(user_id))
        return []
    favorite_list = text["data"]["archives"]
    return favorite_list


def push_data(user_info, videos_info, bangumis_info, favorite_info):
    global valid
    data = user_info.copy()
    data["submitVideos"] = videos_info
    data["bangumi"] = bangumis_info
    data["favorite"] = favorite_info

    f.write(",\r\n")
    f.write(json.dumps(data)+"\r\n")
    valid += 1


def crawler_user(user_id):
    global invalid
    try:
        user_info = get_info(user_id)
    except:
        invalid += 1
        e.write("Error: get_info({})\r\n".format(user_id))
        return
    if user_info == {}:
        invalid += 1
        e.write("Error: get_info({})\r\n".format(user_id))
        return

    # if user_info["sex"] == "":
    #     invalid += 1
    #     e.write("Ignore: Even no gender! {}\r\n".format(user_id))
    #     return

    submit_count, favorite_count, bangumi_count = 0, 0, 0

    submit_videos = get_submit_videos(user_id)
    # if submit_videos == []:
    #     invalid += 1
    #     e.write("Ignore: No submit of user {}!\r\n".format(user_id))
    #     return

    videos_info = []
    for video in submit_videos:
        try:
            video_info = get_video_info(video)
            submit_count += 1
        except:
            e.write("Error: get_video_info({})\r\n".format(video["aid"]))
            continue
        videos_info.append(video_info)

    bangumi_list = get_bangumi_list(user_id)
    # if bangumi_list == []:
    #     invalid += 1
    #     e.write("Ignore: No bangumi for user {}!\r\n".format(user_id))
    #     return

    bangumis_info = []
    for bangumi in bangumi_list:
        try:
            bangumi_info = get_bangumi_info(bangumi)
            bangumi_count += 1
        except:
            e.write("Error: get_bangumi_info({})\r\n".format(bangumi["season_id"]))
            continue
        bangumis_info.append(bangumi_info)

    favorite_list = get_favorite_list(user_id)
    # if favorite_list == []:
    #     invalid += 1
    #     e.write("Ignore: No favorite for user {}!\r\n".format(user_id))
    #     return

    favorite_info = []
    for video in favorite_list:
        try:
            video_info = get_video_info(video)
            favorite_count += 1
        except:
            e.write("Error: get_video_info({})\r\n".format(video["aid"]))
            continue
        favorite_info.append(video_info)

    # if favorite_count + bangumi_count + submit_count < 10:
    #     invalid += 1
    #     e.write("Ignore: Too few info of user {}\r\n".format(user_id))
    #     return

    push_data(user_info, videos_info, bangumis_info, favorite_info)


while valid < valid_expected:
    print("Crawling user {}...".format(current_uid))
    crawler_user(current_uid)
    print("Crawl done: user {}".format(current_uid))
    current_uid += 1
    if current_uid % 100 == 0:
        f.write("]")
        f.close()
        e.close()
        f = open("result{}".format(current_uid / 100), "a")
        e = open("error{}".format(current_uid / 100), "a")
        f.write("[{}")
        print("Current UID reached: ", current_uid)
    if current_uid > max_current_uid:
        break


f.write("]")
f.close()
e.close()

# cat result | jq . > out.json
# out.json is formated

print("Valid info: {}".format(valid))
print("Invalid info: {}".format(invalid))
print("Current_uid: {}".format(current_uid))
print("Finished")

