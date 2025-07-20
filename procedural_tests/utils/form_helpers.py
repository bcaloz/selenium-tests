import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def _assert_equal(expected, actual, message_prefix=""):
    assert (
        expected == actual
    ), f"{message_prefix}Expected: '{expected}', Actual: '{actual.strip()}'"


def _assert_not_equal(expected, actual, message_prefix=""):
    assert (
        expected != actual
    ), f"{message_prefix}Expected: '{expected}', Actual: '{actual.strip()}'"


def validate_text_input(
    driver, locator_type, locator_value, label_expected_text, value_to_type, timeout=10
):
    # Wait for and locate input
    input_elem = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((locator_type, locator_value))
    )

    # Locate corresponding label <td>
    label_elem = input_elem.find_element(By.XPATH, "./parent::td/preceding-sibling::td")

    # Validate label text
    _assert_equal(
        label_elem.text.strip(),
        label_expected_text,
        f"Label text mismatch for '{locator_value}'",
    )

    # Type into field
    input_elem.clear()
    print(f"[text_input] Typing '{value_to_type}' into '{locator_value}'")
    input_elem.send_keys(value_to_type)

    # Validate value was entered
    _assert_equal(
        input_elem.get_attribute("value"), value_to_type, "Value not properly set"
    )


def validate_pre_filled_text_input(
    driver,
    locator_type,
    locator_value,
    pre_filled_text,
    label_expected_text,
    value_to_type,
    timeout=10,
):
    # Wait for and locate input
    input_elem = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((locator_type, locator_value))
    )

    # Locate corresponding label <td>
    label_elem = input_elem.find_element(By.XPATH, "./parent::td/preceding-sibling::td")

    # Validate label text
    _assert_equal(
        label_elem.text.strip(),
        label_expected_text,
        f"Label text mismatch for '{locator_value}'",
    )

    # Validate pre-filled text
    _assert_equal(
        input_elem.get_attribute("value"), pre_filled_text, "Value not properly set"
    )

    # Append the text
    print(
        f"[pre_filled_input] Appending '{value_to_type}' to pre-filled '{pre_filled_text}' in '{locator_value}'"
    )
    input_elem.send_keys(Keys.END)
    input_elem.send_keys(value_to_type)

    # Validate value was entered
    print(f"[pre_filled_input] Final value: '{input_elem.get_attribute('value')}'")
    expected = pre_filled_text + value_to_type
    actual = input_elem.get_attribute("value")
    _assert_equal(expected, actual, f"Final value mismatch for '{locator_value}': ")


def validate_placeholder_field_text_input(
    driver,
    locator_type,
    locator_value,
    placeholder_text,
    label_expected_text,
    value_to_type,
    timeout=10,
):
    # Wait for and locate input
    input_elem = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((locator_type, locator_value))
    )

    # Locate corresponding label <td>
    label_elem = input_elem.find_element(By.XPATH, "./parent::td/preceding-sibling::td")

    # Validate label text
    _assert_equal(
        label_elem.text.strip(),
        label_expected_text,
        f"Label text mismatch for '{locator_value}'",
    )

    # Validate placeholder text
    _assert_equal(
        input_elem.get_attribute("placeholder"),
        placeholder_text,
        f"Placeholder text mismatch for '{locator_value}'",
    )

    # Enter the text
    print(
        f"[placeholder_input] Typing '{value_to_type}' into placeholder '{placeholder_text}' for '{locator_value}'"
    )
    input_elem.send_keys(value_to_type)

    # Validate value was entered
    _assert_equal(
        input_elem.get_attribute("value"), value_to_type, "Value not properly set"
    )


def validate_textarea_input(
    driver, locator_type, locator_value, label_expected_text, values_to_type, timeout=10
):
    # Wait for and locate Text Area
    textarea_elem = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((locator_type, locator_value))
    )

    # Locate corresponding label <td>
    label_elem = textarea_elem.find_element(
        By.XPATH, f"./ancestor::tr/td[contains(text(), '{label_expected_text}')]"
    )

    # Validate label text
    _assert_equal(
        label_elem.text.strip(),
        label_expected_text,
        f"Label text mismatch for '{locator_value}'",
    )

    # Validate that it's indeed a textarea
    textarea_elem.clear()
    print(
        f"[textarea_input] Typing into '{locator_value}':\n" + "\n".join(values_to_type)
    )
    textarea_elem.send_keys("\n".join(values_to_type))
    # Ensure that the textarea contains new lines
    _assert_equal(True, "\n" in textarea_elem.get_attribute("value"), "Textarea is missing newline")  # type: ignore[attr-defined]

    # Validate value was entered
    _assert_equal(
        "\n".join(values_to_type),
        textarea_elem.get_attribute("value"),
        "Value not properly set",
    )


def validate_SVG(
    driver,
    locator_type,
    locator_value,
    label_expected_text,
    stroke_color,
    fill_color,
    timeout=10,
) -> None:
    # Wait for and locate SVG element
    svg_rect = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((locator_type, locator_value))
    )

    # Locate corresponding label <td>
    label_elem = svg_rect.find_element(
        By.XPATH, f"./ancestor::tr/td[contains(text(), '{label_expected_text}')]"
    )

    # Does it have the expected style?
    _assert_equal(
        svg_rect.get_attribute("stroke"),
        stroke_color,
        f"Unexpected stroke color for '{locator_value}'",
    )
    fill_attribute = svg_rect.get_attribute("fill")
    assert fill_attribute is not None, f"'fill' attribute missing on {locator_value}"
    _assert_equal(
        fill_attribute.lower(),
        fill_color.lower(),
        f"Unexpected fill color for '{locator_value}'",
    )

    # Click it to re-trigger the animation
    svg_rect.click()
    # Capture a visual CSS property
    print(f"[SVG] Clicking on '{locator_value}' to trigger animation")
    initial_opacity = svg_rect.value_of_css_property("opacity")
    print(f"[SVG] Initial opacity: {initial_opacity}")
    time.sleep(1.0)  # Wait for the animation to run
    updated_opacity = svg_rect.value_of_css_property("opacity")
    print(f"[SVG] Updated opacity: {updated_opacity}")
    _assert_not_equal(
        initial_opacity,
        updated_opacity,
        f"Opacity did not change for '{locator_value}', indicating SVG rect animation did not run",
    )


def validate_dropdown(
    driver,
    menu_locator_type,
    menu_locator_value,
    contents_locator_type,
    contents_locator_value,
    expected_options,
    selected_option,
    timeout=10,
):
    # Wait for and locate dropdown
    dropdown_menu_elem = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((menu_locator_type, menu_locator_value))
    )
    dropdown_menu_text = dropdown_menu_elem.text.strip()

    # Hover over dropdown to trigger the dropdown menu
    ActionChains(driver).move_to_element(dropdown_menu_elem).pause(0.5).perform()

    # Wait for dropdown items to be visible
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(
            (contents_locator_type, contents_locator_value)
        )
    )

    # Validate options
    dropdown_contents_elem = driver.find_element(
        contents_locator_type, contents_locator_value
    )
    dropdown_options = [
        option.text.strip()
        for option in dropdown_contents_elem.find_elements(By.TAG_NAME, "a")
    ]
    _assert_equal(
        expected_options,
        dropdown_options,
        f"Dropdown options mismatch for '{menu_locator_value}'",
    )

    # Select the option
    print(f"[dropdown] Selecting '{selected_option}' in '{menu_locator_value}'")
    option_elem = dropdown_contents_elem.find_element(
        By.XPATH, f".//a[normalize-space(text())='{selected_option}']"
    )
    ActionChains(driver).move_to_element(option_elem).click().perform()

    # Validate header changes after making dropdown selection
    header_elem = driver.find_element(
        By.XPATH, f".//h3[text()='{selected_option} Selected']"
    )
    _assert_equal(
        header_elem.text.strip(),
        f"{selected_option} Selected",
        f"Header text mismatch after selecting '{selected_option}' in '{menu_locator_value}'",
    )

    # Validate header reverts after clicking dropdown menu again
    print(f"[dropdown] Clicking on '{dropdown_menu_text}' to reset the header")
    dropdown_menu_elem.click()
    WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h3"), "Automation Practice")
    )
    header_elem = driver.find_element(By.TAG_NAME, "h3")
    _assert_equal(
        header_elem.text.strip(),
        "Automation Practice",
        f"Header text mismatch after clicking dropdown menu '{dropdown_menu_text}'",
    )


def validate_color_elements(driver, color, timeout=10) -> None:
    # Elements to check
    elements = [
        ("myButton", f"Click Me ({color})", "text"),
        ("readOnlyText", f"The Color is {color}", "value"),
        ("pText", f"This Text is {color}", "text"),
    ]

    for elem_locator, elem_expected_text, method in elements:
        elem = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, elem_locator))
        )

        # Get actual text from correct source
        if method == "text":
            elem_actual_text = elem.text.strip()
        elif method == "value":
            value_attribute = elem.get_attribute("value")
            assert (
                value_attribute is not None
            ), f"'value' attribute missing on {elem_locator}"
            elem_actual_text = value_attribute.strip()
        else:
            raise ValueError(f"Unknown method '{method}' for element {elem_locator}")
        _assert_equal(elem_actual_text, elem_expected_text)

        style_attribute = elem.get_attribute("style")
        assert (
            style_attribute is not None
        ), f"'style' attribute missing on {elem_locator}"
        elem_actual_style = style_attribute.lower().replace(" ", "").rstrip(";")
        elem_expected_style = f"color:{color.lower()}"
        assert (
            elem_expected_style in elem_actual_style
        ), f"Style mismatch: expected '{elem_expected_style}' in '{elem_actual_style}'"


def validate_button(
    driver, locator_type, locator_value, button_text, label_expected_text, timeout=10
):
    # Wait for and locate button
    button_elem = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((locator_type, locator_value))
    )

    # Validate button text
    button_actual_text = button_elem.text.strip()
    _assert_equal(
        button_actual_text, button_text, f"Button text mismatch for '{locator_value}'"
    )

    # Validate button label text
    label_elem = button_elem.find_element(
        By.XPATH, f"./ancestor::tr/td[contains(text(), '{label_expected_text}')]"
    )
    label_actual_text = label_elem.text.strip()
    _assert_equal(
        label_actual_text,
        label_expected_text,
        f"Label text mismatch for '{locator_value}'",
    )

    # Click the button and validate that the colors and text change to purple
    print(f"[button] Clicking on '{locator_value}'")
    button_elem.click()
    validate_color_elements(driver, "Purple")

    # Click the button again and validate that the colors and text change back to green
    print(f"[button] Clicking on '{locator_value}'")
    button_elem.click()
    validate_color_elements(driver, "Green")
