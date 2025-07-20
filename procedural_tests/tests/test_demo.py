from procedural_tests.utils import form_helpers
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_landing_page(driver):
    driver.get("https://seleniumbase.io/demo_page")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//title[text()='Web Testing Page']"))
    )

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[text()='Demo Page']"))
    )

    assert "Demo Page" in driver.page_source


def test_validate_form_fields(driver):
    driver.get("https://seleniumbase.io/demo_page")

    form_helpers.validate_text_input(
        driver,
        locator_type=By.ID,
        locator_value="myTextInput",
        label_expected_text="Text Input Field:",
        value_to_type="Learn Selenium",
    )

    form_helpers.validate_pre_filled_text_input(
        driver,
        locator_type=By.ID,
        locator_value="myTextInput2",
        pre_filled_text="Text...",
        label_expected_text="Pre-Filled Text Field:",
        value_to_type="- appended!",
    )

    form_helpers.validate_placeholder_field_text_input(
        driver,
        locator_type=By.ID,
        locator_value="placeholderText",
        placeholder_text="Placeholder Text Field",
        label_expected_text="Placeholder Text Field:",
        value_to_type="New text!",
    )

    form_helpers.validate_textarea_input(
        driver,
        locator_type=By.ID,
        locator_value="myTextarea",
        label_expected_text="Textarea:",
        values_to_type=["Line 1", "Line 2"],
    )

    form_helpers.validate_SVG(
        driver,
        locator_type=By.ID,
        locator_value="svgRect",
        label_expected_text="HTML SVG with rect:",
        stroke_color="teal",
        fill_color="#4CA0A0",
    )

    form_helpers.validate_dropdown(
        driver,
        menu_locator_type=By.ID,
        menu_locator_value="myDropdown",
        contents_locator_type=By.CLASS_NAME,
        contents_locator_value="dropdown-content",
        expected_options=["Link One", "Link Two", "Link Three"],
        selected_option="Link Two",
    )

    form_helpers.validate_button(
        driver,
        locator_type=By.ID,
        locator_value="myButton",
        button_text="Click Me (Green)",
        label_expected_text="Button:",
    )
