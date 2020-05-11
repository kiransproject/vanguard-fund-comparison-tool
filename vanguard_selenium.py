import sys, os, re, requests, time, datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
chromedriver = "/home/K/git_projects/vanguard_fund_comparison/chromedriver"

fund1_url="https://www.vanguardinvestor.co.uk/investments/vanguard-ftse-global-all-cap-index-fund-gbp-accumulation-shares/portfolio-data?intcmpgn=equityglobal_ftseglobalallcapindexfund_fund_link"
fund2_url="https://www.vanguardinvestor.co.uk/investments/vanguard-us-equity-index-fund-accumulation-shares/portfolio-data?intcmpgn=equityusa_usequityindexfund_fund_link"

def create_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
    return driver

def terminate(driver):
    driver.quit()

def get_fund_name(url):
    name = re.compile('vanguard-.*(.+?(?=/))')
    result = name.search(url)
    return result.group(0).upper()

def compare_funds(fund_url):
    try:
        fund_list = []
        print('Creating Chrome Driver ...')
        driver = create_driver()
        print('Loading Fund:', get_fund_name(fund_url))
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
        return fund_list
        terminate(driver)
    except Exception as e:
        terminate(driver)
        raise ValueError(str(e))

if __name__ == "__main__":
    fund1_name=(get_fund_name(fund1_url))
    fund2_name=(get_fund_name(fund2_url))
    fund2=compare_funds(fund2_url)
    fund1=compare_funds(fund1_url)
    duplicates=set(fund1).intersection(fund2)
    print(len(duplicates), ' overlapping companies between ', fund1_name,' and ', fund2_name, '. Equating to ', (((len(duplicates))/(len(fund1)))*100), '% overlap for ', fund1_name,' and ', (((len(duplicates))/(len(fund2)))*100), '% overlap for ', fund2_name)
