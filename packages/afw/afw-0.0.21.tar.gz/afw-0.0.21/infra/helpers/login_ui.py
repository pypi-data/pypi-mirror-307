import asyncio
from asyncio import TimeoutError, exceptions
from allure import step


# from infra.helpers.login_ui import handle_popup, skip_tour_guides


class Login:
    login_details = [] # settings.PLATFORM_LOGIN_SETTINGS_DEFAULT

    def __init__(self, page):
        self.page = page  # Ensure this is a Playwright page object, not an async generator.

    @property
    def user_name(self):
        return self.page.locator("[id=username]")

    @property
    def password(self):
        return self.page.locator("[id=password]")

    @property
    def submit_button(self):
        return self.page.locator("[type='submit']")

    async def submit_login(self, username, password):

        # base_url = self.login_details['base_url']
        # ns = self.login_details['namespace']

        # ret = create_user(base_url, username, ns)

        await self.user_name.fill(username)
        await self.password.fill(password)

        await self.submit_button.click()

        await self.page.wait_for_load_state('load')

        # await skip_tour_guides(self.page)

        # Call this function asynchronously at the start of your script/test
        # close_overlay_task = asyncio.create_task(self.close_overlays_when_appear())

        # Call this function to set up the observer when the page is loaded
        # await self.setup_overlay_listener()

        await self.login_completed()

    async def navigate(self, host_url, timeout):
        try:
            await self.page.goto(host_url, timeout=timeout)
            # await self.page.wait_for_load_state('load')
        except TimeoutError:
            raise Exception(f"Navigation to {host_url} timed out after {timeout} ms")
        except exceptions as e:
            raise Exception(f"Navigation to {host_url}: {e} ")

    async def do_login(self, url, username, password):
        # url = self.login_details['frontend_url']
        # username = self.login_details['user_name']
        # password = self.login_details['user_password']

        timeout = 30000  # Adjust timeout as needed (30 seconds)

        await self.navigate(url, timeout)

        await self.submit_login(username, password)

        return self.page

    async def login_completed(self):
        try:
            # await handle_popup(self.page)
            await self.page.get_by_role("link", name="logo").click()
            await self.skip_tour_guides()
            await self.dismiss_tour_guide()
            await self.page.screenshot(path="screenshots/signin_completed.png")
        except Exception as e:
            raise Exception(f"An error occurred during login completion: {str(e)}")


    async def close_overlays_when_appear(self):
        while True:
            # Check if the "Don't show me again" button is visible
            dont_show_button = self.page.get_by_role("button", name="Don't show me again")

            if await dont_show_button.is_visible(timeout=100):
                try:
                    # Click the "Don't show me again" button to close the overlay
                    await dont_show_button.click()
                    print("Clicked 'Don't show me again' button.")
                except Exception as e:
                    print(f"Error clicking 'Don't show me again' button: {e}")
            else:
                # If the overlay doesn't exist, just continue monitoring
                await asyncio.sleep(1000)  # Wait 1 second before checking again

    async def setup_overlay_listener(self):
        await self.page.evaluate("""
            // Create a mutation observer
            const observer = new MutationObserver((mutationsList, observer) => {
                for (const mutation of mutationsList) {
                    if (mutation.type === 'childList') {
                        const overlay = document.querySelector('.tour-guide-step__dont-show-me-again-button');
                        if (overlay) {
                            overlay.click();
                            console.log('Overlay closed via MutationObserver');
                        }
                    }
                }
            });

            // Observe the entire document for changes
            observer.observe(document.body, { childList: true, subtree: true });
        """)

    async def skip_tour_guides(self):
        # List of tours
        tours = ['onboarding-5.3.0', 'tableauViewTour', 'encLoading', 'fullChip', 'dataExport']

        # Iterate over tours and set them in local storage
        for tour in tours:
            await self.page.evaluate(f"localStorage.setItem('ended_tour_id:{tour}', 'true');")

    async def dismiss_tour_guide(self):
        # Find and click the dismiss button for the tour guide popover
        await self.page.locator('.cdk-overlay-container .ant-popover-content .ant-popover-inner span button').click()


