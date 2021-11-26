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

#User Fixtures
@pytest.fixture
def user1():
    return {'username':'Student','email':'student@wsu.edu','password':'123',
    'firstname':'George', 'lastname': 'Washington', 'phone':'5093385885',
    'gpa': '4.0', 'major':'Political Science', 'graduation':'7/1776',
    'experience':'President of the United States'
    }

@pytest.fixture
def user2():
    return {'username':'Faculty','email':'faculty@wsu.edu','password':'123'}    

@pytest.fixture
def registerTest():
    return {'username':'Student','email':'registerTest@wsu.edu','password':'123'}

@pytest.fixture
def emailTest():
    return {'username':'email','email':'test@gmail.com','password':'123'}

@pytest.fixture
def doubleCheck():
    return{'username':'double','email':'double@wsu.edu','password':'123'}


#https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/

#Setting up browser

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


#Tests

#Testing for selecting both studnent and faculty usertypes
def test_double_select(browser,doubleCheck):
    browser.get('http://localhost:5000/register')

    browser.find_element_by_name("username").send_keys(doubleCheck['username'])
    sleep(1)
    browser.find_element_by_name("email").send_keys(doubleCheck['email'])
    sleep(1)
    browser.find_element_by_name("faculty").click()
    browser.find_element_by_name("student").click()
    sleep(1)
    browser.find_element_by_name("password").send_keys(doubleCheck['password'])
    sleep(1)
    browser.find_element_by_name("password2").send_keys(doubleCheck['password'])
    sleep(1)
    browser.find_element_by_name("submit").click()
    sleep(3)

    content = browser.page_source
    assert 'Please select student OR faculty.' in content

#Test for registering a faculty member
def test_faculty_register(browser,user2):
    browser.get('http://localhost:5000/register')

    browser.find_element_by_name("username").send_keys(user2['username'])
    sleep(1)
    browser.find_element_by_name("email").send_keys(user2['email'])
    sleep(1)
    browser.find_element_by_name("faculty").click()
    sleep(1)
    browser.find_element_by_name("password").send_keys(user2['password'])
    sleep(1)
    browser.find_element_by_name("password2").send_keys(user2['password'])
    sleep(1)
    browser.find_element_by_name("submit").click()
    sleep(3)

    content = browser.page_source
    assert 'Registration Successful.' in content

#Testing for registering as a student
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
    sleep(1)

    browser.find_element_by_name("firstname").send_keys(user1['firstname'])
    sleep(1)
    browser.find_element_by_name("lastname").send_keys(user1['lastname'])
    sleep(1)
    browser.find_element_by_name("phone").send_keys(user1['phone'])
    sleep(1)
    browser.find_element_by_name("gpa").send_keys(user1['gpa'])
    sleep(1)
    browser.find_element_by_name("major").send_keys(user1['major'])
    sleep(1)
    browser.find_element_by_name("graduation").send_keys(user1['graduation'])
    sleep(1)

    browser.find_element_by_id("research-0").click()
    browser.find_element_by_id("research-1").click()
    browser.find_element_by_id("research-2").click()
    sleep(1)

    browser.find_element_by_id("language-2").click()
    browser.find_element_by_id("language-3").click()
    browser.find_element_by_id("language-4").click()
    sleep(1)

    browser.find_element_by_name("experience").send_keys(user1['experience'])
    sleep(1)

    browser.find_element_by_name("submit").click()
    sleep(1)


    content = browser.page_source
    assert 'Your account has been updated' in content

#Testing for validation error for duplicate username
def test_register_fail_user(browser, registerTest):
    browser.get('http://localhost:5000/register')

    browser.find_element_by_name("username").send_keys(registerTest['username'])
    sleep(1)
    browser.find_element_by_name("email").send_keys(registerTest['email'])
    sleep(1)
    browser.find_element_by_name("student").click()
    sleep(1)
    browser.find_element_by_name("password").send_keys(registerTest['password'])
    sleep(1)
    browser.find_element_by_name("password2").send_keys(registerTest['password'])
    sleep(1)
    browser.find_element_by_name("submit").click()
    sleep(1)

    content = browser.page_source

    assert 'This username already exists. Please use a different username.' in content

#Testing for WSU email domain
def test_email_domain(browser, emailTest):
    browser.get('http://localhost:5000/register')

    browser.find_element_by_name("username").send_keys(emailTest['username'])
    sleep(1)
    browser.find_element_by_name("email").send_keys(emailTest['email'])
    sleep(1)
    browser.find_element_by_name("student").click()
    sleep(1)
    browser.find_element_by_name("password").send_keys(emailTest['password'])
    sleep(1)
    browser.find_element_by_name("password2").send_keys(emailTest['password'])
    sleep(1)
    browser.find_element_by_name("submit").click()
    sleep(1)

    content = browser.page_source

    assert 'Please register using a wsu.edu email address' in content

    
