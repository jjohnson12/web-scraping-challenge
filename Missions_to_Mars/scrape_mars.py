##Jason Johnson was here.

# Dependencies

import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

# NASA Mars News Site scrape
def scrape():
    mars = {}
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    if browser.is_element_present_by_css('div.content_title', wait_time=3):
        #First look for all of the html
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        #what we are looking for is in a div, nested deep in a title
        results = soup.find_all('div', class_='content_title')

        #We do .text becasue we are pulling out the html text deep listed
        news_title = results[1].text

        #This will return a list for the article teaser body, which comes from the html code
        results = soup.find_all('div', class_='article_teaser_body')

        #This does not have a nested anchor so we will do results 0 here
        news_paragraph = results[0].text

        mars.update({"Latest Mars News Title":news_title, "Latest Mars News":news_paragraph})
    
    ##JPL Mars Space Image - Featured Image
    
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser = init_browser() 
    browser.visit(url)

    time.sleep(5)
    results = browser.find_by_id('full_image')
    img = results[0]
    img.click()

    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = soup.find("img", class_="fancybox-image")["src"]

    base_url = 'https://www.jpl.nasa.gov'
    full_featured_image_url = (f'{base_url}{featured_image_url}')

    mars.update({"JPL Mars Space Image":full_featured_image_url})

    
    # Mars Weather
    
    url = "https://twitter.com/marswxreport?lang=en"
    browser = init_browser() 
    browser.visit(url)

    xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div[1]/div/div/div/article/div/div[2]/div[2]/div[2]/div[1]/div/span'
        #We found xpath from twitter, navigating to the first tweet, right click and copy full xpath
        #this activates silenium, with a wait time of 10 seconds to let the page load
        #This is the line that checks to exist it's real
    if browser.is_element_present_by_xpath(xpath, wait_time=3):
        #Select the html element we copied above
        first_tweet = browser.find_by_xpath(xpath)
        #this is the html of the first tweet
        html = first_tweet.html
        #Pass just the html we want to Beautiful Soup to return the result
        soup = BeautifulSoup(html, 'html.parser')
        mars_weather = (soup.prettify())
        mars.update({"Latest Mars Weather":mars_weather})
    
    
    # Mars Facts

    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    mars_facts = pd.read_html(soup.prettify())[0]
    mars_html = mars_facts.to_html(index=False, header=False)
    mars.update({"Mars Fun Facts":mars_html})

# Mars Hemispheres

    browser = init_browser() 
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    #From home page to Cereberus
    time.sleep(2)
    results = browser.find_by_text('Cerberus Hemisphere Enhanced')
    img = results[0]
    img.click()
    #Get link for Cereberus
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    cerebrus_base = soup.find('a', string='Original').get('href')
    cerberus_hemisphere_img = (f'{cerebrus_base}/full.jpg')
    cerberus_hemisphere_title = soup.find('h2', class_='title').text
    cerberus={"title":cerberus_hemisphere_title, "image_url":cerberus_hemisphere_img}


    # Back to main page
    browser.back()

    #From home page to Schiaparelli
    time.sleep(2)
    results = browser.find_by_text('Schiaparelli Hemisphere Enhanced')
    img = results[0]
    img.click()
    #Get link for Schiaparelli
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    schiaparelli_base= soup.find('a', string='Original').get('href')
    schiaparelli_hemisphere_img = (f'{schiaparelli_base}/full.jpg')
    schiaparelli_hemisphere_title = soup.find('h2', class_='title').text
    schiaparelli={"title":schiaparelli_hemisphere_title, "image_url":schiaparelli_hemisphere_img}

    # Back to main page
    browser.back()

    #From home page to Syrtis Major
    time.sleep(2)
    results = browser.find_by_text('Syrtis Major Hemisphere Enhanced')
    img = results[0]
    img.click()
    #Get link for Syrtis Major
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    syrtis_base = soup.find('a', string='Original').get('href')
    syrtis_hemisphere_img = (f'{syrtis_base}/full.jpg')
    syrtis_hemisphere_title = soup.find('h2', class_='title').text
    syrtis={"title":syrtis_hemisphere_title, "image_url":syrtis_hemisphere_img}


    # Back to main page
    browser.back()

    #From home page to Valles Marineris
    time.sleep(2)
    results = browser.find_by_text('Valles Marineris Hemisphere Enhanced')
    img = results[0]
    img.click()
    #Get link for Valles Marineris
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    valles_base = soup.find('a', string='Original').get('href')
    valles_hemisphere_img = (f'{valles_base}/full.jpg')
    valles_hemisphere_title = soup.find('h2', class_='title').text
    valles={"title":valles_hemisphere_title, "image_url":valles_hemisphere_img}
    
    hemisphere_image_urls=[cerberus, schiaparelli, syrtis, valles]
    mars.update({"Mars Hemispheres":hemisphere_image_urls})
    return mars

if __name__ == "__main__":
    print(scrape())
