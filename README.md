# Wikimedia Commons Cuneiform Uploader
A simple Python script that uploads cuneiform images to Wikimedia commons. Not all of this code was written by me. It is a modified version of [this](https://github.com/fastily/simple-commons-uploader) Python package called "Simple Commons Uploader" (or `scu` for short). The images are not provided with this repository. You can find some relevant Cuneiform images at [this link](https://github.com/vkethana/cuneiform_convert/).
The second file, `entry_editor.py`, allows you to batch edit which image files are associated with various Wikidata items. Make sure to install [WikidataIntegrator](https://github.com/SuLab/WikidataIntegrator) first.

# How to use this repository
Run `python uploader.py -i name_of_folder`, where `name_of_folder` is the path to an image folder containing the images you want uploaded to Wikimedia Commons. Type in your credentials at the prompt.

# Metadata Generation
The image description is the name of the file, without the extension. The image date is the date on which the script is run.
The image author and source will default to my name and a GitHub repository that I own. But this can be easily changed by editing the script.

# Caveats
Wikidata rate limits may slow you down. This is especially true for `entry_edtior.py`. To avoid rate limits, the program sleeps for 0.5 seconds after each image edit.
