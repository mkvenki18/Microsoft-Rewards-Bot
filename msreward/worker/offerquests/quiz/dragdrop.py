import logging
import random
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from ..offerquestbase import OfferQuestBase


class DragDropQuiz(OfferQuestBase):
    def __init__(self, browser):
        super().__init__(browser, 'Drag&Drop Quiz', 'rqAnswerOptionNum0', By.ID)

    def _do_quest(self):
        for _ in range(100):
            if self._browser.find_elements(By.ID, 'quizCompleteContainer'):
                break
            drag_options = self._get_options_for_drag_drop()
            if not drag_options:
                continue
            try:
                choice_a = random.choice(drag_options)
                drag_options.remove(choice_a)
                choice_b = random.choice(drag_options)
                ActionChains(self._browser).drag_and_drop(choice_a, choice_b).perform()
            except (WebDriverException, TypeError):
                logging.debug(msg='Unknown Error.')
                continue
            time.sleep(1)

    def _get_options_for_drag_drop(self):
        drag_options = self._browser.find_elements(By.CLASS_NAME, 'rqOption')
        right_answers = self._browser.find_elements(By.CLASS_NAME, 'correctAnswer')
        if right_answers:
            drag_options = [x for x in drag_options if x not in right_answers]
        return drag_options