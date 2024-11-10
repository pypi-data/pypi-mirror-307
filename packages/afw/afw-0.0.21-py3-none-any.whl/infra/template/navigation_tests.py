import asyncio
import time
import pytest
from infra.helpers.tools import unix_to_datetime
from infra.helpers.playwright_helpers import click_text, click_role
from infra.helpers.afw_decorators import do_login

async def wait_for_page_load(page):
    """
    Wait for the page to load by checking the visibility of important elements.
    """
    # Ensure the event loop is running
    loop = asyncio.get_running_loop()

    # Check if ant-spin is visible and wait for it to disappear (loading spinner)
    if await page.locator('.ant-spin.ant-spin-spinning').is_visible():
        # Wait for all spinners to disappear
        spinners = await page.locator('.ant-spin.ant-spin-spinning').all()

        for spinner in spinners:
            await spinner.wait_for(state='hidden')

        # await page.locator('.ant-spin.ant-spin-spinning').wait_for(state='hidden')


    # Check if ant-skeleton-paragraph is visible and wait for it to disappear (skeleton loading screen)
    if await page.locator('ant-skeleton-paragraph').is_visible():
        await page.locator('ant-skeleton-paragraph').wait_for(state='hidden')

    # Check if 'ant-skeleton-paragraph ng-star-inserted' is visible and wait for it to disappear (skeleton content)
    if await page.locator('ant-skeleton-paragraph ng-star-inserted').is_visible():
        await page.locator('ant-skeleton-paragraph ng-star-inserted').wait_for(state='hidden')

    # Wait for the 'ic-outliers-trends canvas' to be visible
    if await page.locator('ic-outliers-trends').is_visible():
        # Filter based on specific text inside the 'ic-outlier-trend-card' and then wait for its canvas
        canvas_locator = page.locator('ic-outlier-trend-card').filter(has_text="Iddq").locator('canvas')

        # Now wait for the specific canvas to become visible
        await canvas_locator.wait_for(state='visible')

        # await page.locator('ic-outliers-trends canvas').wait_for(state='visible')

    print("Page has fully loaded.")

async def measure_load_time(page, action_description, actions):
    """
    Measure the load time of an action and verify that a list of elements becomes visible after the action.

    :param action_description: A description of the action being measured (for logging).
    :param actions: A list of async actions to perform (e.g., clicks, navigation).
    :param verification_elements: A list of (locator, description) tuples. Each locator will be checked for visibility.
    """
    loop = asyncio.get_running_loop()

    start_time = time.time()  # Record start time for the action

    for action in actions:
        await action  # Execute each action sequentially

    await wait_for_page_load(page)

    action_end_time = time.time()  # Record end time for the action
    action_elapsed_time = (action_end_time - start_time) * 1000  # Calculate elapsed time for the action
    print(f"{action_description} took {action_elapsed_time:.2f} ms")

    start_time_dt = await unix_to_datetime(start_time)
    action_end_time_dt = await unix_to_datetime(action_end_time)
    
    with open('result.txt', 'a') as result_file:

        result_file.write(
            f"{start_time_dt}, {action_end_time_dt}, {page.url}, {page.context.browser.browser_type.name}, {page.context.browser.version}, {action_description}, {action_elapsed_time:.2f}\n")

    with open('sql_insert.txt', 'a') as result_file:
        insert_query = f"""INSERT INTO navigation_performance (start_time, end_time, url, browser_type, browser_version, action_description, action_elapsed_time) VALUES ('{start_time_dt}', '{action_end_time_dt}', '{page.url}', '{page.context.browser.browser_type.name}', '{page.context.browser.version}', '{action_description}', '{action_elapsed_time:.2f}');"""
        
        result_file.write(insert_query)
        result_file.write('\n')

        # data = (start_time_dt, action_end_time_dt, page.url, page.context.browser.browser_type.name, page.context.browser.versioner_version, action_description, action_elapsed_time)

        # result_file.write(f"{start_time} - {action_end_time}\t | {action_description} took {action_elapsed_time:.2f} ms\n")

    # await asyncio.sleep(5)
        # await page.pause()

async def navigate(page, menu, tab=None, sub_tab=None):
    """
    Navigate through the UI by clicking on menu items and tabs.
    """

    loop = asyncio.get_running_loop()

    await page.locator(menu).click(force=True)


    if tab:
        try:
            await page.locator(".ant-layout-sider-children > fa-icon").click(
                force=True)  # Click the main navigation icon
            await click_text(page, tab)  # Click on the tab
        except Exception as e:
            await click_role(page, "link", tab)  # Click on the tab

        if sub_tab:
            await click_role(page, "link", sub_tab)  # Click on sub-tab if needed

async def exec_test(page, test_description, actions_scenario=[]):
    try:
        await measure_load_time(page, action_description=test_description, actions=actions_scenario)
        return True
    except Exception as e:
        print(f"exec_test failed: {e}")
        return False

async def run_navigation_test(page, test_name, menu, tab=None, sub_tab=None):

    description = f"{test_name} {sub_tab or ''}"
    actions_scenario = [navigate(page, menu, tab, sub_tab)]
    result = await exec_test(page, description, actions_scenario)

    print(f"RESULT: Navigate to '{sub_tab or tab}' - {'succeeded' if result else 'failed'}")
    if not result:
        pytest.skip(f"TEST SKIPPED: Unable to Navigate to '{sub_tab or tab}'")



@pytest.mark.asyncio
@do_login()
async def test_navigate_overview(page, url, username, password, headless):
    test_name = 'Overview'
    await run_navigation_test(page, test_name, menu='#page-toolbar__logo')
