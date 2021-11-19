import pytest
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep

# pip install -U selenium

#run using (after running backend):
# pytest -v tests\test_selenium.py

#User Fixture
@pytest.fixture
def user1():
    return {'username':'test1','email':'test@wsu.edu','password':'123'}

#User Fixture
@pytest.fixture
def user2():
    return {'username':'test2','email':'test2@wsu.edu','password':'123'}



#https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/

@pytest.fixture
def browser():
    CHROME_PATH = 'c:\\Webdriver' #Add a new folder called Webdriver
    print(CHROME_PATH)
    opts = Options()
    opts.headless = False #Change to true  if you don't want it to open browser
    driver = webdriver.Chrome(options=opts, executable_path= CHROME_PATH + '/chromedriver.exe') #Add chromedriver to Webdriver folder
    driver.implicitly_wait(10)

    yield driver
    
    driver.quit()

def test_register(browser,user1):
    browser.get('http://localhost:5000/register')

    browser.find_element_by_name("username").send_keys(user1['username'])
    sleep(1)
    browser.find_element_by_name("email").send_keys(user1['email'])
    sleep(1)
    browser.find_element_by_name("student").click()
    sleep(1)
    browser.find_element_by_name("password").send_keys(user1['password'])
    sleep(1)
    browser.find_element_by_name("password2").send_keys(user1['password'])
    sleep(1)
    browser.find_element_by_name("submit").click()
    sleep(2)

    content = browser.page_source

    assert 'Registration Successful.' in content