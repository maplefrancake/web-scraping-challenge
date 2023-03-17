from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# using splinter to visit the site
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()
    mars_dict = {}

    #1 MARS NEWS
    # set url of page to scrape and visit
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html

    # create beautifulSoup object
    soup = bs(html, 'html.parser')

    # we want the news article title and paragraph
    # title = div class list_text > div class content_title
    # paragraph = div class list_text > div class article_teaser_body
    # create list of dictionaries at the same time

    results = soup.find_all('div', class_='list_text')
    for result in results:
        title = result.find(class_='content_title').text
        paragraph = result.find(class_='article_teaser_body').text
        
        mars_dict['news_title']=title
        mars_dict['news_p']=paragraph

    #2 # JPL MARS SPACE IMAGE - FEATURED IMAGE

    url='https://spaceimages-mars.com/'
    browser.visit(url)

    # navigate to featured image using the FULL IMAGE button
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # image is kept in img class headerimage fade-in and jpg is kept in src

    image = browser.find_by_css('img[class="headerimage fade-in"]')
    featured_image_url = image['src']
    mars_dict['featured_image_url']=featured_image_url

    #3 # MARS FACTS

    url='https://galaxyfacts-mars.com/'
    browser.visit(url)

    # from the instructions, we're interested in the table containing facts
    # about the planet including Diameter, Mass, etc.
    # I'm interpretting this as the table found in the diagram about halfway
    # down the page, rather than what's in the sidebar
    # in this case, the class is 'table', and not 'table table-striped'
    marsFacts = pd.read_html(url, attrs = {'class':'table'})

    # transform list into df and clean it up
    marsDF = pd.DataFrame(marsFacts[0])
    marsClean = marsDF.transpose()
    marsClean.rename(columns=marsClean.iloc[0], inplace=True)
    marsClean.drop(marsClean.index[0], inplace=True)
    marsClean.set_index('Mars - Earth Comparison', inplace=True)

    #send df to html and create html file
    marsClean.to_html(open('marsClean.html','w'))
    mars_dict['fact_table']=marsClean.to_html()

    #4 # Mars Hemispheres

    url='https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # goal is to get each full res image
    # under div id=product-section > div class item > a href has html
    # need to click on each link and then get the full res

    hemisphere_image_urls = []

    imageLinks = soup.find_all(class_='item')
    for image in imageLinks:
        aElement = image.find('a')
        link=aElement['href']
        name = image.find('h3').text
            
        #next, we'll click on the link using the name we found
        browser.links.find_by_partial_text(name).click()
        
        #now we need new html + soup object
        imagehtml = browser.html
        imageSoup = bs(imagehtml, 'html.parser')
        
        #we can get the picture elements from downloads
        imageDownloads = imageSoup.find(class_='downloads')
        #original image will always be second in the list within the downloads class
        imageFull = imageDownloads.find_all('li')
        originalA = imageFull[1].find('a')
        imageLink = originalA['href']
        
        hemisphere_image_urls.append({'title':name,'img_url':imageLink})
        
        #save image
        browser.links.find_by_text('Original').click()
        
        browser.back()

    mars_dict['hemisphere_images']=hemisphere_image_urls

    return mars_dict

