from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_LIST_ERROR,
    ExistingListItemForm, ItemForm
)
from lists.forms import ItemForm, EMPTY_LIST_ERROR
import re
from unittest import skip
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest

from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item, List
from django.utils.html import escape
from lists.forms import ItemForm


class SendLoginEmailViewTest(TestCase):
    
    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'wmsupo@gmail.com'
        })
        self.assertRedirects(response, '/')


class HomePageTest(TestCase):
    maxDiff = None
    
    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)
    
    # def assertEqualExceptCSRF(self, html_code1, html_code2):
    #     return self.assertEqual(
    #         self.remove_csrf(html_code1),
    #         self.remove_csrf(html_code2),
    #     )
    
    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, home_page)
    
    # def test_home_page_returns_correct_html(self):
    #     request = HttpRequest()
    #     response = home_page(request)
    #     expected_html = render_to_string('home.html', {'form': ItemForm()})
    #     self.assertEqualExceptCSRF(response.content.decode(), expected_html)
    # self.assertMultiLineEqual(response.content.decode(), expected_html)
    
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')
    
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)
    
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
    
    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )
        
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
    
    # def test_validation_errors_end_up_on_lists_page(self):
    #     list_ = List.objects.create()
    #     response = self.client.post(
    #         f'/lists/{list_.id}/',
    #         data={'text': ''}
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'list.html')
    #     expected_error = escape("You can't have an empty list item")
    #     self.assertContains(response, expected_error)
    
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )
    
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
    
    def test_for_invalid_input_renders_nothing_saved_to_db(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
    
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)
    
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
    
    @skip
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'listts/{list1.id}/',
            data={'text': 'textey'}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)
    
    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')
    
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)


class NewListTest(TestCase):
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )
        
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
    
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)
    
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
    
    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
    
    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
    
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)
