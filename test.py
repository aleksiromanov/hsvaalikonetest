#!/usr/bin/python3

import unittest
import inspect
#import matplotlib.pyplot as plt
from selenium import webdriver
import time 
from random import randint
import numpy as np
#import tensorflow as tf
from scipy.stats import kurtosis, skew, gengamma

URL_VAALIKONE        = "https://www.vaalikone.fi/eduskunta2019/"
OUTPUT_FILE          = "/tmp/LOG"

_SOME_COMMON_DIV_    = "//*[@id='app']/div/main/div/div"
XPATH_QUESTION       = _SOME_COMMON_DIV_ + "[1]/div/div/div[1]/div[1]/div"
XPATH_ANSWER         = _SOME_COMMON_DIV_ + "[1]/div/div/div[1]/div[2]/div[1]/button[%d]"
XPATH_RESULTS_BUTTON = _SOME_COMMON_DIV_ + "[1]/div/div[2]/button"
XPATH_MATCH_PARTY    = _SOME_COMMON_DIV_ + "[1]/div/div[1]/div[3]/div[1]/div/div[1]/div/div[2]/div[2]"
XPATH_DISTRICT       = "//button[@data-district-name='Helsinki']"
CLASS_START_BUTTON   =  "big__1kEOQ"
CLASS_RESULTS_BUTTON =  "button__1ARU2"


class Test(unittest.TestCase):

    driver = None
    out = None

    def _init_driver(self):
        print(inspect.stack()[0][3])
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.add_argument('--window-size=1420,1080')
        #options.add_argument('--no-sandbox')
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.binary_location = "/snap/bin/chromium"
        self.driver = webdriver.Chrome(options=options)
        print(inspect.stack()[0][3] + " - OK")

    def _init_output(self):
        print(inspect.stack()[0][3])
        self.out = open(OUTPUT_FILE, "w")

    def _get_answer_set(self):
        print(inspect.stack()[0][3])
        x = np.random.gamma(2, 2, 30)
        print(x)
        #ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')
        #x = np.random.normal(0, 2, 10000)   # create random values based on a normal distribution
        #print( 'excess kurtosis of normal distribution (should be 0): {}'.format( kurtosis(x) ))
        #print( 'skewness of normal distribution (should be 0): {}'.format( skew(x) ))
        return x

    def _select_district(self):
        print(inspect.stack()[0][3])
        time.sleep(2)
        el = self.driver.find_element_by_xpath(XPATH_DISTRICT)
        self.output("D", el.text)
        el.click()

    def _goto_main_page(self):
        print(inspect.stack()[0][3])
        self.driver.get(URL_VAALIKONE)

    def _goto_questions(self):
        print(inspect.stack()[0][3])
        time.sleep(2)
        self.driver.find_element_by_class_name(CLASS_START_BUTTON).click()

    def _loop_through_questions(self):
        print(inspect.stack()[0][3])
        time.sleep(2)
        for i in [randint(1, 5) for i in range(0, 30)]:
            time.sleep(1)
            self.output("Q", str(i) + " " + self.driver.find_element_by_xpath(XPATH_QUESTION).text)
            self.driver.find_element_by_xpath(XPATH_ANSWER % i).click()

    def _ok_startup_alert(self):
        print(inspect.stack()[0][3])
        time.sleep(5)
        self.driver.switchTo().alert().accept();

    def output(self, label, text = '', delim = ' '):
        line = str(delim.join([label, text]).encode('utf-8').strip())
        self.out.write(line + "\n")
        print(line)

    def _print_results(self):
        print(inspect.stack()[0][3])
        time.sleep(1)
        el = self.driver.find_element_by_xpath(XPATH_MATCH_PARTY)
        self.output("R", el.text.split("\n")[0])

    def _goto_results(self):
        print(inspect.stack()[0][3])
        try:
            time.sleep(1)
            el = self.driver.find_element_by_class_name(CLASS_RESULTS_BUTTON)
            time.sleep(1)
            el.click()
        except:
            self.output('Error in _goto_results')

    def _accept_cookies(self):
        print(inspect.stack()[0][3])
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='sccm-opt-out-c1']").click()
    def setUp(self):
        print(inspect.stack()[0][3])
        self._init_driver()
        self._init_output()

    def testOne(self):
        print(inspect.stack()[0][3])
        if True:
            self._get_answer_set()
        else:
            #self._ok_startup_alert()
            self._goto_main_page()
            self._accept_cookies()
            self._select_district()
            self._goto_questions()
            self._loop_through_questions()
            self._goto_results()
            self._print_results()

    def tearDown(self):
        print(inspect.stack()[0][3])
        if self.driver:
            self.driver.close()
        if self.out:
            self.out.close()

if __name__ == '__main__':
    unittest.main()

