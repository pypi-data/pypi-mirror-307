import asyncio
import functools
import os
import time
# from ..drivers.browser_base import PlaywrightManager
from infra.drivers.browser_base import PlaywrightManager
from infra.helpers.playwright_helpers import handle_popup, click_text, click_role
from infra.helpers.login_ui import Login


async def playwright_manager(headless):
    manager = PlaywrightManager(headless=headless)
    yield manager
    await manager.close()


async def page(playwright_manager):
    page = await playwright_manager.get_page()
    yield page
    await playwright_manager.close()


def print_execution_time(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Record the start time
        start_time = time.time()

        # Execute the function
        result = await func(*args, **kwargs)

        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time in milliseconds
        elapsed_time_ms = (end_time - start_time) * 1000

        # Print the time taken
        print(f"Execution time for {func.__name__}: {elapsed_time_ms:.2f} ms")

        return result

    return wrapper


def do_login():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):


            # Extract url, username, and password from kwargs
            url = kwargs.get('url')
            username = kwargs.get('username')
            password = kwargs.get('password')
            headless = kwargs.get('headless')

            if not url or not username or not password:
                raise ValueError("Test function must include 'url', 'username', and 'password' as keyword arguments")

            # Initialize the PlaywrightManager
            playwright_manager = PlaywrightManager(headless=headless)
            loop = asyncio.get_running_loop()
            try:
                # Get the page
                page = await playwright_manager.get_page()

                if page is None:
                    raise ValueError("Test function must include 'page' as a keyword argument")

                func_name = func.__name__
                await playwright_manager.trace_monitoring_start(func_name)

                # Perform login
                login = Login(page)
                page = await login.do_login(url, username, password)

                # Avoid passing 'page' twice if it's already in kwargs
                kwargs['page'] = page

                # Call the decorated test function
                res = await func(*args, **kwargs)

                # Get the page title
                page_title = await page.title()

                # Get the video path and rename it
                video_path = await page.video.path()

                # Define the new video name using the page title, ensuring it's file-system safe
                new_video_name = f"videos/{func_name}.webm"

                # Rename the video file
                os.rename(video_path, new_video_name)
                # os.remove(video_path)

                print(f"Video saved as {video_path}")
                print(f"Video saved as {new_video_name}")

                await playwright_manager.trace_monitoring_stop(func_name)

                return res

            except Exception as e:
                # Handle any exceptions during the test
                print(f"Error during test execution: {e}")
                raise

            finally:

                # Ensure the browser is closed at the end of the test
                await playwright_manager.close()

        return wrapper
    return decorator


def navigate_to(menu="#control-hub-link", tab="Export", sub_tab="Post-Silicon"):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(page, *args, **kwargs):

            # if 'page' not in kwargs:
            #     print('Page is not exists')
            #     return


            # page = kwargs['page']

            await handle_popup(page)
            # await page.locator(menu).click(force=True)
            # await page.locator(".ant-layout-sider-children > fa-icon").click(force=True)

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

            # # Click on the tab and sub-tab
            # await click_text(page, tab)
            # await click_role(page, "link", sub_tab)

            # Handle any popups that might appear
            await handle_popup(page)

            # Call the decorated function with 'page' passed along
            # return await func(page, *args, **kwargs)

            # Avoid passing 'page' twice if it's already in kwargs
            if 'page' not in kwargs:
                kwargs['page'] = page

            # Call the decorated test function
            return await func(*args, **kwargs)


        return wrapper
    return decorator