import asyncio
from playwright.async_api import Locator


async def wait_until_clickable(locator: Locator, timeout: int = 30000):
    start_time = asyncio.get_event_loop().time()

    while True:
        try:
            # Check if the element is visible and stable
            await locator.wait_for(state="visible", timeout=1000)
            # Additional stability check
            await locator.wait_for(state="attached", timeout=1000)
            # Custom check to see if the element is enabled
            if await locator.is_enabled():
                break
        except Exception as e:
            pass

        # Timeout check
        if asyncio.get_event_loop().time() - start_time > timeout / 1000:
            raise TimeoutError(f"Timeout waiting for element to be clickable after {timeout}ms")

        await asyncio.sleep(0.1)  # Small sleep to prevent tight loop

    return locator


async def handle_popup(page, title="Don't show me again", timeout: int = 5000):
    try:
        if await page.get_by_role("button", name=title).is_visible(timeout=timeout):
            await page.get_by_role("button", name=title).click(force=True)
        else:
            print("No popup to handle!")
    except Exception as e:
        print(f"Timeout or error while handling popup with title '{title}': {str(e)}")

    return page


async def click_element(page, selector: str, timeout: int = 5000):
    try:
        await asyncio.sleep(1)
        await page.locator(selector).first.click(timeout=timeout, force=True)
    except Exception as e:
        print(f"Error while trying to click the element '{selector}': {str(e)}")


async def click_text(page, text: str, exact: bool = True, timeout: int = 5000):
    try:
        print(f"Clicking: {text}")
        await asyncio.sleep(1)
        await page.get_by_text(text, exact=exact).click(timeout=timeout, force=True)
    except Exception as e:
        print(f"Error while trying to click the text '{text}': {str(e)}")
        raise Exception(f"Error while trying to click the text '{text}': {str(e)}")


async def click_role(page, role: str, name: str = None, timeout: int = 5000):
    try:
        print(f"Clicking: {role}-{name}")
        await asyncio.sleep(1)
        if name:
            await page.get_by_role(role, name=name, exact=True).click(timeout=timeout, force=True)
        else:
            await page.get_by_role(role, exact=True).click(timeout=timeout, force=True)
    except Exception as e:
        print(f"Error while trying to click the role '{role}' with name '{name}': {str(e)}")
        raise Exception(f"Error while trying to click the text '{name}': {str(e)}")


async def click_label(page, label: str, timeout: int = 5000):
    try:
        print(f"Clicking: {label}")
        await asyncio.sleep(1)
        await page.get_by_label(label).click(timeout=timeout, force=True)
    except Exception as e:
        print(f"Error while trying to click the label '{label}': {str(e)}")
        raise Exception(f"Error while trying to click the text '{label}': {str(e)}")


async def uncheck_checkbox(page, selector: str, timeout: int = 5000):
    try:
        print(f"unchecking: {selector}")
        await asyncio.sleep(1)
        await page.locator(selector).uncheck(timeout=timeout)
    except Exception as e:
        print(f"Error while trying to uncheck the checkbox '{selector}': {str(e)}")
        raise Exception(f"Error while trying to click the text '{selector}': {str(e)}")


async def check_checkbox(page, selector: str, timeout: int = 5000):
    try:
        print(f"checking: {selector}")
        await asyncio.sleep(1)
        await page.locator(selector).check(timeout=timeout)
    except Exception as e:
        print(f"Error while trying to check the checkbox '{selector}': {str(e)}")
        raise Exception(f"Error while trying to click the text '{selector}': {str(e)}")


async def get_column_index(headers, column_name):
    header_count = await headers.count()
    column_index = -1
    for i in range(header_count):
        header_text = await headers.nth(i).text_content()
        if header_text.strip() == column_name:
            column_index = i + 1  # nth-child is 1-based index, so we add 1
            break

    return column_index


async def get_column_cell_value_by_other_column_cell_value(page, tbl_locator=".ant-table", get_value_in_column='', find_by={"column_name":'', "value":''}):
    # Locate the table
    table_locator = page.locator(tbl_locator)

    await asyncio.sleep(2)

    # Get the header row
    header_locator = table_locator.locator("thead tr")

    # Find the column index based on the column name
    headers = header_locator.locator("th")

    value_column_index = await get_column_index(headers, get_value_in_column)

    if value_column_index == -1:
        raise Exception(f"Column '{get_value_in_column}' not found.")


    find_by_column = find_by["column_name"]
    find_by_value = find_by["value"]

    find_by_column_index = await get_column_index(headers, find_by_column)

    # Get the table body rows
    rows = table_locator.locator("tbody tr")
    row_count = await rows.count()

    # Iterate through the rows to find the one with the matching report name
    for row_index in range(row_count):
        # Extract the report name from the first column (or adjust the column if report name is elsewhere)
        current_value = await rows.nth(row_index).locator(f"td:nth-child({find_by_column_index})").text_content()

        # Check if the report name matches the target report name
        if current_value.strip() == find_by_value:
            # Get the cell value from the desired column
            cell_value = await rows.nth(row_index).locator(f"td:nth-child({value_column_index})").text_content()
            return cell_value

    # If no matching report is found, return None or raise an exception
    return None


async def screen_capture(page, testname: str, filename: str):
    try:
        path = f"screenshots/{testname}/{filename}.png"
        await asyncio.sleep(1)
        await page.screenshot(path=path)
        print(f"Screenshot saved to {path}")
    except Exception as e:
        print(f"Error while taking screenshot for '{testname}' with filename '{filename}': {str(e)}")


async def ensure_sidebar_expanded(page):
    # Locate the sidebar toggle icon
    toggle_icon = page.locator('.ant-layout-sider__toggle-icon')

    # Check if the sidebar is collapsed by checking the parent element's class
    is_collapsed = await toggle_icon.evaluate("toggleIcon => toggleIcon.closest('.ant-layout-sider-collapsed') !== null")

    # If the sidebar is collapsed, click the toggle icon to expand it
    if is_collapsed:
        await toggle_icon.click(force=True)



async def skip_tour_guides(page):
    # List of tours
    tours = ['onboarding-5.3.0', 'tableauViewTour', 'encLoading', 'fullChip', 'dataExport']

    # Iterate over tours and set them in local storage
    for tour in tours:
        await page.evaluate(f"localStorage.setItem('ended_tour_id:{tour}', 'true');")

async def dismiss_tour_guide(page):
    # Find and click the dismiss button for the tour guide popover
    await page.locator('.cdk-overlay-container .ant-popover-content .ant-popover-inner span button').click()


