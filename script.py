from pocket import Pocket, PocketException
import time
import os.path as path
import os
import re
import unicodedata
import requests
from datetime import datetime

# Output dir
OUTDIR = "~/Desktop/pocket_links"

# Setup api
contained_path = '/'.join(__file__.split('/')[:-1])
with open(f'{contained_path}/access_token.txt') as file:
    access = file.read().strip()

with open(f'{contained_path}/consumer_key.txt') as file:
    consumer = file.read().strip()

p = Pocket(
    consumer_key=consumer,
    access_token=access
)

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


# Get response
try:
    response = p.retrieve(offset=0, count=10)
except requests.exceptions.ConnectionError:
    # print(f'GOT CONNECTION ERROR')
    quit()

l = response['list']
resTime = response['since']

container_path = os.path.expanduser(OUTDIR)
exists = path.exists(container_path)
if not exists:
    os.makedirs(container_path)

# Process response
urls = []
titles = set()
for item in l:
    url = l[item]['given_url']
    title = l[item]['resolved_title']
    word_count = l[item]['word_count']
    add_time = int(l[item]["time_added"])
    urls.append(url)

    title = f'{datetime.fromtimestamp(add_time).strftime("%m-%d")}_{slugify(title)}.txt'
    titles.add(title)
    filepath = os.path.join(container_path, title)

    with open(filepath, 'w+') as file:
        # print(f'Opened file: {filepath}')
        file.write(url)


# Remove old files
files = set(os.listdir(container_path))
not_included = files - titles

for file in not_included:
    if file.split('.')[-1] == 'txt':
        # print(f'Removing file: {file}')
        os.remove(os.path.join(container_path, file))
