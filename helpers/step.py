import re

from allure_commons._allure import StepContext

from settings import REPORTER


def step(title):
    if REPORTER == "Allure":
        if callable(title):
            title_name = re.sub(r'_+', ' ', title.__name__)
            return StepContext(title_name, {})(title)
        else:
            return StepContext(title, {})
