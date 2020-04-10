import requests
from bs4 import BeautifulSoup
import pymongo

months = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06",
          "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["calendar_events"]
collection = db["cis"]

page = requests.get("https://cs.uoregon.edu/public_talks")
soup = BeautifulSoup(page.content, "html.parser")

eventsTables = soup.select("div.view-public-talks table.views-table")

for eventsTable in eventsTables:
    month, year = str(eventsTable.caption.text).split()

    events = eventsTable.select("tr")
    for event in events:
        dayOfMonth = str(event.span.text)
        eventDesc = str(event.select("td")[1].a.text)
        presenterName = str(event.select("td")[1].p.strong.text)
        eventCategory = str(event.select("td")[2].text).strip()

        detailsUrl = str(event.select("td")[1].a["href"])
        detailsPage = requests.get("https://cs.uoregon.edu" + detailsUrl)
        detailsSoup = BeautifulSoup(detailsPage.content, "html.parser")
        time = str(detailsSoup.select(
            "div.field-name-field-date-and-time")[0].span.text).split()[-1]

        eventTitle = "{0}, {1}, {2}".format(
            eventDesc, presenterName, eventCategory)
        eventDatestring = "{0}-{1}-{2}T{3}:00".format(
            year, months[month], dayOfMonth, time)
        eventDict = {"title": eventTitle,
                     "category": "time", "start": eventDatestring}
        collection.insert_one(eventDict)
