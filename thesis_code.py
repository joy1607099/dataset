from twarc import Twarc
import preprocessor as p
import io
import csv
ACCESS_TOKEN = "2668727876-Yrz4VAyuedncEMFsFRQhy5G8b6ZKbcB9x2G58BU"
ACCESS_TOKEN_SECRET = "LEXRPAoFSKE7oBaqrrZRUBnIbgdoWbZhS5vG2zM2s7Y6j"
CONSUMER_KEY = "l79fswnkaCLeUjXeZzPir9iQU"
CONSUMER_SECRET = "6s1h36BhY9Ypdu7pxDWWSyT2u6mYpex8EUXwKJaewDAtxhsGVq"
t = Twarc(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
p.set_options(p.OPT.URL, p.OPT.EMOJI,p.OPT.MENTION,p.OPT.SMILEY)


with open('April1.tsv', 'r') as fin, open('April1_out.tsv', 'w') as fout:
    
    reader = csv.reader(fin, dialect='excel-tab')
    writer = csv.writer(fout, dialect='excel-tab')
    for row in reader:
         # delete indices in reverse order to avoid shifting earlier indices
        del row[1:]
        writer.writerow(row)
# t hydrate March1_out.tsv > March1.jsonl

with open('April1.csv', mode='w', encoding="utf-8") as corona_file:
    fieldnames = ['date', 'text', 'truncated']
    writer = csv.DictWriter(corona_file, fieldnames=fieldnames)
    writer.writeheader()
    for tweet in t.hydrate(open('April1_out.tsv')):
        p.clean(tweet["full_text"])
        writer.writerow(
            {'date': tweet["created_at"], 'text': tweet["full_text"], 'truncated': tweet["truncated"]})
