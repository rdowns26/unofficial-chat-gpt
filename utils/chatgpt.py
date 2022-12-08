import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# function to check if an element exists by its XPATH
def check_exists_by_xpath(xpath,driver):
    try:
        driver.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        print (str(xpath) + "- element not found")
        return False
    print (str(xpath) + "- element found")
    return True

# function to wait for elements to appear before clicking on them
def wait_for_element(xpath, driver):
    timeout = 60 # up to 60 seconds
    try:
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
        print (str(xpath) + "- element found")
    except TimeoutException:
        print ("request timed out")

def create_connection(openai_email, openai_password):
    
    # Arguments to use Browserless to create a headless Chrome instance
    chrome_options = webdriver.ChromeOptions()
    # Get Browserless API key from account at https://cloud.browserless.io/account/
    chrome_options.set_capability('browserless:token', os.getenv("BROWSERLESS_KEY"))
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Remote(
        command_executor='https://chrome.browserless.io/webdriver',
        options=chrome_options
    )

    print ("Launching Browserless Chrome instance")
    
    # Create a new Selenium WebDriver instance and navigate to web app's URL
    driver.get('https://chat.openai.com/chat')
    
    print ("Browserless Chrome instance launched")
    
    # pause 5 seconds to let the page load
    time.sleep(5)
    
    print ("Checking for Log In button")

    # Due to ChatGPT's random outages, this logic checks if login button comes up, and if not, returns "try again later"
    if check_exists_by_xpath('//button[text()="Log in"]',driver):
        print ("Login button found")
        
        # Find the log in button and click it
        driver.find_element(By.XPATH, '//button[text()="Log in"]').click()
        print ("Login button clicked")
        
        # wait for username element to appear
        wait_for_element('//*[@id="username"]', driver)
        print ("Username input found")
        
        # Find the email input field, enter your email address, and hit continue
        driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(openai_email)
        driver.find_element(By.XPATH, '//button[text()="Continue"]').click()
        print ("Username submitted")
        
        # wait for Password element to appear
        wait_for_element('//*[@id="password"]', driver)
        print ("Password input found")
        
        # Find the password input field and enter your password and click continue
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(openai_password)
        driver.find_element(By.XPATH, '//button[text()="Continue"]').click()
        print ("Password submitted")
        
        # wait for Next element to appear
        wait_for_element('//button[text()="Next"]', driver)
        print ("Next button found")
        
        # Move through the popup screen with the three buttons
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()
        driver.find_element(By.XPATH, '//button[text()="Done"]').click()
        print ("ChatGPT is open and ready")
        return driver
    else:
        # If the login button is not found, we want to quit the driver and tell the user
        driver.quit()
        print ("Log in button not found")
        return "Try again later"

# function to ask ChatGPT the message once the driver instance has been created
def ask_question(driver, message):
    print ("Submitting text message to ChatGPT")
    
    # Find the text input field, enter text, and submit text
    driver.find_element(By.CSS_SELECTOR, "textarea").send_keys(message)
    driver.find_element(By.CSS_SELECTOR, "textarea").submit()
    print ("Request submitted")

    # waiting until the "try again" button appears to parse the finished response
    timeout = 60 # will wait up to 60 seconds for a response
    print ("ChatGPT response loading")
    
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//button[@class="btn flex gap-2 justify-center btn-neutral"]'))
        WebDriverWait(driver, timeout).until(element_present)
        print ("ChatGPT responded")
    except TimeoutException:
        print ("ChatGPT took too long")

    print ("Grabbing ChatGPT response")
    # appending all responses to list
    response = []
    for element in driver.find_elements(By.TAG_NAME,'p'):
        response.append(element.text)
    
    print ("ChatGPT's response:")
    print(response)

    return response

def close_connection(driver):
    # Close the browser
    print ("Browser closing...")
    driver.quit()