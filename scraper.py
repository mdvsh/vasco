import urllib.request
from urllib.error import URLError
from urllib.parse import urlencode, quote_plus
from bs4 import BeautifulSoup
import sys, os, json

DATA_LINK = "https://ro.umich.edu/calendars/schedule-of-classes/locations"
API_LINK = "https://www.google.com/maps/search/?api=1"

AREAS = [
    "Jackson Hole, Wyoming",
    "Pinckney, Michigan",
    "Monroe, Michigan",
    "Northville, Michigan",
    "Dearborn, Michigan",
    "Pellston, Michigan",
]


def seed(data):
    """
    :param data: decoded response object from link
    :return building_data: map of building abbreviations to building parameters
    """
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
        properties = {
            "location": data[1],
            "area": data[2],
            "gmap_link": make_gmap_link(data[1], data[2]) if data[0] != "ARR" else "",
        }
        building_data["DATA"][data[0]] = properties
    print("Successfully seeded and parsed data")
    return building_data


def save(building_data):
    """
    :param building_data: map of building abbreviations to building parameters
    :return None: saves data to file
    """
    try:
        with open(os.path.join(os.getcwd(), "data", "buildings.json"), "w") as f:
            json.dump(building_data, f, indent=4, sort_keys=True)
    except IOError as e:
        print("Error saving data: ", e.reason)
        sys.exit(1)
    else:
        print("Successfully saved data")


def make_gmap_link(location, area):
    """
    :param building_address: address of building
    :return: link to google maps with encoded address as per google specs
    """
    if area in AREAS:
        location = f"{location} {area.replace(',', '')}"
    else:
        location = f"{location} Ann Arbor Michigan"
    params = {"query": location}
    address_query = f"{urlencode(params, quote_via=quote_plus)}"
    return f"{API_LINK}&{address_query}"


def main():
    try:
        response = urllib.request.urlopen(DATA_LINK)
        data = response.read().decode("utf-8")
        print("Successfully fetched data")
    except URLError as e:
        print("Error fetching data: ", e.reason)
        sys.exit(1)
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)
    else:
        building_data = seed(data)
        save(building_data)
        print("Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
