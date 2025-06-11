from time import sleep

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class TestRunner:
    def __init__(self, app_id: str, driver: WebDriver):
        self.app_id = app_id
        self.driver = driver

    def _start_app(self) -> None:
        print("Tripadvisor app is starting!")
        self.driver.activate_app(self.app_id)

    def _close_app(self) -> None:
        print("Tripadvisor app is closing!")
        self.driver.terminate_app(self.app_id)
        self.driver.quit()

    def _process_result(self, result: WebElement, index: int) -> dict[str, str | int]:
        result_dict: dict[str, str | int] = {
            "index": index,
            "type": result.find_element(
                by=AppiumBy.XPATH,
                value="//*[@resource-id='com.tripadvisor.tripadvisor:id/labelContainer']['value']",
            )
            .find_element(by=AppiumBy.CLASS_NAME, value="android.widget.TextView")
            .text,
            "name": result.find_element(
                by=AppiumBy.XPATH,
                value="//*[@resource-id='com.tripadvisor.tripadvisor:id/txtTitle']",
            ).text,
            "location": result.find_element(
                by=AppiumBy.XPATH,
                value="//*[@resource-id='com.tripadvisor.tripadvisor:id/txtPrimaryInfo']",
            ).text,
        }
        return result_dict

    def _swipe_up_results(self) -> None:
        """
        Swipes up from the first hotel card up to top result
        """
        top_result = self.driver.find_element(
            # by=AppiumBy.ID, value="com.tripadvisor.tripadvisor:id/circularBtnHeart"
            by=AppiumBy.XPATH,
            value="//*[@text='Top result']",
        )
        print(top_result.text)
        all_results = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@text='All results']",
        )
        print(all_results.text)

        self.driver.swipe(
            start_x=all_results.location["x"],
            start_y=all_results.location["y"],
            end_x=top_result.location["x"],
            end_y=top_result.location["y"],
            duration=1000,
        )

    def _get_all_results(self) -> list[WebElement]:
        all_results = self.driver.find_elements(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/item']['value']",
        )

        results_list: list[dict[str, str | int] | None] = []

        for result in all_results:
            index: int = len(results_list) + 1
            processed_data = self._process_result(result, index)
            results_list.append(processed_data)

        return results_list

    def _process_name(self, name: str) -> list[str]:
        name_list: list[str] = name.split(" ")
        whitespace_count: int = name_list.count("")

        if whitespace_count:
            for _ in range(whitespace_count):
                name_list.remove("")

        return name_list

    def _check_results(
        self, results: list[dict[str, str | int]], hotel_name: str
    ) -> list[dict[str, str | int]]:
        success_type: str = "HOTEL"
        hotel_name_list = self._process_name(hotel_name)

        success_list: list[dict[str, str | int] | None] = []

        for result in results:
            result_name_list = self._process_name(result["name"])
            if result_name_list == hotel_name_list and success_type == result["type"]:
                success_list.append(result)

        return success_list

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

    def search_hotel(self, hotel_name: str) -> None:
        self._start_app()
        sleep(5)

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
        search_field.send_keys(hotel_name)
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

        result_list = self._get_all_results()

        succsess = self._check_results(result_list, hotel_name)
        print(succsess)
        print(succsess[0]["index"])

        hotel = self.driver.find_element(
            by=AppiumBy.XPATH,
            value=f"//*[@resource-id='com.tripadvisor.tripadvisor:id/item']['{succsess[0]['index']}']",
        )
        print(hotel)

        hotel.click()

    def _swipe_up_month(self) -> None:
        top_month = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/monthView']['1']",
        )
        bottom_month = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/monthView']['2']",
        )

        self.driver.swipe(
            start_x=bottom_month.location["x"],
            start_y=bottom_month.location["y"],
            end_x=top_month.location["x"],
            end_y=top_month.location["y"],
            duration=1000,
        )

    def _check_month(self, month: str) -> None:
        view_month = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/txtTitle']",
        ).text
        view_month = view_month.split(" ")
        view_month = view_month[0]
        print(view_month)

        if view_month == month:
            return None

        while view_month != month:
            self._swipe_up_month()
            sleep(1)

    def _set_date(self, date: list[str]) -> None:
        date_field = self.driver.find_element(
            by=AppiumBy.ID, value="com.tripadvisor.tripadvisor:id/hotelInfoInputField"
        )
        date_field.click()
        sleep(2)

        start_month = date[0].split(" ")[0]
        print(start_month)
        start_date = date[0].split(" ")[1]
        print(start_date)

        end_month = date[1].split(" ")[0]
        print(end_month)
        end_date = date[1].split(" ")[1]
        print(end_date)

        # self._check_month(start_month)
        select_start_date = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/monthView']['value']",
        ).find_element(by=AppiumBy.XPATH, value=f"//*[@text='{start_date}']")

        print(select_start_date.text)
        select_start_date.click()
        # sleep(2)

        self._check_month(end_month)
        select_end_date = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/monthView']['value']",
        ).find_element(by=AppiumBy.XPATH, value=f"//*[@text='{end_date}']")

        select_end_date.click()
        # sleep(2)

        apply_btn = self.driver.find_element(
            by=AppiumBy.ID, value="com.tripadvisor.tripadvisor:id/btnPrimary"
        )
        apply_btn.click()

    def _take_screenshot(self, date: list[str], hotel_name: str) -> str:
        hotel_name_list = self._process_name(hotel_name)
        hotel_name: str = "_".join(hotel_name_list)
        booking_date: list[list[str]] = [d.split(" ") for d in date]
        screenshot_name: str = f"tripadvisor_{hotel_name}_{booking_date[0][0]}_{booking_date[0][1]}-{booking_date[1][0]}_{booking_date[1][1]}"
        screenshot = self.driver.save_screenshot(f"./screenshots/{screenshot_name}.png")

        if not screenshot:
            print("Can't take screenshot")
        return screenshot_name

    def _get_book_data(self, date: list[str], hotel_name: str) -> None:
        self._set_date(date)
        sleep(12)  # Let the app load prices

        main_vendor_name: str = "Tripadvisor"
        print(main_vendor_name)

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
            print(parner_vendor_name)

            parner_vendor_price = (
                partner_vendor.find_element(
                    by=AppiumBy.CLASS_NAME,
                    value="G1.v",
                )
                .find_element(by=AppiumBy.CLASS_NAME, value="android.widget.TextView")
                .text
            )
            print(parner_vendor_price)

        date_str: str = " - ".join(date)
        screenshot_name = self._take_screenshot(date, hotel_name)
        data: dict[str, str] = {
            date_str: {
                # main_vendor_name: main_vendor_price,
                # parner_vendor_name: parner_vendor_price,
                # "screenshot": screenshot_name,
            }
        }

        if main_vendor_name and main_vendor_price:
            data[date_str].update({main_vendor_name: main_vendor_price})

        if partner_vendor:
            data[date_str].update({parner_vendor_name: parner_vendor_price})

        if screenshot_name:
            data[date_str].update({"screenshot": screenshot_name})

        return data

    def collect_data(self, date_list: list[list[str]]) -> None:
        hotel_name = self.driver.find_element(
            by=AppiumBy.XPATH,
            value="//*[@resource-id='com.tripadvisor.tripadvisor:id/txtTitle']",
        ).text
        print(hotel_name)

        self._swipe_up_booking()
        # sleep(2)

        data = {hotel_name: {}}
        for date in date_list:
            booking_data = self._get_book_data(date, hotel_name)
            data[hotel_name].update(booking_data)

        print(data)
        # self._close_app()
