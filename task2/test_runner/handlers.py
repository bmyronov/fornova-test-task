import logging
from time import sleep

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from schemas import SearchResult

# Create a logger for this module
logger = logging.getLogger(__name__)


class TestRunner:
    __test__ = False

    def __init__(self, app_id: str, driver: WebDriver, hotel_name: str):
        self.app_id = app_id
        self.driver = driver
        self.hotel_name = hotel_name

    def _swipe_up_results(self) -> None:
        """
        Swipes up from the first hotel card up to top result

        ``TODO: Change swipe function``
        """
        top = self.driver.find_element(
            # by=AppiumBy.ID, value="com.tripadvisor.tripadvisor:id/circularBtnHeart"
            by=AppiumBy.XPATH,
            # value="//*[@resource-id='com.tripadvisor.tripadvisor:id/rvTypeaheadResults']/android.view.View[1]",
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/ratingsScore']",
        )

        bottom = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@text='All results']",
        )

        self.driver.swipe(
            start_x=bottom.location["x"],
            start_y=bottom.location["y"],
            end_x=top.location["x"],
            end_y=top.location["y"],
            duration=900,
        )
        logger.info("Swiped up the results")

    def _swipe_up_booking(self) -> None:
        """
        Swipes up to clearly see booking date, price and providers
        """
        top = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/composeView'][1]",
        )
        bottom = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/rvContent']/android.view.ViewGroup[2]",
        )

        self.driver.swipe(
            start_x=bottom.location["x"],
            start_y=bottom.location["y"],
            end_x=top.location["x"],
            end_y=top.location["y"],
            duration=1000,
        )

    def _process_name(self, name: str) -> list[str]:
        """
        Receives name as ``str`` transforms it into a list.
        It removes all the whitespaces.

        Returns ``list[str]``
        """
        name_list = name.split(" ")
        whitespace_count = name_list.count("")

        if whitespace_count:
            for _ in range(whitespace_count):
                name_list.remove("")

        logger.info(f"{name} has been processed. Result: {name_list}")
        return name_list

    def _collect_search_results(self, result: WebElement, index: int) -> SearchResult:
        """
        Gathers basic data from the search result.

        ``index: int`` - position of the element.
        E.g. XPATH value="//*[@resource-id='com.tripadvisor.tripadvisor:id/labelContainer']['value']"
        ['value'] is the position of the element or its index

        ``type: str`` - name of the filter e.g. 'HOTEL' or 'RESTAURANT'

        ``name: str`` - name of the establishment
        """
        search_result = SearchResult(
            index=index,
            type=result.find_element(
                by=AppiumBy.XPATH,
                value="//*[@resource-id='com.tripadvisor.tripadvisor:id/labelContainer']['value']",
            )
            .find_element(by=AppiumBy.CLASS_NAME, value="android.widget.TextView")
            .text,
            name=result.find_element(
                by=AppiumBy.XPATH,
                value="//*[@resource-id='com.tripadvisor.tripadvisor:id/txtTitle']",
            ).text,
        )

        return search_result

    def _get_results(self) -> list[SearchResult]:
        """
        Gathers info from search results.

        Returns ``list[SearchResult]``
        """
        results = self.driver.find_elements(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/item']['value']",
        )
        if len(results) > 3:
            for _ in range(len(results) - 3):
                results.pop()

        results_list: list[SearchResult] = []
        for result in results:
            index: int = len(results_list) + 1
            processed_data = self._collect_search_results(result, index)
            results_list.append(processed_data)

        logger.info(results_list)
        return results_list

    def _process_results(
        self, results: list[SearchResult]
    ) -> list[SearchResult] | None:
        """
        Processes the result. It checks if there are any successful result in the list of results.

        A successful result:

        ``type`` = "HOTEL".

        ``name`` = the same as the name of the hotel was searched for.

        Returns list[SearchResult] | None
        """
        success_type: str = "HOTEL"
        hotel_name_list = self._process_name(self.hotel_name)

        success_list: list[SearchResult] = []

        for result in results:
            result_name_list = self._process_name(result.name)
            if result_name_list == hotel_name_list and success_type == result.type:
                success_list.append(result)

        logger.info(success_list)
        return success_list

    def _set_date(self, date: list[str]) -> None:
        """
        Sets the date.

        Date ``list[str]``:

        ``start_date``

        ``end_date``
        """
        date_field = self.driver.find_element(
            by=AppiumBy.ID, value="com.tripadvisor.tripadvisor:id/hotelInfoInputField"
        )
        date_field.click()
        sleep(2)

        # start_month = date[0].split(" ")[0]
        start_date = date[0].split(" ")[1]
        # end_month = date[1].split(" ")[0]
        end_date = date[1].split(" ")[1]

        select_start_date = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/monthView']['value']",
        ).find_element(by=AppiumBy.XPATH, value=f"//*[@text='{start_date}']")
        select_start_date.click()
        logger.info(f"Selected start_date as {select_start_date.text}")
        # sleep(2)

        # self._check_month(end_month)
        select_end_date = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/monthView']['value']",
        ).find_element(by=AppiumBy.XPATH, value=f"//*[@text='{end_date}']")
        select_end_date.click()
        logger.info(f"Selected end_date as {select_end_date.text}")
        # sleep(2)

        apply_btn = self.driver.find_element(
            by=AppiumBy.ID, value="com.tripadvisor.tripadvisor:id/btnPrimary"
        )
        apply_btn.click()
        logger.info("Pressed apply_btn")

    def _take_screenshot(self, date: list[str]) -> str:
        """
        Takes screenshot of the hotel booking activity.

        Returns ``screenshot_name: str``
        """
        hotel_name_list = self._process_name(self.hotel_name)
        hotel_name: str = "_".join(hotel_name_list)
        booking_date: list[list[str]] = [d.split(" ") for d in date]
        screenshot_name: str = f"tripadvisor_{hotel_name}_{booking_date[0][0]}_{booking_date[0][1]}-{booking_date[1][0]}_{booking_date[1][1]}.png"
        screenshot = self.driver.save_screenshot(f"./screenshots/{screenshot_name}")

        if not screenshot:
            logger.error("Can't take screenshot")

        logger.info(f"Screenshot has been taken. Screenshot_name: {screenshot_name}")
        return screenshot_name

    def _get_booking_data(self, date: list[str]) -> dict[dict[str, str]]:
        self._set_date(date)
        sleep(12)  # Let the app load prices

        main_vendor_name: str = "Tripadvisor"

        try:
            main_vendor_price = (
                self.driver.find_element(
                    by=AppiumBy.XPATH,
                    value="//*[@resource-id='Hotel_Meta_Hybrid_Commerce-offers-CollapsibleContainer-0-VerticalStack-2-HorizontalStack-2-VerticalStack-0-HorizontalStack']",
                )
                .find_element(by=AppiumBy.CLASS_NAME, value="G1.v")
                .find_element(by=AppiumBy.CLASS_NAME, value="android.widget.TextView")
                .text
            )
        except NoSuchElementException:
            main_vendor_price = None

        try:
            partner_vendor = self.driver.find_element(
                by=AppiumBy.XPATH,
                value="//*[@resource-id='Hotel_Meta_Hybrid_Commerce-offers-CollapsibleContainer-4-VerticalStack-0-HorizontalStack']",
            )
        except NoSuchElementException:
            partner_vendor = None

        if not partner_vendor:
            try:
                partner_vendor = self.driver.find_element(
                    by=AppiumBy.XPATH,
                    value="//*[@resource-id='Hotel_Meta_Hybrid_Commerce-offers-CollapsibleContainer-0-VerticalStack-0-HorizontalStack']",
                )
            except NoSuchElementException:
                partner_vendor = None

        if partner_vendor:
            parner_vendor_name = partner_vendor.find_element(
                by=AppiumBy.XPATH,
                value="//*[@content-desc='Booking.com']",
            ).tag_name
            logger.info(f"Parnter_vendor_name: {parner_vendor_name}")

            parner_vendor_price = (
                partner_vendor.find_element(
                    by=AppiumBy.CLASS_NAME,
                    value="G1.v",
                )
                .find_element(by=AppiumBy.CLASS_NAME, value="android.widget.TextView")
                .text
            )
            logger.info(f"Parner_vendor_price: {parner_vendor_price}")

        date_str: str = " - ".join(date)
        screenshot_name = self._take_screenshot(date)
        data: dict[str, dict[str, str]] = {date_str: {}}

        if main_vendor_name and main_vendor_price:
            data[date_str].update({main_vendor_name: main_vendor_price})

        if partner_vendor:
            data[date_str].update({parner_vendor_name: parner_vendor_price})

        if screenshot_name:
            data[date_str].update({"screenshot": screenshot_name})

        return data

    def start_app(self) -> None:
        """
        Starts the app by app_id. App_id is specified in .env file
        """
        logger.info("The app is starting!")
        self.driver.activate_app(self.app_id)

    def close_app(self) -> None:
        """
        Closes the app after all manipulations.
        """
        logger.info("The app is closing!")
        self.driver.terminate_app(self.app_id)
        self.driver.quit()

    def search_hotel(self) -> None:
        """ """
        search_field = self.driver.find_element(
            by=AppiumBy.ID,
            value="com.tripadvisor.tripadvisor:id/edtSearchString",
        )
        search_field.click()  # select search field
        sleep(2)

        search_field = self.driver.find_element(
            by=AppiumBy.ID,
            value="com.tripadvisor.tripadvisor:id/edtSearchString",
        )
        search_field.send_keys(self.hotel_name)
        sleep(2)
        self.driver.press_keycode(AndroidKey.ENTER)
        sleep(1)

        hotel_filter = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@text='Hotels']",
        )
        hotel_filter.click()
        sleep(2)

        # Swipe up
        self._swipe_up_results()
        sleep(2)

        result_list = self._get_results()

        succsess = self._process_results(result_list)
        logger.info(f"Succsessful results: {succsess}")

        hotel = self.driver.find_element(
            by=AppiumBy.XPATH,
            value=f"//*[@resource-id='com.tripadvisor.tripadvisor:id/item']['{succsess[0].index}']",
        )
        hotel.click()
        sleep(5)

    def collect_data(self, date_list: list[list[str]]) -> dict[str, dict[str, str]]:
        hotel_name = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/txtTitle']",
        ).text

        self._swipe_up_booking()

        data: dict[str, dict[str, str]] = {hotel_name: {}}
        for date in date_list:
            booking_data = self._get_booking_data(date)
            data[hotel_name].update(booking_data)

        logger.info(data)
        return data
