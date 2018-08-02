from selenium import webdriver


# use google chrome incognito mode for scraping
option = webdriver.ChromeOptions()
option.add_argument(" - incognito")

# launch browser
browser = webdriver.Chrome(executable_path='/Library/Application Support/Google/chromedriver', chrome_options=option)
browser.implicitly_wait(5)

# launch url
browser.get("http://snu.fbpage.kr/#/search")

posts_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[1]/a[1]")
posts_button.click()

# xpath for next page button //*[@id="mainContainer"]/div/div[5]/center/ul/li[6]/a

# create list to store post elements
post_list = list()


# scrape for posts within page
# the 4th div is the one that needs iteration
def scrape_for_posts():
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


scrape_for_posts()

next_page_button = browser.find_element_by_xpath("//*[@id='mainContainer']/div/div[5]/center/ul/li[6]/a")
next_page_button.click()


print(post_list)

browser.close()



