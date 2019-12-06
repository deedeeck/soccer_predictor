# This file crawls websites for soccer odds

import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException


def set_chrome_options(headless_mode=False):
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=" + user_agent)
    options.add_argument("--profile-directory=Default")

    if headless_mode:
        options.add_argument("headless")

    return options

def wait_till_element_loads(driver,xpath_query):
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    try:
        delay = 5 #seconds
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath_query)))
    except TimeoutException:
        print("page took too long to load")


def crawl_individual_page(driver,page_link):

    valid_bet_types = ["1X2","Total Goals Over/Under 2.5","Total Goals Over/Under 3.5","1/2 Goal"]

    if driver.current_url != page_link:
        driver.get(page_link)

    wait_till_element_loads(driver,'//div[@class="event-markets"]')

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    match_id = page_link.split("/")[6]

    fixture_title = driver.find_element_by_xpath('//span[@class="event-header__event-name"]/span').text.strip()
    fixture_date = driver.find_element_by_xpath('//span[@class="event-header__start-time"]').text.strip()

    bet_types_list = driver.find_elements_by_xpath('//div[@class="event-markets__market js-collapsable"]')

    for bet_type in bet_types_list:
        bet_type_string = bet_type.find_element_by_xpath('.//span[@class="header-title__title"]').text
        
        # only crawl valid bet types
        if bet_type_string in valid_bet_types:
            bet_row = bet_type.find_element_by_xpath('.//div[@class="event-market__outcome-row"]')
            odds = bet_row.find_elements_by_xpath('.//span[@class="button-outcome__price"]')

            if bet_type_string == "1X2":
                home_odds = odds[0].text
                draw_odds = odds[1].text
                away_odds = odds[2].text

            elif bet_type_string == "Total Goals Over/Under 2.5" or bet_type_string == "Total Goals Over/Under 3.5":
                over_under_type = " ".join(bet_type_string.split(" ")[-2:])
                over_odds = odds[0].text
                under_odds = odds[1].text

            elif bet_type_string == "1/2 Goal":
                 home_halfgoal_odds = odds[0].text
                 away_halfgoal_odds = odds[1].text

    crawled_data = {}
    crawled_data['match_id'] = match_id
    crawled_data['timestamp'] = timestamp
    crawled_data['fixture_title'] = fixture_title
    crawled_data['fixture_date'] = fixture_date
    crawled_data['home_odds'] = home_odds
    crawled_data['draw_odds'] = draw_odds
    crawled_data['away_odds'] = away_odds
    crawled_data['over_under_type'] = over_under_type
    crawled_data['over_odds'] = over_odds
    crawled_data['under_odds'] = under_odds
    crawled_data['home_halfgoal_odds'] = home_halfgoal_odds
    crawled_data['away_halfgoal_odds'] = away_halfgoal_odds

    return crawled_data    

def write_result_to_csv(result_dict):
    import csv
    import os

    file_exists = os.path.isfile('result.csv')

    with open('result.csv', 'a') as f: 
        w = csv.DictWriter(f, result_dict.keys())

        if not file_exists:
            w.writeheader() 

        w.writerow(result_dict)


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

    driver.maximize_window()

    web_url = "https://online.singaporepools.com/en/sports/competition/36/football/england/english-premier"

    if driver.current_url != web_url:
        driver.get(web_url)

    # sg pools sometimes alert that I am not using the correct version of a browser
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        print("No alert appeared")

    # used to test individual webpage
    # result = crawl_individual_page(driver,web_url)
    # write_result_to_csv(result)

    # temp commented out
    wait_till_element_loads(driver,'//table[@class="table-condensed"]')
    matches_link = [link.get_attribute("href") for link in driver.find_elements_by_xpath('//td[@class="col-xs-3 hidden-xs"]/span[@class="event-list__event-name"]/a')]

    for link in matches_link:
        result = crawl_individual_page(driver,link)
        write_result_to_csv(result)

    if not remote_mode:
        driver.quit()
