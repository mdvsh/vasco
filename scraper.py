"""
hash of key (abbreviation) : value of another hash with building parameters
"""

import urllib.request
from bs4 import BeautifulSoup
import json

DATA_LINK = "https://ro.umich.edu/calendars/schedule-of-classes/locations"

with urllib.request.urlopen(DATA_LINK) as response:
    data = response.read()

data = data.decode("utf-8")

# seed with locations (ignore paragraph containing regents of umich)
sauce = BeautifulSoup(data, "html.parser")
arr_of_locns = []
for elem in sauce.find_all("p")[:-2]:
    # append if not empty string
    if elem.text != "":
        arr_of_locns.append(elem.text)

# clean the array and make dict
building_data = {"COUNT": len(arr_of_locns), "DATA": {}}
for build_data in arr_of_locns:
    data = build_data.split("\n")
    building_data["DATA"][data[0]] = data[1:]

# save dict as json
with open("buildings.json", "w") as f:
    json.dump(building_data, f, indent=4, sort_keys=True)

