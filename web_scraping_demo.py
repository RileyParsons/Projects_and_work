# beautifulsoup is an html parser
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import re 
# Some soup reference
# https://scrapeops.io/python-web-scraping-playbook/python-beautifulsoup-findall/#findall-by-text
# 
url = "https://shakespeare.mit.edu/romeo_juliet/full.html"

page = urlopen(url)
# test to see if url is accessed
print(page)
# expected: <http.client.HTTPResponse object at 0x0000022E9B6D76D0>

# extract html from webpage
html_data = page.read()

# read returns a sequence of bytes. this needs to be decoded to readable text. utf-8 
html_code = html_data.decode("utf-8")

# print html code to screen to test if read correctly
#print(html_code)

# save to txt file in current directory (in case i get blacklisted from website). Also overwrite
with open("raw_html.txt", "w") as file:
    file.write(html_code)

soup = BeautifulSoup(html_code, "html.parser")

#print(soup.get_text())
txt = soup.get_text()
# convert all text to lowercase for ease of use
lower_case_text = txt.lower()

#print(lower_case_text)

# set up the target words and their associated values
words = ["love", "marry", "wife", "husband", "death", "dead", "die" , "kill"]
word_weighting =[0.01, 0.001, 0.001, 0.001, -0.01, -0.01, -0.001, -0.001]
counts = []
# finding the count for each word as case insensitive
# this prints out the lines that contain the word
# find = soup.find_all(string=re.compile("love", re.IGNORECASE))
# print(find)
#search through text to get total count

def get_count(word):
    num = lower_case_text.count(word)
    counts.append(num)

for w in words:
    get_count(w)

print(counts)

# create initial dataframe state
data_frame_base = {"key_word": words, "multiplier": word_weighting, "count": counts}
# create pandas data frame for results
df = pd.DataFrame(data = data_frame_base)

# add the total count
df["weighted_count"] = df["multiplier"] * df["count"]

# test dataframe
print(df)
df.to_csv("word_weights.cvs")

#get the combined weighting of all words
total_count = df["weighted_count"].sum()
# set up base number for adjusting prediction based on good and bad key words
base_multiplier = 1.0

# get predictor modifier based on words mentioned
prediction_multiplier = base_multiplier + total_count

# this can now be used to adjust the predicted value
print(f"prediction multiplier: {prediction_multiplier}")
