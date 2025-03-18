from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from random import randint
from lib.utilities.modify_coordinates import modify_coordinates, km_to_miles, miles_to_km
from lib.driver_runner import driver_runner, click_driver_many_times, click_driver_randomly
import logging
from lib.file_lib import text_to_filename
from data.search_keywords import search_keywords
from lib.classes.CallService import CallService
from selenium.webdriver.common.alert import Alert
from lib.classes.DriverIterationHelper import DriverIterationHelper
from selenium.webdriver.common.action_chains import ActionChains
from services.scraping.driver.CustomDriver import CustomDriver


class RunAutomationCycle (DriverIterationHelper):

    TIME_BETWEEN_CLICKS = 2
    DRIVER_OPENED_TIMES = 0
    LIMIT_KILOMETERS = 9

    def __init__(self, browser_name: str, global_search: str, global_business_name: str, **kwargs):
        super().__init__()
        self.browser_name = browser_name
        self.url = "https://www.google.com/maps"
        self.global_search = global_search
        self.global_business_name = global_business_name
        self.cache_path = f"/home/seluser/.config/google-chrome/{text_to_filename(self.global_business_name)}"
        self.user_path = os.path.join(
            os.getcwd(), "cache", f"user-data-{text_to_filename(self.global_business_name)}")

        self.is_driver_run_successful = False

        self.driver = CustomDriver(
            set_vpn_when_open=4,
            user_data_path=self.cache_path,
            driver_opened_times=0,
            session_name=global_business_name
        )

        self.driver.execute_cdp_cmd("Browser.grantPermissions", {
            "origin": "https://www.google.com/maps",
            "permissions": ["geolocation"]
        })

    def modify_driver_coordinates(self, lat, lng):

        self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": lat,
            "longitude": lng,
            "accuracy": 10
        })

        time.sleep(1.4)
        self.driver.refresh()

    def automate(self, search):
        search_keyword = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@id='searchboxinput']"))
        )

        search_keyword.send_keys(search)
        search_keyword.send_keys(Keys.RETURN)

        search_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@aria-label='Búsqueda']"))
        )

        return self._find_element_by_scroll_iteration(search_button)

    def _scroll_iterations(self, result, name_to_search):

        results_section = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//div[@aria-label='Resultados de {result}']"))
        )

        iterations = 15
        has_scrolled = True
        while iterations >= 0:
            try:
                element_to_scroll = self.driver.find_element(
                    By.XPATH, f"//a[@aria-label='{name_to_search}']")

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center' });",
                    element_to_scroll
                )

                has_scrolled = True
                break
            except Exception:
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight;", results_section)
                except Exception:
                    has_scrolled = False
                    break

            finally:
                time.sleep(0.5)
                iterations -= 1

        if not has_scrolled:
            new_result = f"{result} {search_keywords[randint(0, len(search_keywords) - 1)]}"
            return self._scroll_iterations(
                result=new_result,
                name_to_search=name_to_search
            )

        return iterations

    def _find_element_by_scroll_iteration(self, search_button):
        for _ in range(3):

            iterations = self._scroll_iterations(
                name_to_search=self.global_business_name,
                result=self.global_search)

            if iterations > 0:
                break

            search_button.click()
            time.sleep(2)

        if iterations <= 0:

            if self.kilometers > self.LIMIT_KILOMETERS:
                return "repeat"

            return "no-repeat"

        return "continue"

    def run(self, lat, lng, search, iterations=0):

        driver_automated_successfully = False
        print("Running")
        # self.driver.maximize_window()

        self.iterations = iterations
        try:
            self.lat = lat
            self.lng = lng

            if iterations == 0:
                self.modify_driver_coordinates(
                    lat=lat,
                    lng=lng,
                    radius_in_km=self.kilometers
                )

            else:
                self.driver.remove_user_data()
                self._quit_and_start_driver()
                self.modify_driver_coordinates(
                    lat=lat,
                    lng=lng,
                    radius_in_km=self.kilometers - self.LIMIT_KILOMETERS
                )

            self.driver.get(self.url)
            super().close_cookies_alert(self.driver)

            location_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "sVuEFc"))
            )

            location_button.click()

            automation_log = self.automate(search)
            # automation_log = self.automate(search)

            if (automation_log == "no-repeat"):
                self.driver.quit_driver()
                logging.warning(
                    f"Unable to find {self.global_business_name} in {search}")
                return False

            elif (automation_log == "repeat"):
                return self.run(lat, lng, search, iterations + 1)

            elif (automation_log == "continue"):
                self.automate_business_data()
                driver_automated_successfully = True

            self.driver.quit_driver()
            return True
        except Exception as e:
            if driver_automated_successfully:
                logging.info("Automation cycle failed to close")
            else:
                logging.warning(f"Automation cycle failed: {str(e)}")
                self.driver.quit_driver()
            return self.is_driver_run_successful
