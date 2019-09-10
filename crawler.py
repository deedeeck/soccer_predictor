# This file crawls websites for soccer odds

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
DRIVER_PATH = "./chromedriver"
options = webdriver.ChromeOptions()
# options.add_argument("headless")
options.add_argument("user-agent=" + USER_AGENT)
options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(DRIVER_PATH, options=options)

url = "http://127.0.0.1:4444/wd/hub"
driver = webdriver.Remote(
    command_executor=url, desired_capabilities=options.to_capabilities()
)
# print(driver.session_id)
# driver.get("https://www.bbc.com/")

session_id = "06e007da5f066e6a84c666b7868847e8"
driver.session_id = session_id

# driver.get(url)
# sg pools sometimes alert that I am not using the correct version of a browser
# try:
#     alert = driver.switch_to_alert()
#     alert.accept()
# except:
#     print("no alert to accept")

selected_div = driver.find_element_by_xpath('//div[@class="event-list"]')

# get listed matches
# bet_type_selector = selected_div.find_element_by_xpath('//select[@name="upcomingFootball_filterBetType"]')
# bet_type_selection = selected_div.find_element_by_xpath("//option[@value='HL']")
# bet_type_selection.click()
# display_button = selected_div.find_element_by_xpath('//button[./span = "Display"]')
# display_button.click()

match_odds = []
# get individual matches data
matches_rows = selected_div.find_elements_by_xpath('//div[@class="event-list__event"]')

for match in matches_rows:

    try:
        match_title = match.find_element_by_xpath(
            './/span[@class="event-list__event-name"]/a'
        ).text.strip()
        print(match_title)
        outcomes = match.find_elements_by_xpath(
            './/div[@class="event-market__outcome-row"]/div[contains(@class,"outcome")]'
        )

        temp_dict = {"match_title": match_title}

        for outcome in outcomes:
            outcome_text = outcome.find_element_by_xpath(
                './/span[@class="button-outcome__text"]/span'
            ).text.strip()
            outcome_price = outcome.find_element_by_xpath(
                './/span[@class="button-outcome__price"]'
            ).text.strip()

            if "Over" in outcome_text:
                temp_dict["over"] = {"Market": outcome_text, "odds": outcome_price}
            elif "Under" in outcome_text:
                temp_dict["under"] = {"Market": outcome_text, "odds": outcome_price}

        match_odds.append(temp_dict)

    except NoSuchElementException:
        continue

print(match_odds)

