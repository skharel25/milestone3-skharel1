import requests
import pdb


def wikifinder(String):
    BASE_URL= "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch="

    Title=String

    url=BASE_URL+Title+"&format=json"
 


    response = requests.get(url)

    response_json = response.json()

    pageid=""

    try:
        print(((response_json["query"]["searchinfo"]["totalhits"])))
        print(((response_json["query"]["search"][0]["pageid"])))

        pageid=((response_json["query"]["search"][0]["pageid"]))
            
    except KeyError:
        return("Couldn't fetch this data!")

    return pageid







