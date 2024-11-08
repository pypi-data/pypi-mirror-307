from time import sleep
from subprocess import Popen
from random import choice, random
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webelement import WebElement
from PyWebScraping.utilities import WindowRect
from PyWindowsCMD.taskkill.functions import taskkill_windows
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from PyWebScraping.browsers_handler import get_browser_version
from PyWindowsCMD.netstat.functions import get_localhost_beasy_ports, get_localhost_minimum_free_port, get_localhost_processes_with_pids
#
#
#
#
class EmptyWebDriver:
	def __init__(self, implicitly_wait: int = 5, page_load_timeout: int = 5):
		self.base_implicitly_wait, self.base_page_load_timeout = implicitly_wait, page_load_timeout
		self.driver = None
	#
	#
	#
	#
	def switch_to_window(self, window: str | int = None):
		"""Switches focus to the specified window.

		:Args:
		- window: The name or the index or window handle of the window to switch to.

		:Returns:
			- SwitchTo: an object containing all options to switch focus into
		"""
		if type(window) == str:
			self.driver.switch_to.window(window)
		elif type(window) == int:
			self.driver.switch_to.window(self.driver.window_handles[window])
		else:
			self.driver.switch_to.window(self.driver.current_window_handle)
	#
	#
	#
	#
	def close_window(self, window: str | int = None):
		"""Closes the window.

		:param window: The name or the index or window handle of the window to close. If it's None driver closes current window
		"""
		if window is not None:
			switch_to_new_window = window == self.driver.current_window_handle

			self.switch_to_window(window)
			self.driver.close()

			if switch_to_new_window:
				self.switch_to_window(-1)
	#
	#
	#
	#
	def close_all_windows(self):
		"""Closes all windows."""
		for window in self.driver.window_handles:
			self.close_window(window)
	#
	#
	#
	#
	def update_times(
			self,
			temp_implicitly_wait: int = None,
			temp_page_load_timeout: int = None
	):
		if temp_implicitly_wait:
			implicitly_wait = temp_implicitly_wait + random()
		else:
			implicitly_wait = self.base_implicitly_wait + random()

		if temp_page_load_timeout:
			page_load_timeout = temp_page_load_timeout + random()
		else:
			page_load_timeout = self.base_page_load_timeout + random()

		self.driver.implicitly_wait(implicitly_wait)
		self.driver.set_page_load_timeout(page_load_timeout)
	#
	#
	#
	#
	def find_inner_web_element(
			self,
			parent_element: WebElement,
			by: By,
			value: str,
			temp_implicitly_wait: int = None,
			temp_page_load_timeout: int = None
	):
		self.update_times(temp_implicitly_wait, temp_page_load_timeout)
		return parent_element.find_element(by, value)
	#
	#
	#
	#
	def find_inner_web_elements(
			self,
			parent_element: WebElement,
			by: By,
			value: str,
			temp_implicitly_wait: int = None,
			temp_page_load_timeout: int = None
	):
		self.update_times(temp_implicitly_wait, temp_page_load_timeout)
		return parent_element.find_elements(by, value)
	#
	#
	#
	#
	def find_web_elements(
			self,
			by: By,
			value: str,
			temp_implicitly_wait: int = None,
			temp_page_load_timeout: int = None
	):
		"""Find elements given a By strategy and locator.

		:Usage:
			::

				elements = driver.find_elements(By.CLASS_NAME, 'foo')

		:rtype: list of WebElement
		"""
		self.update_times(temp_implicitly_wait, temp_page_load_timeout)
		return self.driver.find_elements(by, value)
	#
	#
	#
	#
	def get_current_url(self):
		current_url: str = self.driver.current_url
		return current_url
	#
	#
	#
	#
	def get_page_html(self):
		"""
		Returns current page html
		:Returns:
		- page_source
		:rtype: str
		"""
		return self.driver.page_source
	#
	#
	#
	#
	def get_rect(self):
		window_rect = self.driver.get_window_rect()

		return WindowRect(
				window_rect["x"],
				window_rect["y"],
				window_rect["width"],
				window_rect["height"]
		)
	#
	#
	#
	#
	def get_windows_names(self):
		windows_names: list[str] = self.driver.window_handles
		return windows_names
	#
	#
	#
	#
	def hover_element(self, element: WebElement):
		"""Moving the mouse to the middle of an element.

		:Args:
		 - element: The WebElement to move to.
		"""
		ActionChains(self.driver).move_to_element(element).perform()
	#
	#
	#
	#
	def execute_js_script(self, script: str, *args):
		self.driver.execute_script(script, *args)
	#
	#
	#
	#
	def open_new_tab(self, link: str = ""):
		self.execute_js_script("window.open(\"%s\");" % link)
	#
	#
	#
	#
	def refresh_webdriver(self):
		self.driver.refresh()
	#
	#
	#
	#
	def scroll_by_amount(self, x: int = 0, y: int = 0):
		"""
		Scrolls by provided amounts with the origin in the top left corner of the viewport.

		:Args:
		 - x: Distance along X axis to scroll using the wheel. A negative value scrolls left.
		 - y: Distance along Y axis to scroll using the wheel. A negative value scrolls up.
		"""
		ActionChains(self.driver).scroll_by_amount(x, y)
	#
	#
	#
	#
	def find_web_element(
			self,
			by: By,
			value: str,
			temp_implicitly_wait: int = None,
			temp_page_load_timeout: int = None
	):
		"""
		Find an element given a By strategy and locator.
		:Usage:
			::

				element = driver.find_element(By.ID, 'foo')

		:rtype: WebElement
		"""
		self.update_times(temp_implicitly_wait, temp_page_load_timeout)
		return self.driver.find_element(by, value)
	#
	#
	#
	#
	def scroll_down_of_element(self, by: By, value: str):
		self.find_web_element(by, value).send_keys(Keys.PAGE_DOWN)
	#
	#
	#
	#
	def scroll_from_origin(self, origin: ScrollOrigin, x: int = 0, y: int = 0):
		"""
		Scrolls by provided amount based on a provided origin. The scroll
		origin is either the center of an element or the upper left of the
		viewport plus any offsets. If the origin is an element, and the element
		is not in the viewport, the bottom of the element will first be
		scrolled to the bottom of the viewport.

		:Args:
		 - origin: Where scroll originates (viewport or element center) plus provided offsets.
		 - x: Distance along X axis to scroll using the wheel. A negative value scrolls left.
		 - y: Distance along Y axis to scroll using the wheel. A negative value scrolls up.

		 :Raises: If the origin with offset is outside the viewport.
		  - MoveTargetOutOfBoundsException - If the origin with offset is outside the viewport.
		"""
		ActionChains(self.driver).scroll_from_origin(origin, x, y)
	#
	#
	#
	#
	def scroll_to_element(self, element: WebElement):
		"""
		If the element is outside the viewport, scrolls the bottom of the element to the bottom of the viewport.

		:Args:
		 - element: Which element to scroll into the viewport.
		"""
		ActionChains(self.driver).scroll_to_element(element).perform()
	#
	#
	#
	#
	def scroll_up_of_element(self, by: By, value: str):
		self.find_web_element(by, value).send_keys(Keys.PAGE_UP)
	#
	#
	#
	#
	def search_url(
			self,
			url: str,
			temp_implicitly_wait: int = None,
			temp_page_load_timeout: int = None
	):
		"""Loads a web page in the current browser session."""
		self.update_times(temp_implicitly_wait, temp_page_load_timeout)
		self.driver.get(url)
	#
	#
	#
	#
	def stop_browser_loading(self):
		self.execute_js_script("window.stop();")
#
#
#
#
class BrowserOptionsManager:
	def __init__(
			self,
			debugging_port_command: str,
			user_agent_command: str,
			proxy_command: str,
			debugging_port: int = None,
			user_agent: list[str] = None,
			proxy: str | list[str] = None
	):
		self.options = self.renew_webdriver_options()
		self.debugging_port_command, self.user_agent_command, self.proxy_command = debugging_port_command, user_agent_command, proxy_command
		self.debugging_port, self.user_agent, self.proxy = None, None, None
		self.set_debugger_address(debugging_port)
		self.hide_automation()
		self.set_proxy(proxy)
		self.set_user_agent(user_agent)
	#
	#
	#
	#
	def set_user_agent(self, user_agent: list[str] = None):
		if user_agent is not None:
			self.user_agent = user_agent
		else:
			self.user_agent = [
				"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
				"AppleWebKit/537.36 (KHTML, like Gecko)",
				"Safari/537.36",
				"Chrome/%s.0.0.0" % get_browser_version("Google Chrome").split(".")[0]
			]

		self.options.add_argument(self.user_agent_command % " ".join(self.user_agent))
	#
	#
	#
	#
	def set_proxy(self, proxy: str | list[str] = None):
		self.proxy = proxy

		if self.proxy is not None:
			if type(self.proxy) == str:
				self.options.add_argument(self.proxy_command % self.proxy)
			else:
				self.options.add_argument(self.proxy_command % choice(self.proxy))
	#
	#
	#
	#
	def hide_automation(self):
		pass
	#
	#
	#
	#
	def set_debugger_address(self, debugging_port: int):
		self.debugging_port = debugging_port

		if self.debugging_port is not None:
			self.options.debugger_address = self.debugging_port_command % self.debugging_port
	#
	#
	#
	#
	def renew_webdriver_options(self):
		pass
#
#
#
#
class BrowserStartArgs:
	start_command = ""
	#
	#
	#
	#
	def __init__(
			self,
			browser_file_name: str,
			debugging_port_command_line: str,
			webdriver_dir_command_line: str,
			headless_mode_command_line: str,
			mute_audio_command_line: str,
			webdriver_dir: str = None,
			debugging_port: int = None,
			headless_mode: bool = False,
			mute_audio: bool = False
	):
		self.browser_file_name = browser_file_name
		self.debugging_port_command_line, self.webdriver_dir_command_line, self.headless_mode_command_line, self.mute_audio_command_line = debugging_port_command_line, webdriver_dir_command_line, headless_mode_command_line, mute_audio_command_line
		self.debugging_port, self.webdriver_dir, self.headless_mode, self.mute_audio = debugging_port, webdriver_dir, headless_mode, mute_audio
		self.update_command()
	#
	#
	#
	#
	def update_command(self):
		start_args = [self.browser_file_name]

		if self.debugging_port is not None:
			start_args.append(self.debugging_port_command_line % self.debugging_port)

		if self.webdriver_dir is not None:
			start_args.append(self.webdriver_dir_command_line % self.webdriver_dir)

		if self.headless_mode:
			start_args.append(self.headless_mode_command_line)

		if self.mute_audio is not None:
			start_args.append(self.mute_audio_command_line)

		self.start_command = " ".join(start_args)
	#
	#
	#
	#
	def clear_command(self):
		self.debugging_port = None
		self.webdriver_dir = None
		self.headless_mode = False

		self.update_command()
	#
	#
	#
	#
	def set_debugging_port(self, debugging_port: int = None):
		self.debugging_port = debugging_port

		self.update_command()
	#
	#
	#
	#
	def set_headless_mode(self, headless_mode: bool = False):
		self.headless_mode = headless_mode

		self.update_command()
	#
	#
	#
	#
	def set_mute_audio(self, mute_audio: bool = False):
		self.mute_audio = mute_audio

		self.update_command()
	#
	#
	#
	#
	def set_webdriver_dir(self, webdriver_dir: str = None):
		self.webdriver_dir = webdriver_dir

		self.update_command()
#
#
#
#
class BrowserWebDriver(EmptyWebDriver):
	def __init__(
			self,
			browser_file_name: str,
			bsa_debugging_port_command_line: str,
			bsa_webdriver_dir_command_line: str,
			bsa_headless_mode_command_line: str,
			bsa_mute_audio_command_line: str,
			bom_debugging_port_command: str,
			bom_user_agent_command: str,
			bom_proxy_command: str,
			webdriver_path: str,
			webdriver_start_args: BrowserStartArgs = None,
			webdriver_options_manager: BrowserOptionsManager = None,
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			window_rect: WindowRect = WindowRect()
	):
		super().__init__(implicitly_wait, page_load_timeout)
		#
		#
		#
		#
		self.browser_file_name, self.bsa_debugging_port_command_line, self.bsa_webdriver_dir_command_line, self.bsa_headless_mode_command_line, self.bsa_mute_audio_command_line = browser_file_name, bsa_debugging_port_command_line, bsa_webdriver_dir_command_line, bsa_headless_mode_command_line, bsa_mute_audio_command_line
		self.bom_debugging_port_command, self.bom_user_agent_command, self.bom_proxy_command = bom_debugging_port_command, bom_user_agent_command, bom_proxy_command
		self.webdriver_path = webdriver_path
		#
		#
		#
		#
		if webdriver_start_args is not None:
			self.webdriver_start_args = webdriver_start_args
		else:
			self.webdriver_start_args = BrowserStartArgs(
					self.browser_file_name,
					self.bsa_debugging_port_command_line,
					self.bsa_webdriver_dir_command_line,
					self.bsa_headless_mode_command_line,
					self.bsa_mute_audio_command_line
			)
		#
		#
		#
		#
		if webdriver_options_manager is not None:
			self.webdriver_options_manager = webdriver_options_manager
		else:
			self.webdriver_options_manager = BrowserOptionsManager(
					self.bom_debugging_port_command,
					self.bom_user_agent_command,
					self.bom_proxy_command
			)
		#
		#
		#
		#
		self.webdriver_dir, self.headless_mode, self.mute_audio = self.webdriver_start_args.webdriver_dir, self.webdriver_start_args.headless_mode, self.webdriver_start_args.mute_audio
		self.user_agent, self.proxy = self.webdriver_options_manager.user_agent, self.webdriver_options_manager.proxy
		if self.webdriver_options_manager.debugging_port is not None and self.webdriver_start_args.debugging_port is not None:
			#
			#
			#
			#
			self.debugging_port = self.webdriver_options_manager.debugging_port
		elif self.webdriver_options_manager.debugging_port is not None:
			#
			#
			#
			#
			self.debugging_port = self.webdriver_options_manager.debugging_port
			self.webdriver_start_args.set_debugging_port(self.debugging_port)
		elif self.webdriver_start_args.debugging_port is not None:
			#
			#
			#
			#
			self.debugging_port = self.webdriver_start_args.debugging_port
			self.webdriver_options_manager.set_debugger_address(self.debugging_port)
		#
		#
		#
		#
		else:
			#
			#
			#
			#
			self.debugging_port = None
		self.window_rect = window_rect
		self.webdriver_is_active = False
		self.webdriver_service, self.webdriver_options = None, None
	#
	#
	#
	#
	def create_driver(self):
		pass
	#
	#
	#
	#
	def renew_bas_and_bom(self):
		pass
	#
	#
	#
	#
	def check_webdriver_active(self):
		if self.debugging_port is not None and self.debugging_port in get_localhost_beasy_ports():
			return True
		else:
			return False
	#
	#
	#
	#
	def start_webdriver(
			self,
			debugging_port: int = None,
			webdriver_dir: str = None,
			headless_mode: bool = None,
			mute_audio: bool = None,
			proxy: str | list[str] = None,
			user_agent: list[str] = None,
			window_rect: WindowRect = None
	):
		if self.driver is None:
			if webdriver_dir is not None:
				self.webdriver_dir = webdriver_dir

			if debugging_port is not None:
				self.debugging_port = get_localhost_minimum_free_port(debugging_port)
			elif self.debugging_port is None:
				self.debugging_port = get_localhost_minimum_free_port()

			if headless_mode is not None:
				self.headless_mode = headless_mode

			if headless_mode is not None:
				self.mute_audio = mute_audio

			if user_agent is not None:
				self.user_agent = user_agent

			if proxy is not None:
				self.proxy = proxy

			if window_rect is not None:
				self.window_rect = window_rect

			self.webdriver_is_active = self.check_webdriver_active()

			if not self.webdriver_is_active:
				self.renew_bas_and_bom()

				Popen(self.webdriver_start_args.start_command, shell=True)

				while not self.webdriver_is_active:
					self.webdriver_is_active = self.check_webdriver_active()

				self.create_driver()
			else:
				self.webdriver_start_args.set_debugging_port(self.debugging_port)
				self.webdriver_options_manager.set_debugger_address(self.debugging_port)

				self.create_driver()
	#
	#
	#
	#
	def close_webdriver(self):
		for pid, ports in get_localhost_processes_with_pids().items():
			if self.debugging_port in ports:
				taskkill_windows(pid=pid, f=True)

				while self.webdriver_is_active:
					self.webdriver_is_active = self.check_webdriver_active()

				sleep(1)
				break

		self.webdriver_service = None
		self.webdriver_options = None
		self.driver = None
	#
	#
	#
	#
	def restart_webdriver(
			self,
			debugging_port: int = None,
			webdriver_dir: str = None,
			headless_mode: bool = None,
			mute_audio: bool = None,
			proxy: str | list[str] = None,
			user_agent: list[str] = None,
			window_rect: WindowRect = None
	):
		self.close_webdriver()
		self.start_webdriver(
				debugging_port,
				webdriver_dir,
				headless_mode,
				mute_audio,
				proxy,
				user_agent,
				window_rect
		)
	#
	#
	#
	#
	def change_proxy(self, proxy: str | list[str]):
		self.webdriver_options_manager.set_proxy(proxy)
		self.restart_webdriver()
	#
	#
	#
	#
	def get_vars_for_remote(self):
		"""
		Returns vars for establishing remote webdriver
		:return: "command_executor._url" and "session_id"
		:rtype: (str, str)
		"""
		return self.driver.command_executor._url, self.driver.session_id
