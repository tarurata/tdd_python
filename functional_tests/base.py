from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from django.test.runner import DiscoverRunner
from django.conf import settings
import time

MAX_WAIT = 10


class TestRunner(DiscoverRunner):
    def __init__(self, url=None, **kwargs):
        super().__init__(**kwargs)
        
        print("Passed url: {}".format(url))
        self.url = url
    
    @classmethod
    def add_arguments(cls, parser):
        DiscoverRunner.add_arguments(parser)
        parser.add_argument('-u', '--url', help='Existing server url for test')
    
    def setup_test_environment(self, **kwargs):
        super(TestRunner, self).setup_test_environment(**kwargs)
        settings.TEST_SETTINGS = {
            'url': self.url,
        }


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        if hasattr(settings, 'TEST_SETTINGS'):
            self.live_server_url = settings.TEST_SETTINGS['url']
    
    def tearDown(self):
        self.browser.quit()
    
    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                # table = self.browser.find_element(By.ID, 'id_list_table')
                # rows = table.find_elements(By.TAG_NAME, 'tr')
                # self.assertIn(row_text, [row.text for row in rows])
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
    
    def get_item_input_box(self):
        return self.browser.find_element(By.ID, 'id_text')
