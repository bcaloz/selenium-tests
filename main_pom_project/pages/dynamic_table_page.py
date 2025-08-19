from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from main_pom_project.pages.base_page import BasePage


class DynamicTablePage(BasePage):
    """
    Page Object Model for https://practice.expandtesting.com/dynamic-table

    This page shows a dynamic table of process metrics (CPU, Memory, Network, Disk).
    Below the table, a sentence reports a specific metric (e.g. Chrome's CPU).

    Columns may appear in different orders on each render.

    This class provides methods to extract table data and validate it.
    """

    URL = "https://practice.expandtesting.com/dynamic-table"
    PAGE_TITLE = (
        By.XPATH,
        "//h1[text()='Dynamic Table page for Automation Testing Practice']",
    )
    TABLE_ROWS = (By.CSS_SELECTOR, "table.table-striped tbody tr")
    SUMMARY_TEXT = (By.ID, "chrome-cpu")

    def open(self) -> None:
        print("[DynamicTablePage] Opening page")
        self.driver.get(self.URL)
        self._wait_for_element(self.PAGE_TITLE)

    def get_title_element(self) -> WebElement:
        return self._wait_for_element(self.PAGE_TITLE)

    def get_summary_text(self) -> str:
        return self._wait_for_element(self.SUMMARY_TEXT).text.strip()

    def get_all_rows(self) -> list[list[str]]:
        # Wait for at least one row to confirm table is present
        self._wait_for_element((By.CSS_SELECTOR, "table.table-striped tbody tr"))
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        return [
            [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td")]
            for row in rows
        ]

    def get_table_headers(self) -> list[str]:
        header_cells = self.driver.find_elements(
            By.CSS_SELECTOR, "table.table-striped thead th"
        )
        return [cell.text.strip().lower() for cell in header_cells]

    def get_process_row_dict(self, process_name: str) -> dict[str, str]:
        headers = self.get_table_headers()
        for row in self.get_all_rows():
            if row and row[0].lower() == process_name.lower():
                return dict(zip(headers, row))
        raise ValueError(f"Row for process '{process_name}' not found.")

    def get_chrome_cpu_from_table(self) -> str:
        row_dict = self.get_process_row_dict("chrome")
        cpu_value = row_dict.get("cpu")
        if not cpu_value:
            raise ValueError("CPU value not found in Chrome row.")
        return cpu_value.strip()
