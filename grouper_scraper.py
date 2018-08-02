from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv


# use google chrome incognito mode for scraping
option = webdriver.ChromeOptions()
option.add_argument(" - incognito")

# launch browser
browser = webdriver.Chrome(executable_path='/Library/Application Support/Google/chromedriver', chrome_options=option)
browser.implicitly_wait(3)

# launch url and desired web view
browser.get("http://snu.fbpage.kr/#/search")

posts_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[1]/a[1]")
posts_button.click()

# create timeout period
timeout = 10

# create list to store post elements
post_list = list()
num = 0


# scrape for posts within page
# the 4th div is the one that needs iteration
def scrape_for_posts(adder):
    try:
        loaded = EC.text_to_be_present_in_element((By.XPATH, "//*[@id='mainContainer']/div/div[5]/div[5]"), "년")
        WebDriverWait(browser, timeout).until(loaded)
    except TimeoutException:
        print("Timed out")
        browser.quit()

    post_element = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/div[1]/div/ul/li[1]/p")
    post = post_element.text
    post_list.append(post)

    post_element = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/div[2]/div/ul/li[1]/p")
    post = post_element.text
    post_list.append(post)

    post_element = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/div[3]/div/ul/li[1]/p")
    post = post_element.text
    post_list.append(post)

    post_element = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/div[4]/div/ul/li[1]/p")
    post = post_element.text
    post_list.append(post)

    post_element = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/div[5]/div/ul/li[1]/p")
    post = post_element.text
    post_list.append(post)

    adder += 5
    return adder


num = scrape_for_posts(num)

# button settings for initial page
second_page_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/center/ul/li[2]/a")
second_page_button.click()
num = scrape_for_posts(num)

third_page_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/center/ul/li[3]/a")
third_page_button.click()
num = scrape_for_posts(num)

fourth_page_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/center/ul/li[4]/a")
fourth_page_button.click()
num = scrape_for_posts(num)

fifth_page_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/center/ul/li[5]/a")
fifth_page_button.click()
num = scrape_for_posts(num)

next_page_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/center/ul/li[6]/a")
next_page_button.click()

print(num)

# button settings for pages after that
second_page_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/center/ul/li[3]/a")
third_page_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/center/ul/li[4]/a")
fourth_page_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/center/ul/li[5]/a")
fifth_page_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/center/ul/li[6]/a")
next_page_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/center/ul/li[7]/a")

"""while next_page_button:
    scrape_for_posts()
    second_page_button.click()
    scrape_for_posts()
    third_page_button.click()
    scrape_for_posts()
    fourth_page_button.click()
    scrape_for_posts()
    fifth_page_button.click()
    scrape_for_posts()
    next_page_button.click()
    """


# create csv from list
def write_csv(post_list, num):
    with open('posts data.csv', 'wt', encoding='utf-8') as file:
        w = csv.writer(file)
        w.writerow(['post_text', 'post_likes', 'post_comments', 'post_shares'])
        for i in range(num):
            w.writerow([post_list[i]])


# write_csv(post_list, num)
