from playwright.sync_api import sync_playwright
# var newShimmer=new Game.shimmer("golden");
# Game.cookies = 1


class CookieClicker:
    WEBSITE_URL = "https://orteil.dashnet.org/cookieclicker/"
    LANGUAGE_SELECT_LOCATOR = '#langSelect-EN'
    ACCEPT_COOKIES_ALERT_LOCATOR = '//a[@class="cc_btn cc_btn_accept_all"]'
    CLOSE_ACHIEVEMENT_ALERT_LOCATOR = '//div[@class="framed close sidenote"]'
    BIG_COOKIE_LOCATOR = '#bigCookie'
    GOLDEN_COOKIE_LOCATOR = '//div[@class="shimmer" and @alt="Golden cookie"]'
    TOTAL_COOKIES_LOCATOR = '#cookies'
    PRODUCT_COUNT = 20

    def __init__(self, page):
        self.page = page

    def launch(self):
        self.page.goto(self.WEBSITE_URL)

    def select_language(self):
        language_select = self.page.locator(self.LANGUAGE_SELECT_LOCATOR)
        language_select.click(force=True)

    def accept_cookies(self):
        accept_cookies_alert = self.page.locator(self.ACCEPT_COOKIES_ALERT_LOCATOR)
        if accept_cookies_alert.is_visible():
            accept_cookies_alert.click()
        else:
            pass

    def close_achievement_alert(self):
        achievement_alert = self.page.locator(self.CLOSE_ACHIEVEMENT_ALERT_LOCATOR)
        if achievement_alert.is_visible():
            achievement_alert.click(force=True)
        else:
            pass

    def click_big_cookie(self):
        cookie = self.page.locator(self.BIG_COOKIE_LOCATOR)
        cookie.click(force=True)

    def click_golden_cookie(self):
        golden_cookie = self.page.query_selector_all(self.GOLDEN_COOKIE_LOCATOR)
        for cookie_element in golden_cookie:
            cookie_element.click()
        else:
            pass

    def get_cookies(self):
        number_dictionary = {
            'million': 1000000, 'billion': 1000000000, 'trillion': 1000000000000,
            'quadrillion': 1000000000000000, 'quintillion': 1000000000000000000,
            'sextillion': 1000000000000000000000, 'septillion': 1000000000000000000000000,
            'octillion': 1000000000000000000000000000}
        cookies = self.page.locator(self.TOTAL_COOKIES_LOCATOR).inner_text()
        cookies = cookies.split()
        if not cookies:
            return 0
        else:
            cookie_number = cookies[0]
            cookie_suffix = cookies[1]
            cookies = cookie_number + cookie_suffix
            for key, value in number_dictionary.items():
                if cookie_suffix == key:
                    result = value * float(cookie_number)
                    return int(result)
            else:
                cookies = ''.join(filter(str.isdigit, cookies))
                return int(cookies)

    def get_product_price(self, index):
        number_dictionary = {
            'million': 1000000, 'billion': 1000000000, 'trillion': 1000000000000,
            'quadrillion': 1000000000000000, 'quintillion': 1000000000000000000,
            'sextillion': 1000000000000000000000, 'septillion': 1000000000000000000000000,
            'octillion': 1000000000000000000000000000}
        product_price = self.page.locator(f'#productPrice{index}').inner_text()
        product_price = product_price.split()
        if len(product_price) > 1:
            cost = product_price[0]
            cost_suffix = product_price[1]
            for key, value in number_dictionary.items():
                if cost_suffix == key:
                    result = value * float(cost)
                    return int(result)
        else:
            product_price = product_price[0].replace(",", "")
            return int(product_price)

    def buy_product(self, index):
        product = self.page.locator(f'#product{index}')
        if self.get_cookies() >= self.get_product_price(index):
            product.click()
        else:
            pass

    def buy_all_products(self):
        for i in range(self.PRODUCT_COUNT - 1, -1, -1):
            self.buy_product(i)


def main():
    with sync_playwright() as playwright_function:
        chrome = playwright_function.chromium
        browser = chrome.launch(headless=False)
        browser_context = browser.new_context(no_viewport=True)
        page = browser_context.new_page()

        cookie_clicker = CookieClicker(page)
        cookie_clicker.launch()
        cookie_clicker.select_language()
        cookie_clicker.accept_cookies()
        while True:
            if not cookie_clicker.click_big_cookie():
                cookie_clicker.click_golden_cookie()
                cookie_clicker.close_achievement_alert()
                cookie_clicker.click_big_cookie()
                cookie_clicker.buy_all_products()
            else:
                cookie_clicker.click_big_cookie()


if __name__ == "__main__":
    main()
