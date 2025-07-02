from pom_demo.pages.landing_page import LandingPage


def test_landing_page_renders(driver):
    landing_page = LandingPage(driver)
    landing_page.open()
    assert "Demo Page" in driver.page_source


def test_landing_page_form_fields(driver):
    landing_page = LandingPage(driver)
    landing_page.open()

    landing_page.validate_text_input("Text Input Field:", "Learn Selenium")

    landing_page.validate_pre_filled_text_input(
        label_expected_text="Pre-Filled Text Field:",
        expected_prefill="Text...",
        text_to_append="- appended!"
    )

    landing_page.validate_placeholder_text_input(
        label_expected_text="Placeholder Text Field:",
        expected_placeholder_text="Placeholder Text Field",
        value_to_type="New text!"
    )

    landing_page.validate_textarea_input(
        label_expected_text="Textarea:",
        lines_of_text_to_type=["Line 1", "Line 2"]
    )

    landing_page.validate_svg_element(
        label_expected_text="HTML SVG with rect:",
        expected_stroke="teal",
        expected_fill="#4CA0A0"
    )

    landing_page.validate_dropdown_menu_selection(
        expected_options=["Link One", "Link Two", "Link Three"],
        option_to_select="Link Two"
    )

    landing_page.validate_color_change_button(
        expected_button_text="Click Me (Green)",
        expected_label_text="Button:"
    )
