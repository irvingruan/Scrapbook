#!/usr/bin/env python

# Written by Irving Y. Ruan <irvingruan@gmail.com>

"""Usage: ./Scrapbook.py [OPTIONS] photoset_id

photoset_id must the flickr NSID for a photoset

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
import shutil
import subprocess
from getopt import getopt, GetoptError

scrapbook_photoset_dir = os.path.expanduser('~/Desktop/Scrapbook/')

DEPLOY_SB_FLAG = True

def create_scrapbook_dir():
    """Make the output folder to hold the HTML/CSS files"""
 
    try:        
        if os.path.isdir(scrapbook_photoset_dir):
            shutil.rmtree(scrapbook_photoset_dir)
            
        os.makedirs(scrapbook_photoset_dir)
    except:
        sys.stderr.write("Error: Could not make scrapbook photoset directory at %s\n" % scrapbook_photoset_dir)
            
def generate_html(urls):
    """Make the root index.html with references to Flickr photos"""
    
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
    """Copy over the default package for Scrapbook to output directory"""
    
    try:
        # Copy over the .html, .js, and .css files
        shutil.move(os.getcwd() + "/index.html", scrapbook_photoset_dir)
        
        rv = subprocess.Popen('cp -rf ' + os.getcwd() + '/website/. ' + scrapbook_photoset_dir, shell=True)
        rv.wait()
        
        # Fire up Safari to see the result
        rv = subprocess.Popen('open /Applications/Safari.app ' + scrapbook_photoset_dir + '/index.html', shell=True)
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
    
def get_photo_urls_for_user(user_id, size, number, equal=False):
    """TO DO"""
    
def get_photo_urls_for_photoset(photoset_id, size, equal=False):
    """Retrieves the photo URLs for a photoset"""
    
    photoset = flickr.Photoset(photoset_id, None, None)
    info = photoset.getInfo()
    
    sys.stdout.write("Grabbing photos for Photoset '%s'...\n" % info[0])
    
    photos = photoset.getPhotos()
    urls = []
    for photo in photos:
        try:
            urls.append(get_url(photo, size, equal))
        except flickr.FlickrError:
            if verbose:
                print "%s has no URL for %s" % (photo, size)
    return urls

def get_photo_urls_for_group(group_id, size, number, equal=False):
    """Retrieves the photo URLs for a group"""
    
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
        print "You must specify a photoset ID."
        print __doc__
        sys.exit(0)   
        
    id = sys.argv[1]
    
    if os.path.isdir(scrapbook_photoset_dir):
        sys.stderr.write("Scrapbook photoset gallery already exists at %s. Recreate anyway? (y/n):" % scrapbook_photoset_dir)
        key = 0
        try:
            key = sys.stdin.read(1)
        except KeyboardInterrupt:
            key = 0
            
        if key == 'y':
            urls = get_photo_urls_for_photoset(id, size, equal)
            
            if DEPLOY_SB_FLAG:
                create_scrapbook_dir()
                generate_html(urls)
                make_scrapbook_data()
            
            sys.exit(0)
            
        elif key == 'n':
            sys.stderr.write("\nView your Flickr photoset at " + scrapbook_photoset_dir)
            sys.exit(0)
        elif key == 0:
            sys.stderr.write("\nError: keyboard interrupted.")
            sys.exit(-1)
    else:
        urls = get_photo_urls_for_photoset(id, size, equal)
        
        if DEPLOY_SB_FLAG:
            create_scrapbook_dir()
            generate_html(urls)
            make_scrapbook_data()


if __name__ == "__main__":
    main()
    sys.exit(0)