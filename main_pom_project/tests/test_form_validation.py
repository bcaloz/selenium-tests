import pytest
from main_pom_project.pages.form_validation_page import FormValidationPage
from selenium.webdriver.remote.webdriver import WebDriver

@pytest.mark.form_validation
def test_page_title_is_correct(driver: WebDriver) -> None:
    """
    Ensure that the form validation page loads correctly and the expected title is present.
    Skipping placeholder/default field text checks — low-impact, brittle, and not core to test value.
    """
    page = FormValidationPage(driver)
    page.open()

    title_elem = page.get_title_element()
    expected_title = "Form Validation page for Automation Testing Practice"
    actual_title = title_elem.text.strip()
    page.assert_equal(expected_title, actual_title, "Page title mismatch: ")

@pytest.mark.form_validation
@pytest.mark.smoke
def test_valid_form_submission_redirects(driver: WebDriver) -> None:
    """Happy path - complete form, click Register, and validate user is redirected to form confirmation page with positive acknowledgment message."""
    page = FormValidationPage(driver)
    page.open()

    page.fill_form(
        name="Brian QA",
        phone="345-6789190",
        date="07-16-2025",
        payment_method="card"
    )
    page.click_register_button()

    # Assert user is redirected to confirmation page after clicking Register
    expected_url = "https://practice.expandtesting.com/form-confirmation"
    page.assert_equal(expected_url, driver.current_url, "URL mismatch: ")

    # Assert confirmation message is correct
    expected_msg = "Thank you for validating your ticket"
    actual_msg = page.get_confirmation_message()
    # Use startswith() because web ads are shown on live page which causes some random additional text to appear at the end
    page.assert_startswith(expected_msg, actual_msg, "Confirmation msg mismatch: ")

@pytest.mark.form_validation
def test_blank_form_submission_shows_errors(driver: WebDriver) -> None:
    """Click Register with all fields blank and validate error messages for each."""
    page = FormValidationPage(driver)
    page.open()

    expected_name_error_msg = "Please enter your Contact name."
    expected_number_error_msg = "Please provide your Contact number."
    expected_date_error_msg = "Please provide valid Date."
    expected_payment_method_error_msg = "Please select the Paymeny Method."

    # Page starts with pre-filled text in Contact Name field. Clear to trigger error msg.
    page.clear_name_field()
    page.click_register_button()
    actual_name_error_msg = page.get_name_error_msg()
    actual_phone_error_msg = page.get_phone_error_msg()
    actual_date_error_msg = page.get_date_error_msg()
    actual_payment_method_error_msg = page.get_payment_error_msg()

    page.assert_equal(expected_name_error_msg, actual_name_error_msg, "Name field error message mismatch: ")
    page.assert_equal(expected_number_error_msg, actual_phone_error_msg, "Phone field error message mismatch: ")
    page.assert_equal(expected_date_error_msg, actual_date_error_msg, "Date field error message mismatch: ")
    page.assert_equal(expected_payment_method_error_msg, actual_payment_method_error_msg, "Payment method field error message mismatch: ")

@pytest.mark.form_validation
def test_field_validation_feedback(driver: WebDriver) -> None:
    """
    Trigger validation errors, then fill out one field at a time with valid input and verify they show success indicators.
    
    - Name field should display positive acknowledgment text.
    - Contact number, PickUp Date, and Payment Method should display green checkmarks with no accompanying text.
    """
    page = FormValidationPage(driver)
    page.open()

    # Page starts with pre-filled texct in Contact Name field. Clear to trigger error msg.
    page.clear_name_field()
    page.click_register_button()

    # Now fill out form fields and validate success indicators appear
    page.fill_form(
        name="Brian QA",
        phone="345-6789190",
        date="07-16-2025",
        payment_method="card"
    )

    expected_name_success_msg = "Looks good!"
    actual_name_success_msg = page.get_name_success_msg()
    page.assert_equal(expected_name_success_msg, actual_name_success_msg, "Name field success message mismatch: ")
    page.assert_equal(True, page.get_phone_success_indicator(), "Phone field should suppress error message: ")
    page.assert_equal(True, page.get_date_success_indicator(), "Date field should suppress error message: ")
    page.assert_equal(True, page.get_payment_success_indicator(), "Payment method field should suppress error message: ")