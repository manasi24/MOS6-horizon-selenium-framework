#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from selenium.webdriver.common import by
import pageobject
import time

class LoginPage(pageobject.PageObject):
    _login_username_field_locator = (by.By.ID, 'id_username')
    _login_password_field_locator = (by.By.ID, 'id_password')
    _login_submit_button_locator = (by.By.CSS_SELECTOR,
                                    "button[type='submit']")
    _project_bar_locator = (by.By.CSS_SELECTOR,
     "button[data-toggle='dropdown'].btn.btn-default.btn-sm.dropdown-toggle")
    _logout_locator = (by.By.LINK_TEXT, 'Sign Out')

    def __init__(self, driver, conf):
        super(LoginPage, self).__init__(driver, conf)
        self.login_url = self.conf.dashboard.login_url
	self.project = self.conf.dashboard.project
        self._page_title = "Login"

    def is_login_page(self):
        return (self.is_the_current_page() and
                self._is_element_visible(*self._login_submit_button_locator))

    @property
    def username(self):
        return self._get_element(*self._login_username_field_locator)

    @property
    def password(self):
        return self._get_element(*self._login_password_field_locator)

    @property
    def login_button(self):
        return self._get_element(*self._login_submit_button_locator)
    
    @property
    def project_bar(self):
        return self._get_element(*self._project_bar_locator)

    @property
    def logout_button(self):
        return self._get_element(*self._logout_locator)

    def _click_on_login_button(self):
        self.login_button.click()

    def is_logout_reason_displayed(self):
        return self.driver.find_element(*self._login_logout_reason_locator)

    def login(self, user=None, password=None):
        return self._do_login(user, password, self._click_on_login_button)

    def _do_login(self, user, password, login_method):
        if password is None:
            password = self.conf.identity.password
        if user is None:
            user = self.conf.identity.username
        self.username.send_keys(user)
        self.password.send_keys(password)
        login_method()

    def go_to_login_page(self):
        self.driver.get(self.login_url)

    def select_project(self):
	self.project_bar.click()
	selector = self._get_element(by.By.XPATH,
         "//body/div[1]/div[2]/div[3]/div[2]/div[1]/div/div/div[1]/ul/li[2]/a")
	selector.click()

    def log_out(self):
	self._wait_till_element_visible(self.logout_button, 10)
