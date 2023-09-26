''' Important! Please read below

Make sure you install the necessary dependencies before running (pip install wikidataintegrator)
The erase_png function has a bug in it. See comments below
Not all code was made by me (Vijay Kethanaboyina). Some of the functions that access Wikidata API were made with ChatGPT

Make sure you replace the username/password variables!
'''

# Delete the below lines and replace them with your own username / password
my_username = ""
my_password = ""

from wikidataintegrator import wdi_login, wdi_core, wdi_helpers
import json
import os
import time

# Important Global Variables
login = wdi_login.WDLogin(my_username, my_password)
wikidata_url_stem = "https://www.wikidata.org/wiki/"
qid_dict = json.load(open("qid_to_label.json"))

# This function is supposed to remove the PNG entries from Wikidata items that already have an SVG
# Unfortunately it does not work
def erase_png(wikidata_entity_id,file_name):
  # Fetch the existing statements for the Wikidata item
  item = wdi_core.WDItemEngine(wd_item_id=wikidata_entity_id)

  # Initialize a list to store the statements to delete
  statements_to_delete = []

  # Loop through the statements to find the PNG image(s) and add them to the list
  for statement in item.statements:
      if statement.get_prop_nr() == "P18":  # Assuming P18 is used for image statements
          # Check if the statement contains a PNG image (you can customize this condition)
          if statement.get_value().endswith(".png"):
              statements_to_delete.append(statement)

  # Check if any PNG image statements were found
  if statements_to_delete:
      # Get the current revision of the Wikidata item
      #current_revision = item.get_last_revision()
      current_revision = wdi_helpers.id_mapper(item.write(login, entity_type="item"))

      # Delete the selected PNG image statement(s)
      for statement in statements_to_delete:
          '''
          BELOW is the broken line of code. Debug message says that the argument 'statement' is bad
          Might be formatted wrong?
          See this API link for info on how the remove function works:
          https://www.wikidata.org/w/api.php?action=help&modules=wbremoveclaims

          This link, which contains the Wikidataintegrator source code might also be useful:
          https://github.com/SuLab/WikidataIntegrator/blob/main/wikidataintegrator/wdi_core.py
          '''
          item.delete_statement(statement, revision=current_revision, login=login)
          # This line of code does not work. Not sure how to fix it

      print(f"PNG image statement(s) deleted from Wikidata item {wikidata_entity_id}.")
  else:
      print("No PNG image statement(s) found.")

# Most important function in this file
def change_image(wikidata_entity_id,file_name):
  url = wikidata_url_stem + wikidata_entity_id
  file_name += ".svg"
  #print(url,wikidata_entity_id, file_name)

  statement = wdi_core.WDCommonsMedia(file_name, prop_nr="P18")
  item = wdi_core.WDItemEngine(wd_item_id=wikidata_entity_id, data=[statement])
  statement.set_value(file_name)

  item.update(data=[statement])
  item.write(login, edit_summary="Updating image")
  print(f"Updated the image on Wikidata entity {wikidata_entity_id}.")

# Obtain q-id given URL of wikidata entry
def get_q_id(url):
  q_index = url.find('Q')
  if q_index != -1:
    # Extract everything after 'Q'
    result = url[q_index + 1:]  # Add 2 to skip 'Q='
    return result

# Helper function that gets the image link for a given wikidata URL
# Not necessary, but could be helpful
def get_image_link_from_wikidata_url(wikidata_url):
    try:
        # Extract the Wikidata entity ID from the URL
        entity_id = wikidata_url.split("/")[-1]

        # Log in to Wikimedia Commons
        commons_wiki = Wiki("commons.wikimedia.org", my_username, my_password)

        # Query the Wikidata item to get the image property (P18)
        item = wdi_core.WDItemEngine(wd_item_id=entity_id)
        item.get_wd_json_representation()

        # Get the image URL from the image property (P18)
        image_property = item.wd_json_representation["claims"].get("P18")
        if image_property:
            image_url = image_property[0]["mainsnak"]["datavalue"]["value"]
            return image_url

        print("No image found on the Wikidata item.")
        return None

    except Exception as e:
        print("An error occurred:", str(e))
        return None


for qid in qid_dict:
  change_image('Q'+qid,qid_dict[qid])

  '''
  The below line is commented out because it doesn't work (see the function def for info on the bug)
  '''
  #erase_png(curr_id,qid_dict[curr_id[1:]])

  # You have to sleep for 0.5s because of the 60 second rate limit
  time.sleep(0.5)

  # Debug print
  #print(curr_q_id, q_id_to_form_label, url)
