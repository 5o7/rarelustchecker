from bs4 import BeautifulSoup
import re
import requests
from googlesearch import search
import urllib.request
from googleapiclient.discovery import build
import random

api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
youtube = build("youtube", "v3", developerKey=api_key)

queries = []
count = 0

source = requests.get("https://rarelust.com/movies-index/").text
soup = BeautifulSoup(source, 'lxml')
rare_info = soup.find("div", class_="hfeed")
rare_info = rare_info.text
rare_info = rare_info.strip()
rare_info = rare_info.split("ABCDEFGHIJKLMNOPQRSTUVWXYZ#")
rare_info = rare_info[1]
rare_info = rare_info.split("Responses to Movies-Index")
rare_info = rare_info[0]
rare_info = rare_info.strip("\n")
rare_info = rare_info.split("\n\n")

for i in rare_info:
    i = repr(i)
    if len(i) > 6:
        str(i)
        i = i.replace("\n", "")
        i = i.replace("'", "")
        i = i.strip()
        if "&" in i:
            i = i.replace("&", "")
        if "Back to top" not in i:
            queries.append(i)

for i in range(0, 5):
    random.shuffle(queries)
for i in queries:
    print(i)

print(len(queries))

for query in queries:
    try:
        count = count + 1
        vid_ids = []
        print(count)
        search_results = search(query, 5, 'en')
        for search_result in search_results:
            if "https://www.imdb.com/title/tt" in search_result:
                imdb_link = str(search_result)
                if len(search_result) == 37:
                    break

        source = requests.get(imdb_link).text
        soup1 = BeautifulSoup(source, 'lxml')
        imdb_info = soup1.find("div", class_="title_wrapper")

        imdb_info = imdb_info.text
        imdb_info = imdb_info.strip()
        imdb_info = imdb_info.split("|")
        imdb_info = imdb_info[0].replace("\n", "")
        imdb_title = imdb_info.split(")")
        imdb_title = imdb_title[0].replace("\n", "")
        imdb_title = imdb_title.replace("  ", "") + ")"

        imdb_duration = soup1.find("div", class_="title_wrapper")
        imdb_info = str(imdb_duration)
        imdb_duration = imdb_info.split("time datetime=")
        imdb_duration = imdb_duration[1]
        imdb_duration = imdb_duration.split(">")
        imdb_duration = imdb_duration[0]
        imdb_duration = imdb_duration.replace('"', '')
        imdb_duration = imdb_duration.replace("PT", "")
        imdb_duration = imdb_duration.replace("M", "")

        print("")
        print(imdb_title)
        print("time: " + imdb_duration + " min")
        print("")
    except:
        print("imdb failed")

    try:
        query = query.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query)

        vid_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())


        vid_request = youtube.videos().list(part="contentDetails", id=",".join(vid_ids))
        vid_response = vid_request.execute()

        hours_pattern = re.compile(r"(\d+)H")
        minutes_pattern = re.compile(r"(\d+)M")
        seconds_pattern = re.compile(r"(\d+)S")

        for i in range(0, 20):
            vid_response["items"][i]["contentDetails"]
            duration = vid_response["items"][i]["contentDetails"]["duration"]
            definition = vid_response["items"][i]["contentDetails"]["definition"]
            link = "https://www.youtube.com/watch?v=" + vid_response["items"][i]["id"]

            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            total_minutes = hours*60 + minutes + int(seconds/60)

            yt_link = "https://www.youtube.com/watch?v=" + vid_ids[i]
            source2 = requests.get(yt_link).text
            soup = BeautifulSoup(source, 'lxml')
            source = requests.get(yt_link).text
            soup2 = BeautifulSoup(source, 'lxml')
            yt_info = soup2.find("div", class_="watch-main-col")
            yt_info = str(yt_info)
            yt_title = yt_info.split("content=")
            yt_title = yt_title[1]
            yt_title = yt_title.split("itemprop=")
            yt_title = yt_title[0]
            yt_title = yt_title.replace('"', "")

            upper_limit = int(imdb_duration) + 5
            lower_limit = int(imdb_duration) - 5
            if lower_limit <= total_minutes <= upper_limit:
                print(yt_title)
                print(link)
                print(definition)
                print(total_minutes)
                print()
                break
    except:
        print("youtube failed")

