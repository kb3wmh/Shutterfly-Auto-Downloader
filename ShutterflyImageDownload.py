import urllib.request
import time

#Program Settings
#To use this program, point change this a directory with an HTML source from a shutterfly album page
ALBUM_HTML_SOURCE_PATH = "C:\\Users\\charl\\Documents\\banquet2018\\divisionals"


def trimToImage(albumText):
    # The images we want have these tags in the album HTML source
    nextImage = albumText.find("class=\"pic-item")
    if nextImage == -1:
        return "EOF"
    albumText = albumText[(nextImage + 1):]
    return albumText

def extractURL(albumText):
    #Get the next image
    albumText = trimToImage(albumText)
    if albumText == "EOF":
        return "", "EOF"
    urlStartPos = albumText.find("src=\"") + 5
    urlEndPos = albumText.find("\">", urlStartPos)
    
    url = albumText[urlStartPos:urlEndPos]

    url = "https:" + url
    return url, albumText

def downloadImage(url, id):
    try:
        urllib.request.urlretrieve(url, ALBUM_HTML_SOURCE_PATH + "\\" + str(id) + ".jpg")
        print (id)
    except:
        return


if __name__ == "__main__":
    #This assumes that the album HTML is saved with the name album.txt
    album = open(ALBUM_HTML_SOURCE_PATH + "\\album.txt")
    thumbURLs = []
    photoURLs = []

    albumAsString = album.read()

    albumText = albumAsString
    while albumText != "EOF":
        url, albumText = extractURL(albumText)
        if url != "":
            thumbURLs.append(url)
        
    for url in thumbURLs:
        # Change the thumbnail url to the large image url
        # These values may have to be changed depending on your album source
        startPos = url.find("18108")
        url  = url[:startPos] + "10108" + url[startPos + 5:]
        photoURLs.append(url)


    id = 0
    for url in photoURLs:
        downloadImage(url, id)
        id += 1

        #Wait 3 secs to evade a possible IP ban
        time.sleep(3)