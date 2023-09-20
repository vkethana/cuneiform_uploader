# Wikimedia Commons Cuneiform Uploader
A simple Python script that uploads cuneiform images to Wikimedia commons. Not all of this code was written by me. It is a modified version of [this](https://github.com/fastily/simple-commons-uploader) Python package called "Simple Commons Uploader" (or `scu` for short). 
# How to use this repository
Run `python uploader.py -i name_of_folder`, where `name_of_folder` is the path to an image folder containing the images you want uploaded to Wikidata. Type in your credentials at the prompt.

# Metadata Generation
The image description is the name of the file, without the extension. The image date is the date on which the script is run.
The image author and source will default to my name and a GitHub repository that I own. But this can be easily changed by editing the script.

# Licenses
Important: The code is under a GNU GPL v3 license, but the images are under a Creative Commons Attribution-Share Alike 4.0 International license.
