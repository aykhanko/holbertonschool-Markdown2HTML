#!/usr/bin/python3 

import sys
import os

with open("README.md", "r") as f:
    markdown_text_list = f.readlines()

def markdown_html(text):
    symbol = "#"
    count = text.count(symbol)
    raw_text = text[count+1:].strip()
    html_text = f"<h{count}>{raw_text}</h{count}>\n"

    with open ("README.html", "a", encoding = "UTF-8") as f:
        f.write(html_text)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    if not os.path.isfile("README.md"):
        sys.stderr.write("Missing README.md\n")
        sys.exit(1)

    for text in markdown_text_list:
        markdown_html(text)


    sys.exit(0)


