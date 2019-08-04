# Pexels image downloader

## Description:
Download large amounts of images from [Pexels][0] via terminal.  

## Dependencies:
- `pip install requests`  
- `pip install pexels-api`  

## Installation:
`git clone https://github.com/AguilarLagunasArturo/pexels-image-downloader.git`

## Setup:
Edit pexels_user/\__init\__.py file with your Pexels API as follows:
```python
API_KEY = 'your-pexels-api-key'
```
You can get an API by [signing up][2] in [Pexels][0] and then [Request access][1].

## Usage:
`python download.py [options] [query] [photos] [path]`

### Arguments:
|Argument|Description|Required|
|:-|:-|:-|
|options|Specify an [option][5]|No|
|query|Type a string with the topic of the search|Yes|
|photos|Type the number of photos you wish to download|Yes|
|path|Type the path to an existing directory in which the photos will be downloaded. Current directory assumed if not given|No|

### Options:
|Option|Description|
|:-|:-|
|-v|Verbose mode will print information about each photo|
|-d|Photos will have a description in their filename|
|-i|Photos will have their pexels id in their filename|
|-p|Photos will have their photographer in their filename|
|-o|Photos will be organized by photographer path/query/photographer/filename with description-pexels-id as filename|
|-c|Download compressed size photos, original aspect ratio|
|-l|Download large size photos, maximum width of 1880px and a maximum height of 1300px, original aspect ratio|
|-m|Download medium size photos, maximum height of 350px and a flexible width, original aspect ratio|
|-s|Download small size photos, maximum height of 130px and a flexible width, original aspect ratio|

### Notes:
- By default the images will be downloaded with the original size in path/query/filename and they will be enumerated.  
- You can only choose one size for the images.
- The -o option overwrites -d, -i, and -p.

## Examples
|Command|Description|
|:-|:-|
|`python download.py koala 10`|Download 10 koala images (current directory assumed)|
|`python download.py -v koala 10`|Download 10 koala images and show information while downloading (current directory assumed)|
|`python download.py -p koala 10`|Download 10 koala images with the photographer in its filename (current directory assumed)|
|`python download.py -c koala 10`|Download 10 koala images with a compressed size (current directory assumed)|
|`python download.py -o koala 10`|Download 10 koala images and organized them by photographer (current directory assumed)|
|`python download.py koala 10 ~/Pictures`|Download 10 koala images in ~/Pictures|
|`python download.py -v -s -o koala 50 ~/Pictures`|Download 50 koala images in ~/Pictures with a small size and organized by photographer (You can combine options.)|
|`python download.py 'cats and dogs' 10`|Download 10 'cat and dogs' images (*__Note__*: If you want to make a query with spaces make sure to use double or single quotes 'your query' or "your query")|
---
#### Packages documentation:
- [pexels-api][3]
- [requests][4]

[0]: https://www.pexels.com/                            "Pexels: Website"
[1]: https://www.pexels.com/api/                        "Pexels: API website"
[2]: https://www.pexels.com/join/                       "Pexels: Sign up page"
[3]: https://github.com/AguilarLagunasArturo/pexels-api "Source code: pexels-api package"
[4]: https://2.python-requests.org/en/master/           "Documentation: requests package"
[5]: #options                                           "download.py: options"
