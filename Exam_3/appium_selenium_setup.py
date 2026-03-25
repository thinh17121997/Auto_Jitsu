import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from mobile_elements import LoginPage
from mobile_elements import HomePage
from mobile_elements import TabProfile
from mobile_elements import TabTutorial
from mobile_elements import ActiveAssignment


options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-5554'
options.automation_name = 'UiAutomator2'
options.app_package = 'com.axlehire.drive.staging'
options.app_activity = 'com.axlehire.drive.MainActivity'
options.auto_grant_permissions= True

appium_server_url = 'http://127.0.0.1:4723'
print("Đang khởi tạo kết nối tới Appium...")

try:
    driver = webdriver.Remote(appium_server_url, options=options)
    print("Kết nối thành công! Đã mở app trên điện thoại.")    
    time.sleep(10)
    login_page = LoginPage()
    home_page = HomePage()
    tab_profile = TabProfile()
    tab_tutorial = TabTutorial()
    active_assignment = ActiveAssignment()
    login_page.login(driver, "auto_244332", "Testing1!")
    home_page.navigate_tab_profile(driver)
    tab_profile.click_button_tutorial(driver)
    tab_tutorial.verify_title_tutorial(driver)
    tab_tutorial.click_assigned_route_btn(driver)
    active_assignment.verify_title_active_assignment(driver)
    active_assignment.click_start_tutorial_btn(driver)
    active_assignment.verify_quit_start_tutorial_btn(driver)

except (WebDriverException, TimeoutException) as e:
    print(f"Có lỗi xảy ra: {e}")
finally:
    if 'driver' in locals():
        print("Đang đóng driver...")
        driver.quit()
