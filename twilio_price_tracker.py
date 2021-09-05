from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver

import re # to use regular expressions in the project
# I solved these kinds of problems using the webdrive manager.

# You can automatically use the correct chromedriver by using the webdrive-manager. Install the webdrive-manager:


def get_url(search_text):
    """Generate a url from search text"""
    url = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'.format(search_text)
    
    # add page query
    url += '&page{}'
        
    return url


def extract_record(single_record):
    """Extract and return data from a single record"""

    
    # Title
    title_tag = single_record.h2.a
    title = title_tag.text.strip()
    url = 'https://www.amazon.com' + title_tag.get('href')
    
    # because some products dont have prices we have to 
    # use try-except block to catch AttributeError
    try:
        # product price
        price_parent = single_record.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    result = (title, price)
    
    return result

def main(search_term):


    """Run main program routine"""
    
    # startup the webdriver
    options=Options()
    
    options.headless = False #choose if we want the web browser to be open when doing the crawling 
    # options.use_chromium = True
    driver = webdriver.Chrome('/home/muhammed/Desktop/dev/blog-repo/twilioXseleniumXpython/chromedriver')

    records = []
    url = get_url(search_term)
    
    for page in range(1, 5):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
                print(record)
    driver.close()
  

# # Retieve data
# all_sneakers = client.query(
#    q.paginate(
#        q.match(q.index("Allsneakers"))  #add the name of the index you created
#    ) 
# )

# all_sneakers_list = [all_sneakers["data"]]
# result = re.findall("\d+", str(all_sneakers_list)) #find all the number in the JSON, that will be the ids 

# for i in range(0, len(result)):
#     sneaker_details = client.query(q.get(q.ref(q.collection("shoes"), result[i])))
#     details_list = [sneaker_details["data"]]
#     print(details_list)


main("sneakers")