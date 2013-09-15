import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from tests.config import get_config

class MozartTestCase(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(MozartTestCase, self).__init__(*args, **kwargs)
        self.config = get_config()
    
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=self.config['common']['chromedriver_path'])

    def test_mozart(self):
        driver = self.driver
        config = self.config
        driver.get(config['mozart']['url'])
        time.sleep(0.5) # sleep because the mozart redirection is done in javascript and not http code
        self.assertIn("CAS", driver.title)
        elem = driver.find_element_by_name("username")
        elem.send_keys(config['user']['username'])
        elem = driver.find_element_by_name("password")
        elem.send_keys(config['user']['password'])
        elem.send_keys(Keys.RETURN)
        self.assertIn("mozart", driver.title)
        
        

    def tearDown(self):
        self.driver.close()
