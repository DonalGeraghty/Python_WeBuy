from playwright.sync_api import Page, expect
from blu_ray import Bluray

import re, time


class CexPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://ie.webuy.com/search?productLineId=41&productLineName=Blu-Ray"
        self.title = "CeX"
        self.title_locator = ".card-title"
        self.price_locator = ".product-prices"
        self.product_card_locator = ".search-product-card"
        self.cookies = self.page.locator("#cmpbntyestxt:has-text('Accept All Cookies')")
        self.blu_ray_4k = self.page.locator('span.item-label:has-text("Blu-Ray 4K")').locator('..').locator(
            ".checkmark")
        self.in_stock_online = self.page.locator('span.item-label:has-text("In Stock Online")').first.locator(
            '..').locator(".checkmark")
        self.next_page = self.page.locator('[aria-label="Next Page"]')

    def goto_website(self):
        self.page.goto(self.url)

    def assert_page_title(self):
        expect(self.page).to_have_title(re.compile(self.title))

    def accept_cookies(self):
        self.cookies.click()

    def filter_blu_ray_4k(self):
        self.blu_ray_4k.first.click()

    def filter_in_stock_online(self):
        self.in_stock_online.click()

    def click_next_page(self):
        self.next_page.click()

    # complex data
    def get_all_blu_rays(self):
        cex_page = CexPage(self.page)
        old_url = self.page.url
        my_list = []
        while True:
            blu_ray_all = self.page.locator(self.product_card_locator).all()
            for index, blu_ray in enumerate(blu_ray_all):
                title = blu_ray.locator(self.title_locator).inner_text()
                price = blu_ray.locator(self.price_locator).inner_text()
                blu = Bluray(title, price)
                my_list.append(blu)
            cex_page.click_next_page()
            time.sleep(1)
            new_url = self.page.url
            if old_url is new_url:
                break
            else:
                old_url = new_url
        return my_list
