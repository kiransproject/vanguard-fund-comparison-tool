import sys, os, re, requests, time, datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
chromedriver = "/home/K/git_projects/vanguard_fund_comparison/chromedriver"


def create_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
    return driver

def terminate(driver):
    driver.quit()


def compare_funds(fund_url):
    try:
        fund_list = []
        print('Creating Chrome Driver ...')
        driver = create_driver()
        print('Loading Fund ...')
        driver.get(fund_url)
        time.sleep(3)
        print('Determining number of stock in the fund ...')
        total_stocks=driver.find_element_by_xpath('//*[@id="vuiMenu2_errorHoverTarget"]/div/div/div/p').text
        arraysize= total_stocks.split()
        no_of_funds = int(arraysize[-1])
        next_page = driver.find_element_by_xpath('//*[@id="vuiMenu2_errorHoverTarget"]/div/div/div/vui-action-bar/vui-action-bar-item[2]/button')
        print('Iterating through ', no_of_funds, ' stocks')
        while len(fund_list) < no_of_funds:
                for i in range (1,11):
                       xpath=('//*[@id="holdingDetailsEquity"]/div[2]/div/div[2]/div/table/tbody/tr[%d]/td[1]' % i)
                       fund_list.append(driver.find_element_by_xpath(xpath).text)
                       time.sleep(0.5)
                if ( (len(fund_list) + 10) < no_of_funds ):
                        print ('Next Page, total recorded ', len(fund_list), 'stocks' )
                        driver.execute_script("arguments[0].click();", next_page)        
        print(fund_list)
        return fund_list
        terminate(driver)
    except Exception as e:
        terminate(driver)
        raise ValueError(str(e))

if __name__ == "__main__":
    fund2=compare_funds("https://www.vanguardinvestor.co.uk/investments/vanguard-us-equity-index-fund-accumulation-shares/portfolio-data")
    fund1=compare_funds("https://www.vanguardinvestor.co.uk/investments/vanguard-ftse-global-all-cap-index-fund-gbp-accumulation-shares/portfolio-data")
    duplicates=set(fund1).intersection(fund2)
    print(len(duplicates), ' overlapping companies between the two funds, equating to ', (((len(duplicates))/(len(fund1)))*100), '% overlap for fund 1 and ', (((len(duplicates))/(len(fund1)))*100), '% overlap for fund2')
