import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginPage:
    
    POPUP_NOTIFICATION = (AppiumBy.ID, "ib_bg_lyt_onboarding_pager_fragment")
    USERNAME_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[@hint='USERNAME/EMAIL']")
    PASSWORD_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[@hint='PASSWORD']")
    LOGIN_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@content-desc='Log In']")

    def login(self, driver, username, password, timeout=30):
        print(f"Bắt đầu quá trình đăng nhập với tải khoản: {username}")
        wait = WebDriverWait(driver, timeout)

        popup_noti = wait.until(EC.visibility_of_element_located(LoginPage.POPUP_NOTIFICATION))
        if popup_noti.is_displayed():
            time.sleep(5)
        try:
            username_field = wait.until(EC.visibility_of_element_located(LoginPage.USERNAME_INPUT))
            username_field.click()
            username_field.send_keys(username)
            
            password_field = wait.until(EC.visibility_of_element_located(LoginPage.PASSWORD_INPUT))
            password_field.clear()
            password_field.click()
            password_field.send_keys(password)
            driver.hide_keyboard()
            
            login_button = wait.until(EC.element_to_be_clickable(LoginPage.LOGIN_BUTTON))
            login_button.click()
            time.sleep(1)
            login_button.click()

            print("Đã ấn Đăng nhập thành công!")
            return True
            
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Đã xảy ra lỗi trong quá trình đăng nhập: {e}")
            return False
    
    


class HomePage:
    ICON_PROFILE = (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Profile\nTab 5 of 5']")
    
    def navigate_tab_profile(self, driver, timeout=15):
        wait = WebDriverWait(driver, timeout)
        icon_profile = wait.until(EC.element_to_be_clickable(HomePage.ICON_PROFILE))
        icon_profile.click()

class TabProfile:

    ICON_OPEN_LEFT_MENU = (AppiumBy.ACCESSIBILITY_ID, "Open navigation menu")
    BUTTON_TUTORIAL = (AppiumBy.XPATH, "//android.view.View[@content-desc='Tutorials']")

    def click_button_tutorial(self, driver, timeout=15):
        wait = WebDriverWait(driver, timeout)
        button_tutorial = wait.until(EC.element_to_be_clickable(TabProfile.BUTTON_TUTORIAL))
        button_tutorial.click()

class TabTutorial:
    TILTLE_TUTORIAL = (AppiumBy.ACCESSIBILITY_ID, "Tutorials")
    Assigned_Route_Btn = (AppiumBy.ACCESSIBILITY_ID, "Assigned Route")
    Direct_Booking_Btn = (AppiumBy.ACCESSIBILITY_ID, "Direct Booking")
    Ticket_Booking_Btn = (AppiumBy.ACCESSIBILITY_ID, "Ticket Booking")
    def verify_title_tutorial(self, driver, timeout=15):
        wait = WebDriverWait(driver, timeout)
        title_tutorial = wait.until(EC.visibility_of_element_located(TabTutorial.TILTLE_TUTORIAL))
        assigned_route_btn = wait.until(EC.visibility_of_element_located(TabTutorial.Assigned_Route_Btn))
        direct_bôking_btn = wait.until(EC.visibility_of_element_located(TabTutorial.Direct_Booking_Btn))
        ticket_booking_btn = wait.until(EC.visibility_of_element_located(TabTutorial.Ticket_Booking_Btn))
        is_displayed = title_tutorial.is_displayed() and assigned_route_btn.is_displayed() and direct_bôking_btn.is_displayed() and ticket_booking_btn.is_displayed()
        assert is_displayed, "Không tìm thấy tiêu đề hoặc các nút trên trang Tutorial"

    def click_assigned_route_btn(self, driver, timeout=15):
        wait = WebDriverWait(driver, timeout)
        assigned_route_btn = wait.until(EC.element_to_be_clickable(TabTutorial.Assigned_Route_Btn))
        assigned_route_btn.click()

class ActiveAssignment:
    TITLE_ACTIVE_ASSIGNMENT = (AppiumBy.ACCESSIBILITY_ID, "Active Assignment")
    Start_Tutorial_BTN = (AppiumBy.ACCESSIBILITY_ID, "Start Tutorial")
    Quit_Start_Tutorial_BTN = (AppiumBy.ACCESSIBILITY_ID, "Quit tutorial")

    def verify_title_active_assignment(self, driver, timeout=15):
        wait = WebDriverWait(driver, timeout)
        title_active_assignment = wait.until(EC.visibility_of_element_located(ActiveAssignment.TITLE_ACTIVE_ASSIGNMENT))
        assert title_active_assignment.is_displayed(), "Không tìm thấy tiêu đề trên trang Active Assignment"

    def click_start_tutorial_btn(self, driver, timeout=15):
        wait = WebDriverWait(driver, timeout)
        start_tutorial_btn = wait.until(EC.element_to_be_clickable(ActiveAssignment.Start_Tutorial_BTN))
        if start_tutorial_btn.is_displayed():
            start_tutorial_btn.click()

    def verify_quit_start_tutorial_btn(self, driver, timeout=15):
        wait = WebDriverWait(driver, timeout)
        quit_start_tutorial_btn = wait.until(EC.visibility_of_element_located(ActiveAssignment.Quit_Start_Tutorial_BTN))
        assert quit_start_tutorial_btn.is_displayed(), "Không tìm thấy nút Quit Start Tutorial trên trang Active Assignment"


