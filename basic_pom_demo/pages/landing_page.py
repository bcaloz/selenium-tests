from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class LandingPage:
    """Page Object Model for https://seleniumbase.io/demo_page"""

    URL = "https://seleniumbase.io/demo_page"
    TIMEOUT = 10

    # --- Locators ---
    PAGE_HEADER = (By.XPATH, "//h1[text()='Demo Page']")

    TEXT_INPUT = (By.ID, "myTextInput")
    TEXT_INPUT_LABEL = (
        By.XPATH,
        "//input[@id='myTextInput']/parent::td/preceding-sibling::td",
    )

    PREFILLED_TEXT_INPUT = (By.ID, "myTextInput2")
    PREFILLED_TEXT_INPUT_LABEL = (
        By.XPATH,
        "//input[@id='myTextInput2']/parent::td/preceding-sibling::td",
    )

    PLACEHOLDER_TEXT_INPUT = (By.ID, "placeholderText")
    PLACEHOLDER_TEXT_INPUT_LABEL = (
        By.XPATH,
        "//input[@id='placeholderText']/parent::td/preceding-sibling::td",
    )

    TEXTAREA_INPUT = (By.ID, "myTextarea")

    SVG_RECTANGLE = (By.ID, "svgRect")

    DROPDOWN_MENU = (By.ID, "myDropdown")
    DROPDOWN_MENU_CONTENT = (By.CLASS_NAME, "dropdown-content")

    BUTTON = (By.ID, "myButton")
    BUTTON_LABEL = (
        By.XPATH,
        "//button[@id='myButton']/ancestor::tr/td[contains(text(),'Button:')]",
    )

    READ_ONLY_INPUT = (By.ID, "readOnlyText")
    COLOR_TEXT_PARAGRAPH = (By.ID, "pText")

    # --- Functions ---
    def __init__(self, driver, timeout: int = TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _wait_for_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @staticmethod
    def _assert_equal(expected, actual, message_prefix=""):
        assert (
            expected == actual
        ), f"{message_prefix}Expected: '{expected}', Actual: '{actual.strip()}'"

    @staticmethod
    def _assert_not_equal(expected, actual, message_prefix=""):
        assert (
            expected != actual
        ), f"{message_prefix}Expected: '{expected}', Actual: '{actual.strip()}'"

    def open(self):
        self.driver.get(self.URL)
        self._wait_for_element(self.PAGE_HEADER)

    def validate_text_input(self, label_expected_text, value_to_type):
        input_elem = self._wait_for_element(self.TEXT_INPUT)
        label_elem = self._wait_for_element(self.TEXT_INPUT_LABEL)
        self._assert_equal(
            label_elem.text.strip(), label_expected_text, "Label text mismatch: "
        )
        input_elem.clear()
        input_elem.send_keys(value_to_type)
        self._assert_equal(
            input_elem.get_attribute("value"), value_to_type, "Input value mismatch: "
        )

    def validate_pre_filled_text_input(
        self, label_expected_text, expected_prefill, text_to_append
    ):
        input_elem = self._wait_for_element(self.PREFILLED_TEXT_INPUT)
        label_elem = self._wait_for_element(self.PREFILLED_TEXT_INPUT_LABEL)
        self._assert_equal(label_elem.text.strip(), label_expected_text)
        self._assert_equal(input_elem.get_attribute("value"), expected_prefill)
        input_elem.send_keys(Keys.END, text_to_append)
        self._assert_equal(
            input_elem.get_attribute("value"), expected_prefill + text_to_append
        )

    def validate_placeholder_text_input(
        self, label_expected_text, expected_placeholder_text, value_to_type
    ):
        input_elem = self._wait_for_element(self.PLACEHOLDER_TEXT_INPUT)
        label_elem = self._wait_for_element(self.PLACEHOLDER_TEXT_INPUT_LABEL)
        self._assert_equal(label_elem.text.strip(), label_expected_text)
        self._assert_equal(
            input_elem.get_attribute("placeholder"), expected_placeholder_text
        )
        input_elem.send_keys(value_to_type)
        self._assert_equal(input_elem.get_attribute("value"), value_to_type)

    def validate_textarea_input(self, label_expected_text, lines_of_text_to_type):
        textarea_elem = self._wait_for_element(self.TEXTAREA_INPUT)
        label_elem = textarea_elem.find_element(
            By.XPATH, f"./ancestor::tr/td[contains(text(), '{label_expected_text}')]"
        )
        self._assert_equal(label_elem.text.strip(), label_expected_text)
        full_text = "\n".join(lines_of_text_to_type)
        textarea_elem.clear()
        textarea_elem.send_keys(full_text)
        self._assert_equal(textarea_elem.get_attribute("value"), full_text)

    def validate_svg_element(
        self, label_expected_text, expected_stroke, expected_fill
    ) -> None:
        svg_elem = self._wait_for_element(self.SVG_RECTANGLE)
        svg_elem.find_element(
            By.XPATH, f"./ancestor::tr/td[contains(text(), '{label_expected_text}')]"
        )
        self._assert_equal(svg_elem.get_attribute("stroke"), expected_stroke)
        fill_attribute = svg_elem.get_attribute("fill")
        assert fill_attribute is not None, f"'fill' attribute missing on {svg_elem}"
        self._assert_equal(fill_attribute.lower(), expected_fill.lower())
        svg_elem.click()
        initial_opacity = svg_elem.value_of_css_property("opacity")
        ActionChains(self.driver).pause(1).perform()
        final_opacity = svg_elem.value_of_css_property("opacity")
        self._assert_not_equal(
            initial_opacity, final_opacity, "SVG opacity unchanged after click"
        )

    def validate_dropdown_menu_selection(self, expected_options, option_to_select):
        dropdown_elem = self._wait_for_element(self.DROPDOWN_MENU)
        ActionChains(self.driver).move_to_element(dropdown_elem).pause(0.5).perform()
        content_elem = self._wait_for_element(self.DROPDOWN_MENU_CONTENT)
        actual_options = [
            a.text.strip() for a in content_elem.find_elements(By.TAG_NAME, "a")
        ]
        self._assert_equal(
            actual_options, expected_options, "Dropdown options mismatch: "
        )
        content_elem.find_element(
            By.XPATH, f".//a[normalize-space()='{option_to_select}']"
        ).click()
        self._wait_for_element(
            (By.XPATH, f"//h3[text()='{option_to_select} Selected']")
        )
        dropdown_elem.click()
        self._wait_for_element((By.XPATH, "//h3[text()='Automation Practice']"))

    def validate_color_change_button(self, expected_button_text, expected_label_text):
        button_elem = self._wait_for_element(self.BUTTON)
        label_elem = self._wait_for_element(self.BUTTON_LABEL)
        self._assert_equal(button_elem.text.strip(), expected_button_text)
        self._assert_equal(label_elem.text.strip(), expected_label_text)
        for color in ("Purple", "Green"):
            button_elem.click()
            self._assert_color_feedback(color)

    def _assert_color_feedback(self, expected_color: str) -> None:
        elements = [
            (self.BUTTON, f"Click Me ({expected_color})", "text"),
            (self.READ_ONLY_INPUT, f"The Color is {expected_color}", "value"),
            (self.COLOR_TEXT_PARAGRAPH, f"This Text is {expected_color}", "text"),
        ]

        for locator, expected_text, source in elements:
            element = self._wait_for_element(locator)

            if source == "value":
                value_attr = element.get_attribute("value")
                assert value_attr is not None, f"'value' attribute missing on {locator}"
                actual_text = value_attr.strip()
            elif source == "text":
                actual_text = element.text.strip()
            else:
                raise ValueError(f"Unknown source '{source}'")

            self._assert_equal(actual_text, expected_text)

            style_attr = element.get_attribute("style")
            assert style_attr is not None, f"'style' attribute missing on {locator}"
            actual_style = style_attr.lower().replace(" ", "").rstrip(";")

            expected_style = f"color:{expected_color.lower()}"
            assert (
                expected_style in actual_style
            ), f"Style mismatch: expected '{expected_style}' in '{actual_style}'"
