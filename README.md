Scrapbook
=====

**Visualize your Flickr photos in a cool way**

Written by Irving Y. Ruan [irvingruan@gmail.com](irvingruan@gmail.com)

![Roundabout](https://github.com/irvingruan/Scrapbook/raw/master/samples/Roundabout.png)

![Cover Flow](https://github.com/irvingruan/Scrapbook/raw/master/samples/BlackCoverFlow.png)

![Screwdriver](https://github.com/irvingruan/Scrapbook/raw/master/samples/Screwdriver.png)

## About

Scrapbook is a Python tool that grabs your (or anybody's public) Flickr photos and generates the HTML and CSS files to visualize them in an elegant and intuitive way.

## Requirements

You will need to [sign up](http://www.flickr.com/services/api/misc.api_keys.html) for a Flickr API key, which is free! After you get a key (which is right after you sign up), you will need to add it to the included file, `config.py`.

Just paste your key and secret that Flickr provides for you in the the `API_KEY` and `API_SECRET` fields and you're set. Unfortunately, I cannot provide *my* Flickr key and secret, as that would bring up issues of potential abuse. ;-)

Scrapbook runs on Mac OS X  and needs Python. I plan to "appify" this tool in the future as this project merely serves as a learning experience in data visualization and Python.

## Usage

The current version only supports grabbing photos by a specific Flickr Photoset ID. I'm sticking with this [for now] for two reasons:

1. Flickr Photoset IDs are easy to obtain. They exist in the URL.
2. Some people have hundreds, if not thousands, of photos. Grabbing *all* the photos for a user is expensive on the API.

I plan on supporting grabbing photos by galleries and groups in the future, though.

In the meantime, to run Scrapbook:

`./Scrapbook.py photoset_id`

Where `photoset_id` is the ID that corresponds to a Flickr Photoset. For example, one of my Photosets, "Perspectives in Design", is located at the URL [<http://www.flickr.com/photos/irvingruan/sets/72157628025609024/>](http://www.flickr.com/photos/irvingruan/sets/72157628025609024/). The Photoset ID is thus `72157628025609024`.

Simply doing:

`./Scrapbook.py 72157628025609024`

Will generate the visualization for all photos in that Photoset.

## Legal

Scrapbook is Copyright (c) 2012 Irving Ruan and BSD licensed. The full text of the license can be found in LICENSE.



