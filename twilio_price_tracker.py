from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from twilio.rest import Client
 

# I solved these kinds of problems using the webdrive manager.

# You can automatically use the correct chromedriver by using the webdrive-manager. Install the webdrive-manager:
account_sid = "AC93642d372e8e6635f97a1f70e9010b77"
auth_token = "f4ff9d1387e26c23635ec222ff249732"

client = Client(account_sid, auth_token)

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

def main(search_term, max_price):


    """Run main program routine"""
    
    # startup the webdriver
    options=Options()
    
    options.headless = True #choose if we want the web browser to be open when doing the crawling 
    # options.use_chromium = True
    driver = webdriver.Chrome('/home/muhammed/Desktop/dev/blog-repo/twilioXseleniumXpython/chromedriver',options=options)

    records = []
    prices_list=[]
    url = get_url(search_term)
    
    for page in range(1, 3):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    for titles, prices in records:
        prices_list.append(prices)


    new_prices= [s.replace("$", "").replace(',',"") for s in prices_list]
    print(new_prices)
    new=[]
    prices_float = [float(i) for i in new_prices]
    for i in prices_float:
        
        if i < max_price:
            new.append(i)
    # print(new)
    client.messages.create(
        # to send SMS to mobile phone
        to="+2348112398610",
        from_="+14692840596",
        body=f"There are {len(new)} rolex watchs less than than amount"
    )
       

main("rolex", 10000)
