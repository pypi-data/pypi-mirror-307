import browsers
#
#
#
#
def get_installed_browsers():
    installed_browsers = []

    for browser in browsers.browsers():
        if browser not in installed_browsers:
            installed_browsers.append(browser)

    return installed_browsers
#
#
#
#
def get_browser_version(browser_name: str):
    for browser in browsers.browsers():
        if browser["display_name"] == browser_name:
            return browser["version"]

    return None
