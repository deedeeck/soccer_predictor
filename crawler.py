# This file crawls websites for soccer odds

import argparse
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def set_chrome_options(headless_mode=False):
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=" + user_agent)
    options.add_argument("--profile-directory=Default")

    if headless_mode:
        options.add_argument("headless")

    return options

def crawl_individual_page(driver,page_link):

    driver.get(page_link)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--remote', action='store_true', help="Set crawler to use remote selenium standalone server")
    parser.add_argument('-s', '--session', help="Set session id for remote session")

    args = parser.parse_args()
    remote_mode = args.remote
    session_id = args.session

    if remote_mode : 
        remote_url = "http://127.0.0.1:4444/wd/hub"
        driver = webdriver.Remote(
            command_executor=remote_url,
            desired_capabilities=set_chrome_options().to_capabilities(),
        )

        if session_id :
            driver.quit() # quit the new session that has just opened
            driver.session_id = session_id # attach to existing session
        else:
            print("Session id of remote server is :", driver.session_id)
            quit()
    else:
        driver_path = "./chromedriver"
        driver = webdriver.Chrome(driver_path, options=set_chrome_options())

    web_url = "https://online.singaporepools.com/en/sports/competition/36/football/england/english-premier"

    if driver.current_url != web_url:
        driver.get(web_url)

    # sg pools sometimes alert that I am not using the correct version of a browser
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        print("no alert to accept")

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException

    delay = 5 

    # wait for page to load finish
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table-condensed"]')))
    except TimeoutException:
        print("page took too long to load")

    matches_link = [link.get_attribute("href") for link in driver.find_elements_by_xpath('//span[@class="event-list__event-name"]/a')]
        
    for link in matches_link:
        crawl_individual_page(driver,link)
        break

    # matches_list = driver.find_elements_by_xpath('//table[@class="table-condensed"]/tbody/tr')
    # for match in matches_list:
    #     match.find_element_by_xpath('//td/span[@class="event-list__event-name"]')


# old code
# selected_div = driver.find_element_by_xpath('//div[@class="event-list"]')

# get listed matches
# bet_type_selector = selected_div.find_element_by_xpath('//select[@name="upcomingFootball_filterBetType"]')
# bet_type_selection = selected_div.find_element_by_xpath("//option[@value='HL']")
# bet_type_selection.click()
# display_button = selected_div.find_element_by_xpath('//button[./span = "Display"]')
# display_button.click()

# match_odds = []
# get individual matches data
# matches_rows = selected_div.find_elements_by_xpath('//div[@class="event-list__event"]')

# for match in matches_rows:

#     try:
#         match_title = match.find_element_by_xpath(
#             './/span[@class="event-list__event-name"]/a'
#         ).text.strip()
#         print(match_title)
#         outcomes = match.find_elements_by_xpath(
#             './/div[@class="event-market__outcome-row"]/div[contains(@class,"outcome")]'
#         )

#         temp_dict = {"match_title": match_title}

#         for outcome in outcomes:
#             outcome_text = outcome.find_element_by_xpath(
#                 './/span[@class="button-outcome__text"]/span'
#             ).text.strip()
#             outcome_price = outcome.find_element_by_xpath(
#                 './/span[@class="button-outcome__price"]'
#             ).text.strip()

#             if "Over" in outcome_text:
#                 temp_dict["over"] = {"Market": outcome_text, "odds": outcome_price}
#             elif "Under" in outcome_text:
#                 temp_dict["under"] = {"Market": outcome_text, "odds": outcome_price}

#         match_odds.append(temp_dict)

#     except NoSuchElementException:
#         print('in exception')
#         continue

# print(match_odds)

