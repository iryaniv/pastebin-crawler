# pastebin-crawler
Fetch all recent pastes from pastebin.com with time interval and save them to local tinydb json.

# DB Fields:
  * id : pastebin paste id
  * name : paste name
  * user : pastebin poster or empty for anonymous
  * date : UTC posting date
  * content: paste content


# Dependencies
  Python3
  Requirments:
  * requests
  * arrow
  * lxml
  * tinydb

```
usage: python main.py [-h] [-db DB] [-t TIME]

optional arguments:
  -h, --help            show this help message and exit
  -db DB                Local database path
  -t TIME, --time TIME  Scrapping interval in seconds
``` 
