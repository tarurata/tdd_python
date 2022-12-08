from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test.runner import DiscoverRunner
from django.conf import settings


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
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
