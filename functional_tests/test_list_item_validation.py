from .base import FunctionalTest
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, 'id_new_item').send_keys('\n')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        error = self.browser.find_element(By.CSS_SELECTOR, '.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        
        # She tires again with some text for the item, which now works
        # self.browser.find_element(By.ID, 'id_new_item') = self.browser.find_element(By.ID, 'id_new_item')
        self.browser.find_element(By.ID, 'id_new_item').send_keys('Buy milk\n')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy milk')
        
        # Perversely, she now decides to submit a second blank list item
        self.browser.find_element(By.ID, 'id_new_item').send_keys('\n')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        time.sleep(1)
        
        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element(By.CSS_SELECTOR, '.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # And she can correct it by filling some text in
        self.browser.find_element(By.ID, 'id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
