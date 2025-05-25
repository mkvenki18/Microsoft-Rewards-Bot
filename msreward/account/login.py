import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyotp

from helper.browser import Browser
from helper.utils import hide_email
from env import *

class FailToSignInException(Exception):
    pass

class MSRLogin:
    _browser: Browser
    email: str
    psw: str
    otp_secret: str

    def log_in(self):
        logging.info(msg=f'Logging in {hide_email(self.email)}...')
        self._browser.get(URL_LOGIN)
        time.sleep(2)

        self._enter_email()
        time.sleep(2)
        self._enter_password()
        if self.otp_secret:
            self._enter_otc()
        time.sleep(1)
        #self._click_i_look_good()

        #self._browser.click_element(By.XPATH, '//input[@type="submit"]', ignore_no_ele_exc=True)
        #self._browser.wait_until_visible(By.XPATH, '//*[@id="uhfLogo" or @id="microsoft"]', 10)

        #self._log_into_bing_mobile() if self._browser.mobile_mode else self._log_into_bing_pc()
        #time.sleep(1)
        #self._accept_bnp()
        time.sleep(1)
        logging.info(msg='Log In successful.')

    def _enter_email(self):
        self._browser.save_screenshot('logs/emailEntry.png')
        self.enter_login_screen_value('usernameEntry', self.email, 'Sent Email Address.')

    def _enter_password(self):
        self._browser.save_screenshot('logs/EnterPassword.png')
        #self.press_login_screen_button("span[role='button'][class*='fui-Link']", 'Click password option')
        self.enter_login_screen_value('passwordEntry', self.pswd, 'Entered Password')
        self._browser.save_screenshot('logs/staySignedIn.png')
        self.press_login_screen_button("button[data-testid='secondaryButton']", "Click 'Don't stay signed in' buttons", "CSS")
        self.press_login_screen_button("landing-page-dialog.close", "Click X Button", "ID")
        time.sleep(2)
        self._browser.save_screenshot('logs/MicrosoftLive.png')


    def _enter_otc(self):
        logging.debug(msg='OTC information is provided.')
        if not self._browser.find_elements(By.NAME, 'otc'):
            self._switch_to_otc_method()
        totp = pyotp.TOTP(self.otp_secret)
        otc = totp.now()
        self._enter_login_screen_value('otc', otc, 'Sent OTC')

    def _switch_to_otc_method(self):
        logging.debug(msg='Switching to OTC verification method.')
        sign_in_another_way = self._browser.find_elements(By.ID, 'signInAnotherWay')
        if not sign_in_another_way:
            raise FailToSignInException('Sign in is failed. Unable to switch to OTC verification method. Did not find the "sign in another way" link.')

        sign_in_another_way[0].click()
        time.sleep(1)
        verification_methods = self._browser.find_elements(By.XPATH, '//div[@data-bind="text: display"]')
        for vm in verification_methods:
            if 'mobile app' in vm.text:
                vm.click()
                break
        else:
            raise FailToSignInException(f'Sign in is failed. Unable to switch to OTC verification method. No such option. All options are:\n{[x.text for x in verification_methods]}')

    def enter_login_screen_value(self, ele_name, value, msg):
        self._browser.wait_until_visible(By.ID, ele_name, 10)
        self._browser.send_key(By.ID, ele_name, value)
        logging.debug(msg=msg)
        time.sleep(0.5)
        self._browser.send_key(By.ID, ele_name, Keys.RETURN)
        time.sleep(0.5)
    
    def press_login_screen_button(self, ele_name, msg, type):
        if type == "CSS":
            self._browser.wait_until_visible(By.CSS_SELECTOR, ele_name, 10)
            self._browser.click_element(By.CSS_SELECTOR, ele_name)
            logging.debug(msg=msg)
            time.sleep(0.5)
        else:
            self._browser.wait_until_visible(By.ID, ele_name, 15)
            self._browser.click_element(By.ID, ele_name)
            logging.debug(msg=msg)
            time.sleep(0.5)
    

    def sign_in_prompt(self):
        time.sleep(3)
        if self._browser.find_elements(By.CLASS_NAME, 'simpleSignIn'):
            logging.debug(msg='Detected sign-in prompt')
            self._browser.wait_until_visible(By.LINK_TEXT, 'Sign in', 15)
            self._browser.click_element(By.LINK_TEXT, 'Sign in')
            logging.info(msg='Clicked sign-in prompt')
            time.sleep(4)

    def _log_into_bing_pc(self):
        self._browser.get(URL_BING_SEARCH)
        self._browser.wait_until_clickable(By.ID, 'id_l', 5)
        self._browser.click_element(By.ID, 'id_l')
        time.sleep(0.1)
        self._browser.wait_until_clickable(By.ID, 'id_l', 5)
        self._browser.save_screenshot('logs/bing.png')

    def _log_into_bing_mobile(self):
        self._browser.get(URL_BING_SEARCH)
        self._browser.wait_until_clickable(By.XPATH, '//*[@aria-label="Preferences"]', 10)
        self._browser.click_element(By.XPATH, '//*[@aria-label="Preferences"]', ignore_no_ele_exc=True)
        time.sleep(0.1)
        self._browser.wait_until_clickable(By.XPATH, "//*[text()='Sign in']//parent::a", 5)
        if self._browser.click_element(By.XPATH, "//*[text()='Sign in']//parent::a", ignore_no_ele_exc=True):
            self._browser.wait_until_clickable(By.XPATH, '//*[@aria-label="Preferences"]', 5)
        else:
            self._browser.click_element(By.XPATH, '//*[@aria-label="Preferences"]', ignore_no_ele_exc=True)

    def _accept_bnp(self):
        self._browser.click_element(By.CLASS_NAME, 'bnp_btn_accept', ignore_no_ele_exc=True)

    def _click_i_look_good(self):
        self._browser.click_element(By.ID, 'iLooksGood', ignore_no_ele_exc=True)
    