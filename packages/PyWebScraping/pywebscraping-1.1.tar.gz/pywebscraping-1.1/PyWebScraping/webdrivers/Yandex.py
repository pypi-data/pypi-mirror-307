from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PyWebScraping.utilities import WindowRect
from PyWebScraping.webdrivers.BaseDriver import BrowserOptionsManager, BrowserStartArgs, BrowserWebDriver, EmptyWebDriver
#
#
#
#
class YandexOptionsManager(BrowserOptionsManager):
	def __init__(
			self,
			debugging_port: int = None,
			user_agent: list[str] = None,
			proxy: str | list[str] = None
	):
		super().__init__(
				"127.0.0.1:%d",
				"user-agent=%s",
				"--proxy-server=%s",
				debugging_port,
				user_agent,
				proxy
		)
	#
	#
	#
	#
	def hide_automation(self):
		self.options.add_argument("--disable-blink-features=AutomationControlled")
		self.options.add_argument("--no-first-run")
		self.options.add_argument("--no-service-autorun")
		self.options.add_argument("--password-store=basic")
	#
	#
	#
	#
	def renew_webdriver_options(self):
		return Options()
#
#
#
#
class YandexStartArgs(BrowserStartArgs):
	def __init__(
			self,
			webdriver_dir: str = None,
			debugging_port: int = None,
			headless_mode: bool = False,
			mute_audio: bool = False
	):
		super().__init__(
				"browser.exe",
				"--remote-debugging-port=%d",
				"--user-data-dir=\"%s\"",
				"--headless=new",
				"--mute-audio",
				webdriver_dir,
				debugging_port,
				headless_mode,
				mute_audio
		)
#
#
#
#
class YandexWebDriver(BrowserWebDriver):
	def __init__(
			self,
			webdriver_path: str,
			webdriver_start_args: YandexStartArgs = YandexStartArgs(),
			webdriver_options_manager: YandexOptionsManager = YandexOptionsManager(),
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			window_rect: WindowRect = WindowRect()
	):
		super().__init__(
				"browser.exe",
				"--remote-debugging-port=%d",
				"--user-data-dir=\"%s\"",
				"--headless=new",
				"--mute-audio",
				"127.0.0.1:%d",
				"user-agent=%s",
				"--proxy-server=%s",
				webdriver_path,
				webdriver_start_args,
				webdriver_options_manager,
				implicitly_wait,
				page_load_timeout,
				window_rect
		)
	#
	#
	#
	#
	def create_driver(self):
		self.webdriver_service = Service(executable_path=self.webdriver_path)
		self.webdriver_options = self.webdriver_options_manager.options

		self.driver = webdriver.Chrome(
				options=self.webdriver_options,
				service=self.webdriver_service
		)

		self.driver.set_window_position(x=self.window_rect.x, y=self.window_rect.y)
		self.driver.set_window_size(width=self.window_rect.width, height=self.window_rect.height)

		self.driver.implicitly_wait(self.base_implicitly_wait)
		self.driver.set_page_load_timeout(self.base_page_load_timeout)
	#
	#
	#
	#
	def renew_bas_and_bom(self):
		self.webdriver_start_args = YandexStartArgs(
				self.webdriver_dir,
				self.debugging_port,
				self.headless_mode,
				self.mute_audio
		)
		self.webdriver_options_manager = YandexOptionsManager(self.debugging_port, self.user_agent, self.proxy)
#
#
#
#
class YandexRemoteWebDriver(EmptyWebDriver):
	def __init__(
			self,
			command_executor: str,
			session_id: str,
			webdriver_options_manager: YandexOptionsManager = YandexOptionsManager(),
			implicitly_wait: int = 5,
			page_load_timeout: int = 5
	):
		super().__init__(implicitly_wait, page_load_timeout)
		#
		#
		#
		#
		self.command_executor, self.session_id = command_executor, session_id
		self.webdriver_options_manager = webdriver_options_manager
	#
	#
	#
	#
	def create_driver(self, command_executor: str = None, session_id: str = None):
		if command_executor is not None:
			self.command_executor = command_executor

		if session_id is not None:
			self.session_id = session_id

		self.driver = webdriver.Remote(
				command_executor=self.command_executor,
				options=self.webdriver_options_manager.options
		)

		self.close_window()
		self.driver.session_id = self.session_id
		self.switch_to_window()

		self.driver.implicitly_wait(self.base_implicitly_wait)
		self.driver.set_page_load_timeout(self.base_page_load_timeout)
