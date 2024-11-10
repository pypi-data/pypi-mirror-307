import json
import nest_asyncio
import shutil
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright


# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()


async def handle_console_msg(msg):
    print(f"Console log: {msg.text}")

@asynccontextmanager
async def browser_base():
    playwright = await async_playwright().start()
    try:
        yield playwright
    finally:
        await playwright.stop()

class PlaywrightManager:
    def __init__(self, headless=False):
        self.playwright = None
        self.browser = None
        self.page = None
        self.client = None
        self.headless = headless
        

    async def get_page(self):
        if self.playwright is None:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=["--start-fullscreen", "--start-maximized"]
            )
            

            context = await self.browser.new_context(
                record_video_dir="videos/"
                # record_video_size={"width": 1920, "height": 920}
            )

            # Clear all cookies and cache before starting
            await self.clear_cookies_and_cache(context)

            # Set global timeout for all actions
            context.set_default_timeout(60000)

            self.page = await context.new_page()

            # Set the viewport size
            await self.page.set_viewport_size({"width": 1920, "height": 920})

            # Add a listener for console events
            self.page.on("console", handle_console_msg)

            # video_path = await self.page.video.path()
            # print(f"video: {video_path}")

        return self.page

    async def close(self):
        try:
            if self.page is not None:
                await self.page.close()
            if self.browser is not None:
                await self.browser.close()
            if self.playwright is not None:
                await self.playwright.stop()
        except Exception as e:
            print(f'ERROR! {e}')

    async def get_performance(self):
        window_performance_timing = await self.page.evaluate("() => JSON.stringify(window.performance.timing)")
        performance_timing = await self.page.evaluate("() => performance.getEntriesByType('navigation')")
        performance_metrics = await self.client.send("Performance.getMetrics")
        performance_navigation = json.loads(
            await self.page.evaluate("() => JSON.stringify(window.performance.getEntriesByType('navigation'))"))
        performance_resource = json.loads(
            await self.page.evaluate("() => JSON.stringify(window.performance.getEntriesByType('resource'))"))

        res = {
            'window_performance_timing': window_performance_timing,
            'performance_timing': performance_timing,
            'performance_metrics': performance_metrics,
            'performance_navigation': performance_navigation,
            'performance_resource': performance_resource
        }

        return res

    async def get_performance_metrics(self):
        perf_data = await self.get_performance()
        # print(perf_data)
        print(f"get_performance_metrics: {len(perf_data)}")
        return perf_data

    async def activate_performance(self):
        self.client = await self.page.context.new_cdp_session(self.page)
        await self.client.send("Performance.enable")

    async def trace_monitoring_start(self, testname):
        await self.browser.start_tracing(page=self.page, path=f"{testname}.json", screenshots=True)
        await self.page.context.tracing.start(screenshots=True, snapshots=True, sources=True, title=f"{testname}.json")
        video_path = await self.page.video.path()
        print(f"video: {video_path}")

    async def trace_monitoring_stop(self, testname):
        await self.page.context.tracing.stop(path=f"{testname}.zip")

    async def clear_cookies_and_cache(self, context):
        # Clear all cookies
        await context.clear_cookies()

        try:
            # Clear cache by navigating to about:blank and clearing storage
            page = await context.new_page()
            await page.goto("about:blank")
            await page.evaluate("window.localStorage.clear()")
            await page.evaluate("window.sessionStorage.clear()")

            await page.close()
        except Exception as e:
            print(f"Error clearing storage: {e}")


