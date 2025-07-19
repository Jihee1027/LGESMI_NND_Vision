import time
import win32con 
import win32api
import win32gui
import pyautogui
import pyperclip
import csv
import os
from datetime import datetime
from Log_Email import send_email_fail, send_email_success

class KakaoChatConfig:
    def __init__(self):
        self.chat_messages = {
        }

class KakaoChatService:
    def __init__(self):
        self.start_time = datetime.now()
        self.start_time_str = self.start_time.strftime('%Y%m%d_%H%M')

    def kakao_sendtext_and_close(self, chatroom_name, text):
        hwndMain = self.open_chatroom(chatroom_name)
        if hwndMain != 0:
            win32gui.SetForegroundWindow(hwndMain)
            time.sleep(0.1)


            actual_title = win32gui.GetWindowText(hwndMain)

            if chatroom_name not in actual_title:
                self.log_case(chatroom_name, actual_title, text, code, searchedroom_name, "opened_wrong_chatroom", "") 
                win32gui.PostMessage(hwndMain, win32con.WM_CLOSE, 0, 0)

            else:
                try:
                    # Send the message
                    code = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    logo = "*****LGESMI NND Alert*****\n"
                    pyperclip.copy(f"{code}" + "\n\n" + logo+ text)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.5)
                    
                    pyautogui.press('enter')
                    time.sleep(1)

                    # Unique code confirmation
                    new_hwnd, searchedroom_name = self.unique_code_confirm(code, hwndMain)
            
                    # Check if the message actually sent
                    if searchedroom_name == chatroom_name:
                        self.log_case(chatroom_name, actual_title, text, code, searchedroom_name, "message_sent_desired_chatroom", "")
                    else:
                        if searchedroom_name == "Integrated Search":
                            new_hwnd, searchedroom_name = self.unique_code_confirm(code, hwndMain)
                            if searchedroom_name == chatroom_name:
                                self.log_case(chatroom_name, actual_title, text, code, searchedroom_name, "message_sent_desired_chatroom", "")
                        else:
                            self.log_case(chatroom_name, actual_title, text, code, searchedroom_name, "message_sent_wrong_chatroom", "")

                except Exception as e:
                    self.log_case(chatroom_name, actual_title, text, code, searchedroom_name, "N/A", e)

                hwndMain = new_hwnd
                win32gui.PostMessage(hwndMain, win32con.WM_CLOSE, 0, 0)
                time.sleep(1)
                
                integrated_hwnd = win32gui.GetForegroundWindow()
                integrated_window = win32gui.GetWindowText(integrated_hwnd)
                if integrated_window == "Integrated Search":
                    win32gui.PostMessage(integrated_hwnd, win32con.WM_CLOSE, 0, 0)

        else:
            self.log_case(chatroom_name, "", text, "", "", "chatroom_not_found", "")

    # Enter for open_chatroom
    def SendReturn(sefl, hwnd):
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0) # Press key
        time.sleep(0.01)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0) # Unpress key

    def open_chatroom(self, chatroom_name):

        hwndkakao = win32gui.FindWindow(None, "KakaoTalk")
        hwndkakao_edit1 = win32gui.FindWindowEx( hwndkakao, None, "EVA_ChildWindow", None)
        hwndkakao_edit2_1 = win32gui.FindWindowEx( hwndkakao_edit1, None, "EVA_Window", None)
        hwndkakao_edit2_2 = win32gui.FindWindowEx( hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window", None)
        hwndkakao_edit3 = win32gui.FindWindowEx( hwndkakao_edit2_2, None, "Edit", None)

        # Search for chatroom
        win32api.SendMessage(hwndkakao_edit3, win32con.WM_SETTEXT, 0, chatroom_name)
        time.sleep(1) 
        self.SendReturn(hwndkakao_edit3)

        # Clear the search box
        time.sleep(1)
        win32api.SendMessage(hwndkakao_edit3, win32con.WM_SETTEXT, 0, "")
        time.sleep(1)

        hwndMain = win32gui.FindWindow(None, chatroom_name)

        return hwndMain
    
    def unique_code_confirm(self, code, hwndMain):
        pyautogui.keyDown('ctrl')
        pyautogui.press('f')
        time.sleep(0.5)
        pyperclip.copy(code)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('tab')   
        pyautogui.press('space')
        time.sleep(0.5)    
        win32gui.PostMessage(hwndMain, win32con.WM_CLOSE, 0, 0)
        pyautogui.press('enter')
        time.sleep(0.2)
        pyautogui.press('down')
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(0.5)
        new_hwnd = win32gui.GetForegroundWindow()
        searchedroom_name = win32gui.GetWindowText(new_hwnd)
        time.sleep(0.5)

        return new_hwnd, searchedroom_name
    
    def log_case(self, chatroom_desired, chatroom_opened, message_input, unique_code_search, chatroom_found, case, e):
        match case:
            case "opened_wrong_chatroom":
                self.log_result(chatroom_desired, chatroom_opened, message_input, "", "FAIL", "Opend Wrong Chatroom: Message Not Sent")
                print (False, chatroom_desired, message_input)
                self.last_log_case_result = (False, chatroom_desired, message_input)
                send_email_fail(chatroom_found)
                return (False, chatroom_desired, message_input)
            case "chatroom_not_found":
                self.log_result(chatroom_desired, "", message_input, "", "FAIL", "Chatroom Not Found: Message Not Sent")
                print (False, chatroom_desired, message_input)
                self.last_log_case_result = (False, chatroom_desired, message_input)
                send_email_fail(chatroom_found)
                return (False, chatroom_desired, message_input)
            case "message_sent_desired_chatroom":
                self.log_result(chatroom_desired, chatroom_opened, message_input, unique_code_search, chatroom_found, "SUCCESS")
                print (True, chatroom_desired, message_input)
                self.last_log_case_result = (True, chatroom_desired, message_input)
                send_email_success(chatroom_found)
                return (True, chatroom_desired, message_input)
            case "message_sent_wrong_chatroom":
                self.log_result(chatroom_desired, chatroom_opened, message_input, unique_code_search, chatroom_found, "FAIL", "Message Sent to Wrong Chatroom")
                print (False, chatroom_desired, message_input)
                self.last_log_case_result = (False, chatroom_desired, message_input)
                send_email_fail(chatroom_found)
                return (False, chatroom_desired, message_input)
            case "N/A":
                self.log_result(chatroom_desired, chatroom_opened, message_input, "", "", "FAIL", f"{str(e)}: Message Not Sent")
                print (False, chatroom_desired, message_input)
                self.last_log_case_result = (False, chatroom_desired, message_input)
                send_email_fail(chatroom_found)
                return (False, chatroom_desired, message_input)
            
    def log_result(self, chatroom_desired, chatroom_opened, message_input, unique_code_search, chatroom_found, status, reason_fail = ""):
        now = datetime.now()

        year = self.start_time.strftime('%Y')
        month = self.start_time.strftime('%m')
        day = self.start_time.strftime('%d')
        hour = self.start_time.strftime('%H')

        base_dir = r"C:\CMIA41AS0001\LGVISION\Log"
        folder_path = os.path.join(base_dir, year, month, day, hour)
        os.makedirs(folder_path, exist_ok=True)

        filename = f'kakao_log_{self.start_time_str}.csv'
        file_path = os.path.join(folder_path, filename)

        write_header = not os.path.exists(file_path)
        
        with open(file_path, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow([
                    "Time", "Chatroom(Desired)", "Chatroom(Opened)",
                    "Message Input", "Unique Code(Searched)", "Chatroom(Found)", "Status", "Reason(FAIL)"
                ])
            writer.writerow([
                now.strftime("%Y-%m-%d %H:%M:%S"),
                chatroom_desired,
                chatroom_opened,
                message_input,
                unique_code_search,
                chatroom_found,
                status,
                reason_fail
            ])

class KakaoBot:
    '''
    KakaoBot class to manage sending messages in KakaoTalk chatrooms.
    It uses KakaoChatConfig for configuration and KakaoChatService for sending messages.
    It can send messages to all chatrooms defined in the configuration or to a specific chatroom.
    '''
    def __init__(self, config: KakaoChatConfig, service: KakaoChatService):
        self.config = config
        self.service = service
    
    def send_all(self):
        '''
        Send all messages in the config to their respective chatrooms.
        '''
        for chatroom, message in self.config.chat_messages.items():
            self.service.kakao_sendtext_and_close(chatroom, message)
    
    def send_one(self, chatroom, message):
        '''
        Send a message to a specific chatroom.
        If the chatroom is not found, it will not send the message and return False.
        '''
        self.service.kakao_sendtext_and_close(chatroom, message)
    
    def update_message(self, chatroom, message):
        '''
        Update the message for a specific chatroom if needed.
        '''
        self.config.chat_messages[chatroom] = message

def main():
    config = KakaoChatConfig()
    service = KakaoChatService()
    bot = KakaoBot(config, service)
    
    reciever = "김지희 (Jihee Kim)"
    text = "HELLO"
    bot.update_message(reciever, text)


    bot.send_all()


if __name__ == "__main__":
    main()
