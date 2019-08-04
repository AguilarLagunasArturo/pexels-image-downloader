# Author:   Arturo Aguilar Lagunas
# Purpose:  Download photos from https://www.pexels.com/
from pexels_api import API
from pexels_user import API_KEY
import requests
import sys
import os
# Get args
args_boundary = (2,12)
required_args_boundary = (2,3)
usage = "Usage: " + sys.argv[0] + " [options] [query] [photos] [path]"
long_usage = usage + """\n
Description:        Download photos from https://www.pexels.com
Arguments:
    Required:
        query:      A string with the topic of the search
        photos:     The number of photos you wish to download
    Not required:
        path:       The path to an existing directory in which the photos will be downloaded. Current directory assumed if not given
        Options:
            -v:     Verbose mode will print more information about each photo
            -d:     Photos will have a description in their filename
            -i:     Photos will have their pexels id in their filename
            -p:     Photos will have their photographer in their filename
            -o:     Photos will be organized by photographer path/query/photographer/filename with description-pexels-id as filename
            -c:     Download compressed size photos, original aspect ratio
            -l:     Download large size photos, maximum width of 1880px and a maximum height of 1300px, original aspect ratio
            -m:     Download medium size photos, maximum height of 350px and a flexible width, original aspect ratio
            -s:     Download small size photos, maximum height of 130px and a flexible width, original aspect ratio
Notes:
By default the photos will be downloaded with the original size in path/query/filename and they will be enumerated.
You can only choose one size for the photos.
The -o option overwrites -d, -i, and -p"""
args = sys.argv[1:]
if len(args) == 0 or (len(args) == 1 and args[0] == "--help"):
    print(long_usage)
    exit()
if len(args) < args_boundary[0] or len(args) > args_boundary[1]:
    print(usage)
    exit()
required_args = []
optional_args = []
query = None
total_photos = None
path = os.getcwd()
options = {
    "-v": False,
    "-i": False,
    "-d": False,
    "-p": False,
    "-o": False,
    "-c": False,
    "-l": False,
    "-m": False,
    "-s": False
}
sizes = ["-c", "-l", "-m", "-s"]
required_args = args
# Get required_args and optional_args
optional_args = [arg for arg in args if arg in options]
optional_args = list(dict.fromkeys(optional_args))
if len([size for size in sizes if size in optional_args]) > 1:
    print(usage)
    print("Too many sizes")
    exit()
required_args = [arg for arg in args if arg not in options]
if len(required_args) < required_args_boundary[0] or len(required_args) > required_args_boundary[1]:
    print(usage)
    exit()
# Get options
for option in optional_args:
    options[option] = True
query = required_args[0]
try:
    total_photos = int(required_args[1])
except:
    print("{}: Must be hole number".format(required_args[1]))
    print(usage)
    exit()
if total_photos < 1:
    print("{}: Minimum value 1".format(total_photos))
    print(usage)
    exit()
if len(required_args) == 3:
    if os.path.isdir(required_args[2]):
        path = required_args[2]
    else:
        print("{}: Must be a directory".format(required_args[2]))
        print(usage)
        exit()
# Create api object
api = API(API_KEY)
# Search photos
print("Searching:\t{}".format(query))
per_page = total_photos if total_photos < 80 else 80
api.search(query, per_page)
print("Total results: {}".format(api.total_results))
# Check if there are photos
if not api.json["photos"]: exit()
# If there aren't enough photos assign new total_photos
if total_photos > api.total_results:
    total_photos = api.total_results
    print("There is only {} photos about '{}'".format(total_photos, query))
# Create directory if does not exists
path = os.path.join(path, query.replace(" ", "-"))
if not os.path.isdir(path):
    os.mkdir(path)
print("Writing to {}".format(path))
# Get photos
photos = 0
download_url = ""
break_loop = False
while True:
    for photo in api.get_entries():
        photos = photos + 1
        filename = str(photos).zfill(len(str(total_photos)))
        if options["-d"]:
            filename += "-" + photo.description
        if options["-i"]:
            filename += "-" + str(photo.id)
        if options["-p"]:
            filename += "-" + photo.photographer.replace(" ", "-")
        dir = path
        if options["-o"]:
            filename = "{}-{}".format(photo.description, photo.id)
            dir = os.path.join(path, photo.photographer.replace(" ", "-"))
            print("Writing to ", dir)
            if not os.path.isdir(dir):
                os.mkdir(dir)
        if options["-c"]:
            download_url = photo.compressed
            filename += ".jpg"
        elif options["-l"]:
            download_url = photo.large2x
            filename += ".jpg"
        elif options["-m"]:
            download_url = photo.medium
            filename += ".jpg"
        elif options["-s"]:
            download_url = photo.small
            filename += ".jpg"
        else:
            download_url = photo.original
            filename += "." + photo.extension if not photo.extension == "jpeg" else ".jpg"
        if options["-v"]:
            # if Verbose
            print()
            print("Downloading:\t{}".format(photo.original))
            print("Photo url:\t{}".format(photo.url))
            print("photographer:\t{}".format(photo.photographer))
            print("Progress:\t{}/{}".format(photos, total_photos))
        else:
            if photos == total_photos:
                print("Donwloading: {}/{}".format(photos, total_photos))
            else:
                print("Donwloading: {}/{}".format(photos, total_photos), end="\r")
        # Download photos
        photo_path = os.path.join(dir, filename)
        with open(photo_path, "wb") as f:
            try:
                f.write(requests.get(download_url, timeout=15).content)
            except:
                print("Interrupted {} photos dowloaded".format(photos-1))
                os.remove(photo_path)
                if not os.listdir(dir):
                    os.rmdir(dir)
                    if options["-o"]:
                        if not os.listdir(os.path.split(dir)[0]):
                            os.rmdir(os.path.split(dir)[0])
                break_loop = True
                break
        if photos == total_photos:
            break_loop = True
            break
    if break_loop: break
    if not api.search_next_page(): break
