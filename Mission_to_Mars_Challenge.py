#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
#Search for elements with a specific combination of tag (div) 
#and attribute (list_text). As an example, ul.item_list would be found in HTML 
#as <ul class="item_list">
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[6]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[7]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[8]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[9]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[10]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[11]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[12]:


#Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table 
#with Pandas' .read_html() function.

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

#The Pandas function read_html() specifically searches for and returns a list of tables 
#found in the HTML. By specifying an index of 0, we're telling Pandas 
#to pull only the first table it encounters, or the first item in the list. 
#Then, it turns the table into a DataFrame.


# In[13]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[14]:


#Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)


# In[16]:


html = browser.html
hemi_soup = soup(html, 'html.parser')


# In[17]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
hemi_titles = []
hemi_dict = {}


# In[18]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.
main_url = hemi_soup.find_all('div', class_='item')

for detail in main_url:
    title = detail.find('h3').text
    mars_url = detail.find('a')['href']
    hemi_url = f'https://astrogeology.usgs.gov/{mars_url}'
#hemi_url
    browser.visit(hemi_url)
    html = browser.html
    mars_soup = soup(html, 'html.parser')
    original_img = mars_soup.find('div',class_='downloads')
    hemi_img_url = original_img.find('a')['href']
    
    print(hemi_img_url)
    img_data = dict({'img_url':hemi_img_url, 'title':title})
    hemisphere_image_urls.append(img_data)
    
    browser.back()


# In[19]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[20]:


# 5. Quit the browser
browser.quit()


# In[ ]:




