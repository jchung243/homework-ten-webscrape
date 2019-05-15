# Dependancies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

# Define function
def scrape():
    # Create dictionary to return
    return_dict = {}

    # Create initial browser object
    executable_path = {'executable_path': '/Users/joshchung/Bootcamp/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Scrape NASA Mars news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')
    results = soup.find('li', class_="slide")
    article_date = results.find('div', class_="list_date").text
    article_title = results.find('div', class_="content_title").text
    article_teaser = results.find('div', class_="article_teaser_body").text
    return_dict.update({'article_date':article_date,
                        'article_title':article_title,
                        'article_teaser':article_teaser})

    # Scrape JPL image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')
    results = soup.find_all('article', class_="carousel_item")
    url_string = results[0].get('style')
    url_string = url_string.split("url('")
    url_string = url_string[1].split("');")
    url_string = url_string[0]
    img_url = 'https://www.jpl.nasa.gov' + url_string
    return_dict.update({'img_url':img_url})

    # Scrape Twitter
    url = 'https://twitter.com/marswxreport'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')
    last_tweet = soup.find('p', class_="tweet-text").text
    last_tweet = last_tweet.replace('\n', ' ')
    return_dict.update({'last_tweet':last_tweet})

    # Scrape Mars facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_table = mars_df.to_html()
    mars_table = mars_table.replace('\n', '')
    return_dict.update({'mars_table':mars_table})

    # Scrape Mars hemisphere images
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mars_urls = {}
    for x in range(0,4):
        browser.visit(url)
        links = browser.find_by_tag('h3')
        links[x].click()
        html = browser.html
        soup = bs(html, 'lxml')
        downloads = soup.find('div', class_="downloads")
        dl_links = downloads.find_all('a')
        img_link = dl_links[0].get('href')
        title = soup.find('h2', class_="title").text
        mars_urls.update({f"marsimg_{x}" : img_link})
        browser.back()
    return_dict.update(mars_urls)

    # Return dictionary when function is run
    return return_dict