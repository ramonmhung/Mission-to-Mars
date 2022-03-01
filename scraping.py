# Import splinter BeautifulSoup

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import pandas as pd

def scrape_all():


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    
    news_title, news_paragraph = mars_news(browser)
    #hemisphere_image_urls = hemisphere(browser)
    df = mars_facts()
    
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        #"hemispheres": hemisphere_image_urls,
        "facts": df,
        "last_modified": dt.datetime.now(),
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # visit the mars nasa news site

    url = 'http://redplanetscience.com/'
    browser.visit(url)

    #optional delay for loading the page

    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # now lets set up the HTML parser

    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    # Add try/except for error handling
    try:
        # let's start scraping

        slide_elem.find('div', class_='content_title')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        


        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p


# ### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()



    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

### MARS FACTS

def mars_facts():
    
    # Add try/except for error handling
   
    try:
        
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    
    # Assign columns and set index of dataframe
    
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    

    # Convert dataframe into HTML format, add bootstrap
    
    return df.to_html(classes="table table-striped")

def hemisphere(browser):
    url = 'https://marshemispheres.com'

    browser.visit(url)


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        hemispheres = {}

        # Get through all the loops to find the elements
        browser.find_by_css('a.product-item h3')[i].click()

        # extract the source 'href'
        element = browser.links.find_by_text('Sample').first
        img_url = element['href']
        
        
        #hemisphere["img_url"] = sample_img["href"]

        # get hemisphere title
        title = browser.find_by_css("h2.title").text
    
         # get image url
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title


        # Let's append the hemisphere objects our predetrmined list of dictionaries
        hemisphere_image_urls.append(hemispheres)
        
        browser.back()
                   
   
                   
    # 4. Print the list that holds the dictionary of each image url and title.
    hemisphere_image_urls

    # 5. Quit the browser
    browser.quit()


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())