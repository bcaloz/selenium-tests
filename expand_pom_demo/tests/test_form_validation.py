import pytest
from expand_pom_demo.pages.form_validation_page import FormValidationPage
from selenium.webdriver.remote.webdriver import WebDriver

@pytest.mark.form_validation
def test_page_title_is_correct(driver: WebDriver) -> None:
    """
    Ensure that the form validation page loads correctly and the expected title is present.
    """
    page = FormValidationPage(driver)
    page.open()

    title_elem = page.get_title_element()
    expected_title = "Form Validation page for Automation Testing Practice"
    actual_title = title_elem.text.strip()
    page.assert_equal(expected_title, actual_title, "Page title mismatch: ")