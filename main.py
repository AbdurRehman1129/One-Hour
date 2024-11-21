from appium import webdriver
from time import sleep

# Desired capabilities
desired_caps = {
    "platformName": "Android",
    "platformVersion": "13.5.0",
    "deviceName": "1089137443002481",
    "automationName": "UiAutomator2",
    "appPackage": "com.whatsapp",
    "appActivity": "com.whatsapp.Main",
    "noReset": True,
}

try:
    print("Connecting to Appium server...")
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    print("Connection successful! WhatsApp should now open on your device.")
    
    # Wait for WhatsApp to load
    sleep(5)
    
    print("Ready for interaction.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Ensure the Appium server is running, and desired capabilities are correct.")

finally:
    try:
        driver.quit()
        print("Driver session ended.")
    except NameError:
        print("Driver was not initialized, skipping quit.")
