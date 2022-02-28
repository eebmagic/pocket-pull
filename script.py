from pocket import Pocket, PocketException
import time
import os.path as path
import os
import re
import unicodedata

# Output dir
OUTDIR = "~/Desktop/pocket_links"

# Setup api
with open('access_token.txt') as file:
    access = file.read().strip()

with open('consumer_key.txt') as file:
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
response = p.retrieve(offset=0, count=10)
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
    urls.append(url)

    title = f'{slugify(title)}.txt'
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
        print(f'Removing file: {file}')
        os.remove(os.path.join(container_path, file))
