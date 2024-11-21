import os
import time
import json

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear screen for Linux/Mac or Windows

def open_whatsapp():
    os.system("adb shell monkey -p com.whatsapp -c android.intent.category.LAUNCHER 1")
    print("WhatsApp opened.")

def click_agree_continue():
    time.sleep(3)
    os.system('adb shell input tap 540 2318')  # Coordinates for 'Agree and Continue'
    print("Tapped 'Agree and Continue'.")

def enter_phone_number(phone_number):
    time.sleep(3)
    os.system(f'adb shell input text "{phone_number}"')
    print(f"Entered phone number: {phone_number}")
    os.system('adb shell input tap 540 1585')  # Coordinates for "Next"
    print("Tapped 'Next'.")

def click_continue_or_yes():
    start_time = time.time()
    timeout = 60

    while time.time() - start_time < timeout:
        time.sleep(3)
        os.system('adb shell uiautomator dump /sdcard/ui.xml')
        os.system('adb pull /sdcard/ui.xml')

        with open('ui.xml', 'r', encoding='utf-8') as f:
            ui_content = f.read()

        if 'resource-id="android:id/button1"' in ui_content:
            os.system('adb shell input tap 813 1437')  # Coordinates for "Yes" button
            print("Tapped 'Yes'.")
            os.remove('ui.xml')
            break
        elif 'text="CONTINUE"' in ui_content:
            os.system('adb shell input tap 540 2220')  # Coordinates for "Continue"
            print("Tapped 'Continue'.")
            os.remove('ui.xml')
            break
        else:
            os.remove('ui.xml')
            print("Neither 'Continue' nor 'Yes' button found, retrying...")

    if time.time() - start_time >= timeout:
        print("Timeout reached, no button found.")

def click_ok_button():
    start_time = time.time()
    timeout = 60

    while time.time() - start_time < timeout:
        time.sleep(3)
        os.system('adb shell uiautomator dump /sdcard/ui.xml')
        os.system('adb pull /sdcard/ui.xml')

        with open('ui.xml', 'r', encoding='utf-8') as f:
            ui_content = f.read()

        if 'resource-id="android:id/button1"' in ui_content:
            os.system('adb shell input tap 813 1437')  # Coordinates for "OK" button
            print("Tapped 'OK'.")
            os.remove('ui.xml')
            return True  # Indicate that the "OK" button was found and tapped
        else:
            os.remove('ui.xml')
            print("'OK' button not found, retrying...")

    if time.time() - start_time >= timeout:
        print("Timeout reached, 'OK' button not found.")
    return False  # Indicate failure to find "OK" button

def click_wrong_number_button():
    start_time = time.time()
    timeout = 60

    while time.time() - start_time < timeout:
        time.sleep(3)
        capture_ui_dump()

        with open('window_dump.xml', 'r', encoding='utf-8') as f:
            ui_content = f.read()

        if 'text="Wrong number?"' in ui_content or 'content-desc="Wrong number?"' in ui_content:
            os.system('adb shell input tap 894 544')  # Coordinates for 'Wrong number?' button
            print("Tapped 'Wrong number?' button.")
            break
        else:
            print("'Wrong number?' button not found, retrying...")

    if time.time() - start_time >= timeout:
        print("Timeout reached, 'Wrong number?' button not found.")

def capture_ui_dump():
    os.system('adb shell uiautomator dump /sdcard/window_dump.xml')
    os.system('adb pull /sdcard/window_dump.xml .')
    print("UI dump captured.")

def load_json_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

def save_json_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def process_numbers(phone_numbers):
    one_hour_data = load_json_data("ONE_Hour.json")
    otp_sent_data = load_json_data("OTP_Sent.json")
    
    for phone_number in phone_numbers:
        enter_phone_number(phone_number)
        click_continue_or_yes()

        if click_ok_button():
            one_hour_data.append(phone_number)
            print(f"Saved {phone_number} to ONE_Hour.json.")
        else:
            otp_sent_data.append(phone_number)
            print(f"Saved {phone_number} to OTP_Sent.json.")

        click_wrong_number_button()

    save_json_data("ONE_Hour.json", one_hour_data)
    save_json_data("OTP_Sent.json", otp_sent_data)

def display_data(file_name):
    data = load_json_data(file_name)
    print(f"\nDisplaying data from {file_name}:")
    for index, number in enumerate(data, start=1):
        print(f"{index}. {number}")
    print(f"\nTotal: {len(data)} numbers.")

def main():
    while True:
        clear_screen()
        
        print("Select an option:")
        print("1. Enter phone numbers")
        print("2. Display One Hour numbers")
        print("3. Display OTP Sent numbers")
        print("4. Exit")
        
        choice = input("Enter your choice (1/2/3/4): ").strip()
        
        if choice == '1':
            phone_numbers_input = input("Enter phone numbers separated by commas: ").strip()
            phone_numbers = [number.strip() for number in phone_numbers_input.split(',')]
            open_whatsapp()
            click_agree_continue()
            process_numbers(phone_numbers)
        
        elif choice == '2':
            display_data("ONE_Hour.json")
            input("Press Enter to return to the menu...")
        
        elif choice == '3':
            display_data("OTP_Sent.json")
            input("Press Enter to return to the menu...")
        
        elif choice == '4':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
