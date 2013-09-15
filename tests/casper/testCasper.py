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
    
    def login(self):
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
    
    def test_load(self):
        driver = self.driver
        config = self.config
        self.login()
    
    def test_reload(self):
        driver = self.driver
        config = self.config
        
        # login
        self.login()
        
        
        # get elements
        big_panel = driver.find_element_by_xpath("//div[@class='hero-unit']")
        solde_container = big_panel.find_element_by_tag_name('strong')
        solde = float(solde_container.text.replace('€', '').replace(',', '.').strip())
        button_reload = driver.find_element_by_xpath("//form[@action='/payutc/casper/index.php?reload']/div/button[@type='submit']")
        
        ##
        # TEST RELOAD
        #
        
        button_reload.click()
        
        ### Page 1 : payement type
        
        # assert we are on paybox page
        self.assertIn('PAYBOX', driver.title)
        # choose CB reload
        button_cb = driver.find_element_by_xpath("//input[@name='PBX_TYPECARTE'][@value='CB']")
        button_cb.click()
        # submit
        button_ok = driver.find_element_by_id('boutonA0')
        button_ok.click()
        
        ### Page 2 : card information
        
        # input card number
        input_card_number = driver.find_element_by_id('NUMERO_CARTE')
        # inputs expiration date
        select_month_validity = driver.find_element_by_id('MOIS_VALIDITE')
        all_mounth_options = select_month_validity.find_elements_by_tag_name("option")
        select_year_validity = driver.find_element_by_id('AN_VALIDITE')
        all_year_options = select_year_validity.find_elements_by_tag_name("option")
        # input short code
        input_short_code = driver.find_element_by_id('CVVX')
        # submit button
        button_submit = driver.find_element_by_xpath("//input[@name='VALIDER']")
        # fill the form
        input_card_number.send_keys('1111222233334444')
        all_mounth_options[-1].click()
        all_year_options[-1].click()
        input_short_code.send_keys('123')
        # submit form
        button_submit.click()
        
        ### Page 3 : ticket
        
        # assert we are on the ticket page
        self.assertIn('Ticket', driver.title)
        # assert this is a success
        body = driver.find_element_by_tag_name('body')
        self.assertIn('succès', body.text)
        # back to casper
        continue_link = driver.find_element_by_tag_name('a')
        continue_link.click()
        
        ### Page 4 : casper again
        
        self.assertIn('payutc', driver.title)
        alert = driver.find_element_by_class_name('alert-success')
        self.assertIn('recharg', alert.text)
        
        ##
        # END TEST RELOAD
        #

    def tearDown(self):
        self.driver.close()
