import json
import requests
import os
import subprocess

exportfolder = "export"

# JSON-Datei einlesen
with open('api/ps-videos_tracks.json', 'r', encoding='utf-8') as file:
    trackData = json.load(file)  # JSON-Daten aus der Datei laden
print(f"Geladene Tracks: {len(trackData)}")

# JSON-Datei einlesen
with open('api/ps-api__videos_1.json', 'r', encoding='utf-8') as file:
    videoData = json.load(file)  # JSON-Daten aus der Datei laden

with open('api/ps-api__videos_2.json', 'r', encoding='utf-8') as file:
    videoData2 = json.load(file)  # JSON-Daten aus der Datei laden
for item in videoData2:
    videoData.append(item)
videoData2 = None

print(f"Geladene Videos: {len(videoData)}")

with open(f"api/exkl.csv", 'r', encoding='utf-8') as file:
    exklIDs = [line.strip() for line in file if line.strip()]
print(f"Anzahl an exklusiven IDs: {len(exklIDs)}")

for ID in exklIDs:
    video = next((item1 for item1 in videoData if str(item1["id"]) == str(ID)), None)
    track = next((item2 for item2 in trackData if str(item2["id"]) == str(ID)), None)
    
    if not video and track:
        print(f"{s} - No Video")
        input("Press enter to continue")
        continue
    elif video and not track:
        print(f"{s} - No Track")
        input("Press enter to continue")
        continue
    elif not video and not track:
        print(f"{s} - Nothing")
        input("Press enter to continue")
        continue
        
    #Download von YouTube (nur bei Videos vor dem 10.10.2016)
    if video["remote"] == True:
        remote_url = video["remote_url"]
        ytid = remote_url.replace("http://", "").replace("https://", "").replace("www.youtube.com/watch?v=", "")
        url_slug = video["url_slug"]
        file_name = video["publish_date"].replace(":", "-") + "_" + url_slug
        filename = os.path.join(exportfolder, file_name)
        
        try:
            # yt-dlp Befehl ausführen
            ytdlp = [
                "../yt-dlp.exe",
                "--cookies-from-browser", "firefox",
                "-f", "bestvideo+bestaudio",        # Beste Video- und Audiospuren kombinieren
                "--merge-output-format", "mp4",     # Mergen als .mp4
                "-o", f"{filename}.%(ext)s",        # Ausgabe-Dateiname
                remote_url                          # Source-URL
            ]
            subprocess.run(ytdlp, check=True)
            if not os.path.isfile(filename + ".mp4"):
                print(f"Download nicht erfolgreich: {url_slug}")
        except Exception as e:
            print(f"Fehler: {e}")
            input("Press Enter to continue...")
    #Download von pietcdn.de
    else:
        for track_item in track["tracks"]:
            url_slug = video["url_slug"]
            tracktitle = str(track_item["id"])
            file_name = video["publish_date"].replace(":", "-") + "_" + url_slug + "_" + tracktitle
            filename = os.path.join(exportfolder, file_name)
            print(file_name)
            try:
                # yt-dlp Befehl ausführen
                dash = [
                    "yt-dlp.exe", 
                    "-f", "bestvideo+bestaudio",        # Beste Video- und Audiospuren kombinieren
                    "--merge-output-format", "mp4",     # Mergen als .mp4
                    "-o", f"{filename}.%(ext)s",        # Ausgabe-Dateiname
                    track_item["sources"]["dash"]["src"]     # Source-URL
                ]
                subprocess.run(dash, check=True)
                if not os.path.isfile(filename + ".mp4"):
                    print(f"Download nicht erfolgreich: {url_slug}/{tracktitle}")
            except Exception as e:
                print(f"Fehler: {e}")
                input("Press Enter to continue...")
    