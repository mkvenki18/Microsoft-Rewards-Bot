import time
import logging
import ollama

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .offerquests import OfferQuests
from helper.browser import Browser
import env


class MSROffer:
    def __init__(self, browser:Browser) -> None:
        self._quests = OfferQuests(browser)
        self._browser = browser

    def do_offers(self):
        global_offers = self._goto_dashboard_get_offer_links()
        if not global_offers:
            logging.info(msg='No more global offers')
            return 0
        for card in global_offers:
            card.click()
            logging.info(msg=f'{card.aria_role + card.accessible_name}')
        return 1
    
    
    def do_daily_set(self):
        daily_set = self._goto_dashboard_get_daily_set_links()
        if not daily_set:
            logging.info(msg='No more daily set found')
            return 0
        
        for card in daily_set:
            card.click()
            logging.info(msg=f'{card.aria_role + card.accessible_name}')
        return 1
    
    def do_daily_quiz(self):
        daily_quiz = self._goto_dashboard_get_daily_quiz_links()
        if not daily_quiz:
            logging.info(msg='No daily quiz found')
            return 0
        
        for card in daily_quiz:
            card.click()
            self._do_quiz()
        return 1

    def _do_quiz(self):
        self._browser.goto_latest_window()
        logging.info(msg=f'{self._browser.current_url}')
        time.sleep(1.2)
        self._browser.wait_until_visible(By.ID, 'rqStartQuiz', 15)
        self._browser.click_element(By.ID, 'rqStartQuiz')
        for x in range(3):
            time.sleep(5)
            question = self._browser.find_element(By.CLASS_NAME, 'rqQuestion').text
            logging.info(msg='Current question: '+ question)
            options = [opt.text for opt in self._browser.find_elements(By.CLASS_NAME, 'rq_button')]
            answer = self.get_quiz_answer(question, options)
            index = ord(answer) - ord('A')
            self._browser.find_element(By.CLASS_NAME, 'rq_button')[index].click()
        self._browser.close()

    def _do_offers(self):
        daily_offers = self._goto_dashboard_get_offer_links()
        if not daily_offers:
            logging.info(msg='No more daily offers available')
    
    def _goto_dashboard_get_offer_links(self) -> list[WebElement]:
        self._browser.get(env.URL_DASHBOARD)
        time.sleep(5)
        daily_offers = self._browser.find_elements(By.XPATH, '//div[contains(@data-bi-id, "DailyGlobal") and not(contains(@data-bi-id, "Locked"))]')
        logging.info(msg=f'Global Offers: {len(daily_offers)}')
        return daily_offers
    
    def _goto_dashboard_get_daily_set_links(self) -> list[WebElement]:
        logging.info(msg='Starting Daily Set')
        self._browser.get(env.URL_DASHBOARD)
        time.sleep(5)
        daily_set = self._browser.find_elements(By.XPATH, '//div[contains(@data-bi-id, "DailySet")][not(@tabindex) or @tabindex!="-1"]')
        logging.info(msg=f'Daily Set Number: {len(daily_set)}')
        return daily_set
    
    def _goto_dashboard_get_daily_quiz_links(self) -> list[WebElement]:
        logging.info(msg='Starting Daily Quiz')
        self._browser.get(env.URL_DASHBOARD)
        time.sleep(5)
        daily_quiz = self._browser.find_elements(By.XPATH, '//div[contains(@data-bi-id, "DailySet") and contains(@data-m, "quiz")][not(@tabindex) or @tabindex!="-1"]')
        logging.info(msg=f'Daily Quiz Number: {len(daily_quiz)}')
        return daily_quiz

    def _complete_sign_in_prompt(self):
        sign_in_prompt_msg = self._browser.find_elements(By.CLASS_NAME, 'simpleSignIn')
        if not sign_in_prompt_msg:
            return
        logging.info(msg='Detected sign-in prompt')
        self._browser.wait_until_clickable(By.LINK_TEXT, 'Sign in', 15)
        self._browser.click_element(By.LINK_TEXT, 'Sign in')
        logging.info(msg='Clicked sign-in prompt')
        time.sleep(4)

    def get_quiz_answer(self, question: str, options: list[str]) -> str:
        prompt = f"""
        Question: {question}
        Options: {", ".join(options)}
        Answer ONLY with the letter of the correct option (A, B, C, etc.).
        """
        
        response = ollama.generate(
            model="llama3",  
            prompt=prompt,
            options={"temperature": 0.1}  
        )
        
        return response["response"].strip()[0].upper()