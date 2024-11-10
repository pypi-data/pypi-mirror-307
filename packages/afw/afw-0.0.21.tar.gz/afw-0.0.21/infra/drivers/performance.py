import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BrowserLogger")

# Create a file handler that logs even debug messages
fh = logging.FileHandler('browser_logger.log')
fh.setLevel(logging.DEBUG)  # Set the level for the file handler

class performance:

    def __init__(self, page):
        self.page = page
        self.client = self.page.context.new_cdp_session(self.page)

    def handle_console_event(self, msg):
        # print(f"[{msg.type}]\t\t{msg.text}")

        if msg.type == 'error':
            logger.error(f"{msg.text}")
        elif msg.type == 'warning':
            logger.warning(f"{msg.text}")
        else:
            logger.debug(f"{msg.text}")


    def collect_performance(self):
        # Register the event listener
        self.page.on("console", self.handle_console_event)

        # Enable CDP session
        self.client.send("Performance.enable")

        initial_metrics = self.get_performance()

        logger.info(f"{initial_metrics}")


    def get_performance(self):
        window_performance_timing = self.page.evaluate("() => JSON.stringify(window.performance.timing)")
        performance_timing = self.page.evaluate("() => performance.getEntriesByType('navigation')")
        performance_metrics = self.client.send("Performance.getMetrics")
        performance_navigation = json.loads(
            self.page.evaluate("() => JSON.stringify(window.performance.getEntriesByType('navigation'))"))
        performance_resource = json.loads(
            self.page.evaluate("() => JSON.stringify(window.performance.getEntriesByType('resource'))"))

        res = {
            'window_performance_timing': window_performance_timing,
            'performance_timing': performance_timing,
            'performance_metrics': performance_metrics,
            'performance_navigation': performance_navigation,
            'performance_resource': performance_resource
        }

        return res



    def performance_monitoring_stop(self, testname):
        self.client.send("Performance.enable")
        final_metrics = self.get_performance()
        self.page.context.tracing.stop(path=f"{testname}.zip")
        self.playwright.browser.stop_tracing()

        return final_metrics

    def performance_monitoring_stop(self, testname):
        self.client.send("Performance.enable")
        final_metrics = self.get_performance()
        self.page.context.tracing.stop(path=f"{testname}.zip")
        self.playwright.browser.stop_tracing()

        return final_metrics