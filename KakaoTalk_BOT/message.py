import time
import win32con 
import win32api
import win32gui
import pyautogui
import pyperclip
import csv
import os
from datetime import datetime
import uuid

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
                self.log_case(chatroom_name, actual_title, text, code, searchedroom_name, "opened_wrong_chatroom") 
                win32gui.PostMessage(hwndMain, win32con.WM_CLOSE, 0, 0)

            else:
                try:
                    # Send the message
                    code = uuid.uuid4().hex[:8]
                    pyperclip.copy(f"chat code: {code}" + "\n\n" + text)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.5)
                    
                    pyautogui.press('enter')
                    time.sleep(1)

                    # Unique code confirmation
                    new_hwnd, searchedroom_name = self.unique_code_confirm(code, hwndMain)
            
                    # Check if the message actually sent
                    if searchedroom_name == chatroom_name:
                        self.log_case(chatroom_name, actual_title, text, code, searchedroom_name, "message_sent_desired_chatroom")
                        
                    else:
                        if searchedroom_name == "Integrated Search":
                            # Re_searching the code if not found
                            new_hwnd, searchedroom_name = self.re_unique_code_confirm(code)

                            if searchedroom_name == chatroom_name:
                                self.log_case(chatroom_name, actual_title, text, code, searchedroom_name, "message_sent_desired_chatroom2")
                        else:
                            self.log_case(chatroom_name, actual_title, text, code, searchedroom_name, "message_sent_wrong_chatroom")

                except Exception as e:
                     self.log_case(chatroom_name, actual_title, text, code, searchedroom_name, "N/A")

                hwndMain = new_hwnd
                win32gui.PostMessage(hwndMain, win32con.WM_CLOSE, 0, 0)
                time.sleep(1)
                
                integrated_hwnd = win32gui.GetForegroundWindow()
                integrated_window = win32gui.GetWindowText(integrated_hwnd)
                if integrated_window == "Integrated Search":
                    win32gui.PostMessage(integrated_hwnd, win32con.WM_CLOSE, 0, 0)

        else:
            self.log_case(chatroom_name, actual_title, text, code, searchedroom_name, "chatroom_not_found")

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
    
    def re_unique_code_confirm(self, code):
        time.sleep(0.5)
        pyautogui.keyDown('ctrl')
        pyautogui.press('f')
        time.sleep(0.1)
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        time.sleep(0.1)
        pyperclip.copy(code)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('down')
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(1)
        new_hwnd =  win32gui.GetForegroundWindow()
        searchedroom_name = win32gui.GetWindowText(new_hwnd)
        
        return new_hwnd, searchedroom_name
    
    def log_case(self, chatroom_desired, chatroom_opened, message_input, unique_code_search, chatroom_found, case, reason):
        match case:
            case "opened_wrong_chatroom":
                self.log_result(chatroom_desired, chatroom_opened, message_input, "", "FAIL", "Opend Wrong Chatroom: Message Not Sent")
                print (False, chatroom_desired, message_input)
                return (False, chatroom_desired, message_input)
            case "chatroom_not_found":
                self.log_result(chatroom_desired, "", message_input, "", "FAIL", "Chatroom Not Found: Message Not Sent")
                print (False, chatroom_desired, message_input)
                return (False, chatroom_desired, message_input)
            case "message_sent_desired_chatroom":
                self.log_result(chatroom_desired, chatroom_opened, message_input, unique_code_search, chatroom_found, "SUCCESS")
                print ("True2", chatroom_desired, message_input)
                return (True, chatroom_desired, message_input)
            case "message_sent_desired_chatroom2":
                self.log_result(chatroom_desired, chatroom_opened, message_input, unique_code_search, chatroom_found, "SUCCESS (CODE RECONFIRM)")
                print (True, chatroom_desired, message_input)
                return (True, chatroom_desired, message_input)
            case "message_sent_wrong_chatroom":
                self.log_result(chatroom_desired, chatroom_opened, message_input, unique_code_search, chatroom_found, "FAIL", "Message Sent to Wrong Chatroom")
                print (False, chatroom_desired, message_input)
                return (False, chatroom_desired, message_input)
            case "N/A":
                self.log_result(chatroom_desired, chatroom_opened, message_input, "", "", "FAIL", f"{str(reason)}: Message Not Sent")
                print (False, chatroom_desired, message_input)
                return (False, chatroom_desired, message_input)

    def log_result(self, chatroom_desired, chatroom_opened, message_input, unique_code_search, chatroom_found, status, reason_fail = ""):
        now = datetime.now()

        year = self.start_time.strftime('%Y')
        month = self.start_time.strftime('%m')
        day = self.start_time.strftime('%d')
        hour = self.start_time.strftime('%H')

        base_dir = r"C:\Users\webal\OneDrive\Documents\0.LG_Project\Log"
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
    text = "hello"
    bot.update_message(reciever, text)
    kakao_opentalk_names = ["김지희 (Jihee Kim)", "NND alert test 1", "NND alert test 2", "NND alert test 3", "test 4", "test 5", "test 6", "test 7", "test 8", "test 9", "test 10"]


    message = "MI2 NND(A) #02 INTEGRATION LOT_ID: 8EGB35NA02 has NG Rate of 7.33% at 2025-07-11 08:01:21. Total defect count is 47. Surface defect count: 36, Dimension defect count: 15. Please Check!!"

    # for i in range(100):
    #     selected_room = random.choice(kakao_opentalk_names)
    #     print(f"[{i+1}/100] Sending to: {selected_room}")
    #     bot.send_one(selected_room, message)
    #     time.sleep(0.5)

    bot.send_all()


if __name__ == "__main__":
    main()
