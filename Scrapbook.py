#!/usr/bin/env python

# Written by Irving Y. Ruan <irvingruan@gmail.com>

"""Usage: ./Scrapbook.py [OPTIONS] group_id

group_id must the flickr NSID for a group

OPTIONS:
  -v or --verbose
  -e or --equal : width and height of photo must be the same
  -s size or --size size : size of photo Thumbnail, Small,
                           Medium, Large, Original
  -n number or --number number : the number of photos to retrieve

"""

import os
import sys
import flickr
import urllib
import statichtml
import errno
from getopt import getopt, GetoptError

scrapbook_gallery_path = os.path.expanduser('~/Desktop/Scrapbook/')

def create_scrapbook_dir():
 
    try:
        os.makedirs(scrapbook_gallery_path)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise Exception("Scrapbook directory already exists!")
            sys.exit(-1)   
            
def generate_html(urls):
    
    try:
        html_output = open('index.html', 'w')
        html_output.write(statichtml.header)
        html_output.write(statichtml.body_start)
        
        for url in urls:
            html_output.write("\t\t\t<div class=\"item\">\n")
            html_output.write("\t\t\t\t<img class=\"content\" src=\"" + str(url) + "\"/>\n")
            html_output.write("\t\t\t</div>\n")


        html_output.write(statichtml.body_end)   
        html_output.close()
            
    except:
        sys.stderr.write("Error: Unable to generate index.html.")
        sys.exit(-1)          

def make_scrapbook_data():
    
    try:
        # Copy over the .html, .js, and .css files
        shutil.move(os.getcwd() + "/index.html", scrapbook_gallery_path)
        
        rv = subprocess.Popen('cp -rf ' + os.getcwd() + '/website/. ' + scrapbook_gallery_path, shell=True)
        rv.wait()
        
        # Fire up Safari to see the result
        rv = subprocess.Popen('open /Applications/Safari.app ' + scrapbook_gallery_path + '/index.html', shell=True)
        rv.wait()
        
    except:
        sys.stderr.write("Error: Could not produce Scrapbook HTML/CSS files.\n")
        sys.exit(-1)


def get_url(photo, size, equal=False):
    """Retrieves a url for the photo.  (flickr.photos.getSizes)
    
    photo - the photo
    size - what size 'Thumbnail, Small, Medium, Large, Original'
    equal - should width == height?
    """
    
    method = 'flickr.photos.getSizes'
    data = flickr._doget(method, photo_id=photo.id)
    for psize in data.rsp.sizes.size:
        if psize.label == size:
            if equal and psize.width == psize.height:
                return psize.source
            elif not equal:
                return psize.source
    raise flickr.FlickrError, "No URL found"

def get_photo_urls(group_id, size, number, equal=False):
    group = flickr.Group(group_id)
    photos = group.getPhotos(per_page=number)
    urls = []
    for photo in photos:
        try:
            urls.append(get_url(photo, size, equal))
        except flickr.FlickrError:
            if verbose:
                print "%s has no URL for %s" % (photo, size)
    return urls
    
def grab_api_key():
    api_key_file = open('API_KEY.txt', 'r')
    
    

def main(*argv):
    try:
        (opts, args) = getopt(argv[1:],\
                              'ves:n:',\
                              ['verbose', 'size', 'equal', 'number'])
    except GetoptError, e:
        print e
        print __doc__
        return 1

    size = 'Medium'
    equal = False
    number = 5

    for o, a in opts:
        if o in ('-s' , '--size'):
            size = a.capitalize()
        elif o in ('-e', '--equal'):
            equal = True
        elif o in ('-v', '--verbose'):
            verbose = True
        elif o in ('-n', '--number'):
            number = a
        else:
            print "Unknown argument: %s" % o
            print __doc__
            sys.exit(0)

    
    if len(sys.argv) < 1:
        print "You must specify a group"
        print __doc__
        sys.exit(0)   
        
    group_id = sys.argv[1]
    
    urls = get_photo_urls(group_id, size, number, equal)
    
    create_scrapbook_dir()
    generate_html(urls)

if __name__ == "__main__":
    main()
    sys.exit(0)