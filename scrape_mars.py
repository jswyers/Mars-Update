from bs4 import BeautifulSoup as bs
import requests 
import time
import pandas as pd
from splinter import Browser
from flask import Flask , render_template
import pymongo





def scrape():
    
    # create mars_data dict that we can insert into mongo
    mars = {}

    browser = Browser('chrome',headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)

    html=browser.html
    soup=bs(html,'html.parser')
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
    mars['title'] = news_title
    mars['article'] = news_p

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser = Browser('chrome',headless=False)    
    browser.visit(url)
    time.sleep(2)
    html=browser.html
    browser.find_by_css("div.carousel_container div.carousel_items a.button").first.click()
    featured_image_url = browser.find_by_css("img.fancybox-image")['src']
    mars['image'] = featured_image_url

    browser = Browser('chrome',headless=False)
    url ='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(2)
    html=browser.html
    weather_soup = bs(html,'html.parser')
    mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    mars_weather = mars_weather_tweet.find('p', class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars['weather'] = mars_weather

    
    browser = Browser('chrome',headless=False)
    url = 'http://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(2)

    html=browser.html
    facts_table= pd.read_html(url)
    facts_df = facts_table[0]
    facts_df.columns=['Mars Planet Profile', 'Information']
    facts_df.set_index('Mars Planet Profile', inplace=True)
    html_table = facts_df.to_html()
    html_table = html_table.replace('\n','')
    mars['facts'] = html_table

    return mars

    