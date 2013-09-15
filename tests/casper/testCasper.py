import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from tests.config import get_config

class CasperTestCase(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(CasperTestCase, self).__init__(*args, **kwargs)
        self.config = get_config()
    
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=self.config['common']['chromedriver_path'])

    def test_casper(self):
        driver = self.driver
        config = self.config
        driver.get(config['casper']['url'])
        self.assertIn("CAS", driver.title)
        elem = driver.find_element_by_name("username")
        elem.send_keys(config['user']['username'])
        elem = driver.find_element_by_name("password")
        elem.send_keys(config['user']['password'])
        elem.send_keys(Keys.RETURN)
        self.assertIn("payutc", driver.title)
        
        

    def tearDown(self):
        self.driver.close()
