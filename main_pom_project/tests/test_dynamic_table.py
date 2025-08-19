import pytest
from main_pom_project.pages.dynamic_table_page import DynamicTablePage
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.mark.dynamic_table
def test_page_title_is_correct(driver: WebDriver) -> None:
    """
    Ensure that the dynamic table page loads correctly and the
    expected title is present.
    """
    page = DynamicTablePage(driver)
    page.open()

    title_elem = page.get_title_element()
    expected_title = "Dynamic Table page for Automation Testing Practice"
    actual_title = title_elem.text.strip()
    page.assert_equal(expected_title, actual_title, "Page title mismatch: ")


@pytest.mark.dynamic_table
@pytest.mark.smoke
def test_chrome_cpu_label_matches_table(driver: WebDriver) -> None:
    """
    Extract Chrome CPU value from table and confirm it matches the summary label below.
    """
    page = DynamicTablePage(driver)
    page.open()

    chrome_cpu_from_table = page.get_chrome_cpu_from_table()
    summary_text = page.get_summary_text()

    # Expect summary format like: "Chrome CPU: 33%"
    expected_fragment = f"Chrome CPU: {chrome_cpu_from_table}"
    page.assert_in(
        expected_fragment,
        summary_text,
        "Mismatch between summary text and Chrome row CPU value: ",
    )


# fix this
@pytest.mark.dynamic_table
def test_dynamic_table_has_valid_structure(driver: WebDriver) -> None:
    """
    Validate each row has 5 columns (Process, CPU, Network, Disk, Memory)
    and that all metrics (except Process) are percent strings.
    """
    page = DynamicTablePage(driver)
    page.open()

    all_rows = page.get_all_rows()
    for row in all_rows:
        page.assert_equal(5, len(row), f"Row should have 5 columns: {row}")

        for value in row[1:]:  # Skip first column (Process name)
            is_percent = (
                value.endswith("%") and value[:-1].replace(".", "", 1).isdigit()
            )
            page.assert_equal(
                True,
                is_percent,
                f"Metric column should be a percentage value, got: {value}",
            )
