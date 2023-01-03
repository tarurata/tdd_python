from .base import FunctionalTest
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from django.utils.html import escape


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # The browser intercepts the request, and does not load the list page
        self.wait_for(lambda: self.browser.find_elements(By.CSS_SELECTOR,
                                                         '#id_text:invalid'
                                                         ))
        
        # She start typing some text for the new item and the error disappears
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements(By.CSS_SELECTOR,
                                                         '#id_text:invalid'
                                                         ))
        # And She can submit it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        
        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # Again, the browser will not comply
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_elements(By.CSS_SELECTOR,
                                                         '#id_text:invalid'
                                                         ))
        
        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements(By.CSS_SELECTOR,
                                                         '#id_text:invalid'
                                                         ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
    
    def test_cannot_add_duplicate_items(self):
        # Edith goes to the hom page and starts a new list
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy wellies')
        
        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # she sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this item in your list"
        ))
    
    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.add_list_item(('Banter too thick'))
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))
        
        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')
        # self.get_item_input_box().send_keys(Keys.ENTER)
        
        # She is pleased to see that the error message disappears
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
    
    def get_error_element(self):
        return self.browser.find_element(By.CSS_SELECTOR, '.has-error')
