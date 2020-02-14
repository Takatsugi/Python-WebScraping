from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import time
import pymongo
from pymongo import MongoClient

#Database connection
cluster = MongoClient("mongodb+srv://hatem:hatem@cluster0-ah2bd.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["news"]

def scrapeDailyKos():
    list_links = []
    base_url = 'https://www.dailykos.com/blogs/main'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")
    articles = soup.find_all(class_='story-title heading')
    for n in np.arange(0, len(articles)):
        link = articles[n].find('a')['href']
        list_links.append("https://www.dailykos.com"+link)
    return list_links

def scrapeDailyKosInside():
    nb = scrapeDailyKos()
    number_of_articles = len(scrapeDailyKos())
    contenuTxt = ""
    for x in np.arange(0, number_of_articles):
        base_url = nb[x]
        r = requests.get(base_url)
        soup = BeautifulSoup(r.text, "html.parser")
        container = soup.find(class_='story-wrapper')
        titleContainer = container.find(class_='story-title heading')
        title = titleContainer.find('a').get_text()
        auteurContainer = container.find(class_='author-name')
        auteur = auteurContainer.find('a').get_text()
        date = container.find(class_='author-date hidden-sm').get_text()
        dateRefined = date.split("\n",2)
        contenu = container.find_all('p')
        for x in contenu:
            contenuTxt += x.get_text()
        scraped_dict = {'auteur':auteur,'title':title,'contenu':contenuTxt,'date':dateRefined[1]}
        contenuTxt = ""
        collection.insert_one(scraped_dict)
    return "ok"

def scrape():
    list_links = []
    bu = 'https://www.oann.com/category/newsroom'
    r1 = requests.get(bu)
    soup1 = BeautifulSoup(r1.text, "html.parser")
    pages = soup1.find(class_='pagination clearfix')
    #find number of pages to scrape
    page_nb = pages.find_all(class_='page-numbers')
    for nbp in range(0, int(page_nb[-2].get_text())):
        if nbp==0:
            base_url = 'https://www.oann.com/category/newsroom'
        else:
            base_url = 'https://www.oann.com/category/newsroom/page/'+str(nbp) 
       
        r = requests.get(base_url)
        soup = BeautifulSoup(r.text, "html.parser")

        main_containt = soup.find(class_='mh-loop')
        coverpage_news = main_containt.find_all('article')
        for n in np.arange(0, len(coverpage_news)):
            link = coverpage_news[n].find('a')['href']
            list_links.append(link)

    return list_links
          
def scrape_inside():
    nb=scrape()
    number_of_articles = len(scrape())
    contenuTxt = ""
    for x in np.arange(0, number_of_articles):
        base_url = nb[x]
        r = requests.get(base_url)
        soup = BeautifulSoup(r.text, "html.parser")
        container = soup.find('article')
        title = container.find('h1', class_='entry-title')
        auteurH5 = container.find_all('h5')
        for h in auteurH5:
            if "UPDATED" in h.get_text():
                auteur = h.get_text()
        #auteur = container.find('h5')
        container2 = soup.find(class_='entry-content clearfix')
        contenu = container2.find_all('p')
        for x in contenu:
            contenuTxt += x.get_text()
        aut = auteur.split("\n",1)
        date = auteur.split("\u2014",1)
        if aut[0] == "":
            scraped_dict = {'auteur':"",'title':title.text,'contenu':contenuTxt,'date':""}
        else:
            scraped_dict = {'auteur':aut[0],'title':title.text,'contenu':contenuTxt,'date':date[1]}
        contenuTxt = ""
        collection.insert_one(scraped_dict)
        #scraped_ordered_list.append(scraped_dict)

    return "ok"

def scrapeEverything():
    scrapeDailyKosInside()
    scrape_inside()

if __name__ == "__main__":
    print(scrape_inside())