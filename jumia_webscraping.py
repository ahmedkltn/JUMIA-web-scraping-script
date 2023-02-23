#Importing libraries :
from time import sleep
from urllib import request
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sys
import lxml
#The Main function to scrape data : 
def scraper(urls):
    name = []
    price = []
    stars = []
    number_reviews = []
    category = []
    brand = []
    specific_category = []
    img = []
    old_price = []
    is_discount = []
    discount = []
    jumia_store = []
    id = []
    basic_url = "https://www.jumia.com.tn"
    for k in range(len(urls)):
      print(f'{k} / {len(urls)} Done ...',end="\r")
      for i in range(1, 51):
        try:
          url = urls[k] + "?page=" + str(i)
          try:
            response = requests.get(url)  
          except:
            sleep(5)
            continue
          soup = bs(response.content, "lxml")
          article = soup.findAll("article", attrs={"class", "c-prd"})
          for j in range(len(article)):
            core_div = article[j].find("a", attrs={"class", "core"})
            info_div = article[j].find("div", attrs={"class", "info"})
            id.append(core_div["data-id"])
            try:
              name.append(info_div.find("h3", attrs={"class", "name"}).text)
            except:
              name.append("N/A")
            try:
              price.append(info_div.find("div", attrs={"class", "prc"}).text)
            except:
              price.append("N/A")
            try:
              category.append(core_div["data-category"].split("&")[0])
            except:
              category.append("N/A")
            try:
              specific_category.append(core_div["data-category"].split("&")[1])
            except:
              specific_category.append("N/A")
            try:
              brand.append(core_div["data-brand"])
            except:
              brand.append("N/A")
            try:
              img.append(core_div.find("img")["data-src"])
            except:
              img.append("N/A")
            try:
              stars.append(info_div.find(
                  "div", attrs={"class", "stars _s"}).text)
            except:
              stars.append("N/A")
            try:
              number_reviews.append(info_div.find(
                  "div", attrs={"class", "rev"}).text.split("(")[1][:-1])
            except:
              number_reviews.append("N/A")
            try:
              old_price.append(info_div.find(
                  "div", attrs={"class", "old"}).text)
              discount.append(info_div.find(
                  "div", attrs={"class", "bdg _dsct _sm"}).text)
              is_discount.append(True)
            except:
              old_price.append("N/A")
              discount.append("N/A")
              is_discount.append(False)
            try:
              if(len(info_div.find("div", attrs={"class", "bdg _mall _xs"}).text) != 0):
                jumia_store.append(True)
            except:
              jumia_store.append(False)
        except:
            pass
    return name, price, stars, number_reviews, category, brand, specific_category, img, is_discount, old_price, jumia_store, discount, id
all_urls = []
urls = [
    "https://www.jumia.com.tn/automobile-outils/",
    "https://www.jumia.com.tn/bebe-puericulture/",
    "https://www.jumia.com.tn/jeux-et-jouets/",
    "https://www.jumia.com.tn/divers/",
    "https://www.jumia.com.tn/animalerie/",
    "https://www.jumia.com.tn/livres-papeterie/",
    "https://www.jumia.com.tn/instruments-musique/",
    "https://www.jumia.com.tn/industriel-scientifique/",
    "https://www.jumia.com.tn/deals-billetterie/"
]
website = "https://www.jumia.com.tn"
def get_cat(class_name,all_urls):
    #Getting the web site
    response = requests.get(website)
    soup = bs(response.content, "lxml")
    #Finding the menu -> cataloge
    all_subs_cat = soup.findAll("a", attrs={"class", class_name})
    #Looping over the cataloges
    for sub in all_subs_cat:
        try:
        # Getting the link of categories ex : href="jumia.com.tn/epicerie/"
            url = website + sub["href"]
        #Getting the respond and evoiding the limit of requests using sleep(5)
        except:
            break
        try:
            response = requests.get(url)
        except Exception as e:
            sleep(5)
            continue
        soup = bs(response.content, "lxml")
        #Looping over the categoris of other categories
        cats = soup.find_all("a", attrs={"class", "-db -pvs -phxl -hov-bg-gy05"})
        for cat in cats:
            new_url = website + cat["href"]
            all_urls.append(new_url)
            try:
              res = requests.get(new_url)
            except Exception as e:
              print(e)
              sleep(5)
              continue
            sub_soup = bs(res.content, "lxml")
            #Looping over the categoris of other categories
            sub_cats = sub_soup.find_all("a", attrs={"class", "-db -pvs -phxl -hov-bg-gy05"})
            for sub_cat in sub_cats:
              all_urls.append(sub_cat["href"])
def get_hidden_cat(urls, all_urls):
  for url in urls:
    try:
        response = requests.get(url)
    except:
        sleep(5)
        continue
    soup = bs(response.content, "lxml")
    #Looping over the categoris of other categories
    cats = soup.find_all("a", attrs={"class", "-db -pvs -phxl -hov-bg-gy05"})
    for cat in cats:
          new_url = website + cat["href"]
          try:
            res = requests.get(new_url)
            all_urls.append(new_url)
          except Exception as e:
              print(e)
              sleep(5)
              continue
          sub_soup = bs(res.content, "lxml")
            #Looping over the categoris of other categories :
          sub_cats = sub_soup.find_all("a", attrs={"class", "-db -pvs -phxl -hov-bg-gy05"})
          for sub_cat in sub_cats:
              all_urls.append(sub_cat["href"])
#Getting the cataloge of class='itm'
get_cat("itm",all_urls)
get_hidden_cat(urls,all_urls)
print(all_urls)
name,price,stars,number_reviews,category,brand,specific_category,img,is_discount,old_price,jumia_store,discount,id = scraper(all_urls)
i = range(1,len(name)+1)
df = pd.DataFrame({
                   "product_id":id,
                   "product_name":name,
                   "price_TND":price,
                   "seller_rating":stars,
                   "number_reviews":number_reviews,
                   "category":category,
                   "brand":brand,
                   "specific_category":specific_category,
                   "img":img,
                   "discount":discount,
                   "is_discount":is_discount,
                   "old_price_TND":old_price,
                   "jumia_store":jumia_store
                  },index=i)
df.to_csv("jumia_listing.csv")
