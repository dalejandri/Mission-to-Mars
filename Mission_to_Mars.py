# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
#Search for elements with a specific combination of tag (div) 
#and attribute (list_text). As an example, ul.item_list would be found in HTML 
#as <ul class="item_list">
browser.is_element_present_by_css('div.list_text', wait_time=1)

#set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ## Mars Facts
#Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table 
#with Pandas' .read_html() function.

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

#The Pandas function read_html() specifically searches for and returns a list of tables 
#found in the HTML. By specifying an index of 0, we're telling Pandas 
#to pull only the first table it encounters, or the first item in the list. 
#Then, it turns the table into a DataFrame.
#Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function
df.to_html()

# end the automated browsing session
browser.quit()