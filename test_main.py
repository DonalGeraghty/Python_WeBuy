import data_control
import time

from playwright.sync_api import sync_playwright

import pytest

import my_mailer
from cex_page import CexPage


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # You can choose 'firefox' or 'webkit' as well
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    page.goto("https://ie.webuy.com/search?productLineId=41&productLineName=Blu-Ray", wait_until="load")  # Replace with the actual path to your HTML file
    yield page
    page.close()

def test_we_buy(page):
    cex_page = CexPage(page)
    cex_page.goto_website()
    page.wait_for_load_state()
    cex_page.assert_page_title()
    cex_page.accept_cookies()
    cex_page.filter_blu_ray_4k()
    time.sleep(3)
    cex_page.filter_in_stock_online()
    time.sleep(3)
    blu_ray_all = cex_page.get_all_blu_rays()
    data_control.output_blu_rays(blu_ray_all)
    blu_ray_list = data_control.return_diff_yesterday_today()
    name_price_df = data_control.get_prices_from_list(blu_ray_list)
    data_control.cleanup_files()
    my_mailer.send_mail(name_price_df)
