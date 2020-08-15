import requests
import argparse
import time
import json
import random
import pandas as pd
import os
import xml.etree.ElementTree as xml
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup

internal_links = set()
external_links = set()
urls = []
total_links_visited = 0

#check if url is valid
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

#this function finds and prints out the internal and external links
def get_all_website_links(url):
    global urls
    domain_name = urlparse(url).netloc
    res1 = requests.get(url)
    soup = BeautifulSoup(res1.content, "html.parser")
    for a_tag in soup.findAll("a"):
        href_tag = a_tag.attrs.get("href")
        if href_tag:
            href_tag = urljoin(url, href_tag)
            parsed_href = urlparse(href_tag)
            href_tag = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if is_valid(href_tag):
                if domain_name not in urlparse(href_tag).netloc and href_tag not in external_links:
                    print(f"External link: {href_tag}")
                    external_links.add(href_tag)
                    continue
                elif href_tag not in urls:
                    print(f"Internal link: {href_tag}")
                    urls.append(href_tag)
                    internal_links.add(href_tag)

    #this function crawls a web page and extracts all links
def crawl(url, max_urls=50):
    global total_links_visited, urls
    total_links_visited += 1
    get_all_website_links(url)
    for link in urls:
        if total_links_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

def save(output_file_format, domain_name, internal_links, external_links):
    if (output_file_format == "json"):
        #writing to json files
        f = open(f"{domain_name}_internal_links.json","w")
        json.dump({'internal_links':list(internal_links)}, f, indent=6)
        f.close()
        f = open(f"{domain_name}_external_links.json","w")
        json.dump({'external_links':list(external_links)}, f, indent=6)
        f.close()

    elif (output_file_format == "csv"):
        #writing to csv
        df = pd.DataFrame(list(internal_links))
        df.to_csv(f"{domain_name}_internal_links.csv", index=False, header=False)
        df = pd.DataFrame(list(external_links))
        df.to_csv(f"{domain_name}_external_links.csv", index=False, header=False)

    elif (output_file_format == "xml"):
        #writing to xml
        xmlformat = xml.Element("internal_links")
        xmlformat_1 = xml.SubElement(xmlformat, "link")
        for l in list(internal_links):
            xmlformat_1.text = str(l)
            xmlformat.append(xmlformat_1)
        tree = xml.ElementTree(xmlformat)
        tree.write(f"{domain_name}_internal_links.xml")

        xmlformat = xml.Element("external_links")
        xmlformat_1 = xml.SubElement(xmlformat, "link")
        for l in list(external_links):
            xmlformat_1.text = str(l)
            xmlformat.append(xmlformat_1)
        tree = xml.ElementTree(xmlformat)
        tree.write(f"{domain_name}_external_links.xml")
      
    elif (output_file_format == "ALL"):
        with open(f"{domain_name}_internal_links.txt", "w") as f:
            for internal_link in internal_links:
                print(internal_link.strip(), file=f)
        with open(f"{domain_name}_external_links.txt", "w") as f:
            for external_link in external_links:
                print(external_link.strip(), file=f)
        
        #writing to json files
        f = open(f"{domain_name}_internal_links.json","w")
        json.dump({'internal_links':list(internal_links)}, f, indent=6)
        f.close()
        f = open(f"{domain_name}_external_links.json","w")
        json.dump({'external_links':list(external_links)}, f, indent=6)
        f.close()
        
        #writing to csv
        df = pd.DataFrame(list(internal_links))
        df.to_csv(f"{domain_name}_internal_links.csv", index=False, header=False)
        df = pd.DataFrame(list(external_links))
        df.to_csv(f"{domain_name}_external_links.csv", index=False, header=False)
        
        #writing to xml
        xmlformat = xml.Element("internal_links")
        xmlformat_1 = xml.SubElement(xmlformat, "link")
        for l in list(internal_links):
            xmlformat_1.text = str(l)
            xmlformat.append(xmlformat_1)
        tree = xml.ElementTree(xmlformat)
        tree.write(f"{domain_name}_internal_links.xml")

        xmlformat = xml.Element("external_links")
        xmlformat_1 = xml.SubElement(xmlformat, "link")
        for l in list(external_links):
            xmlformat_1.text = str(l)
            xmlformat.append(xmlformat_1)
        tree = xml.ElementTree(xmlformat)
        tree.write(f"{domain_name}_external_links.xml")
                
    else:
        with open(f"{domain_name}_internal_links.txt", "w") as f:
            for internal_link in internal_links:
                print(internal_link.strip(), file=f)
        with open(f"{domain_name}_external_links.txt", "w") as f:
            for external_link in external_links:
                print(external_link.strip(), file=f)

#main function
def main():
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)
    parser.add_argument("-t", "--output-file-format", help="Output file format to store the data. Write ALL to get all file formats Default text", default="txt")
    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls
    output_file_format = args.output_file_format
    domain_name = urlparse(url).netloc
    res = requests.get(url)
    statuscode = res.status_code
    print("Status Code:", statuscode)
    if statuscode == 200:
        crawl(url, max_urls=max_urls)
        print("Total Internal Links:", len(internal_links))
        print("Total External Links:", len(external_links))
        print("Total Links:", len(external_links) + len(internal_links))
        save(output_file_format, domain_name, internal_links, external_links)
    else:
        print("Failed to get a request response back.")
        
#executing the python script
if __name__ == "__main__":
    main()