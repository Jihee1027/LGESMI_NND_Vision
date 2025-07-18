from message import KakaoChatConfig, KakaoChatService, KakaoBot
import random
import uuid
from datetime import datetime
import time
from Email import EmailSummaryExtractor
import os
import csv
from datetime import datetime

# Set up
config = KakaoChatConfig()
service = KakaoChatService()
bot = KakaoBot(config, service)

chatrooms = "LGESMI NND MESSAGE"
# chatrooms = "test 7"

prev_summary = None

class SimpleLogger:
    def __init__(self):
        self.start_time = datetime.now()
        self.start_time_str = self.start_time.strftime('%Y%m%d_%H%M%S')
        self.base_dir = r"C:\Users\CMIA41AS0001\LGVISION\Log_continue"

    def log_result(self, summary, status, x):
        now = datetime.now()

        year = self.start_time.strftime('%Y')
        month = self.start_time.strftime('%m')
        day = self.start_time.strftime('%d')
        hour = self.start_time.strftime('%H')

        folder_path = os.path.join(self.base_dir, year, month, day, hour)
        os.makedirs(folder_path, exist_ok=True)

        filename = f'kakao_log_{self.start_time_str}.csv'
        file_path = os.path.join(folder_path, filename)

        write_header = not os.path.exists(file_path)

        with open(file_path, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["Time", "Summary", "Status", "Int"])
            writer.writerow([
                now.strftime("%Y-%m-%d %H:%M:%S"),
                summary,
                status,
                x
            ])

logger = SimpleLogger()


try:
    while True:
        try:
            print("\n")
            extractor = EmailSummaryExtractor(
                email="lgesmivisionautomated@gmail.com",
                password="nuwm bbco vmso lngs",
                sender="junyoungbae@lgensol.com"
            )
            content, summary_log = extractor.get_latest_email()
            summary = extractor.extract_summary(content)
            

            if summary != prev_summary:
                prev_summary = summary
                result = bot.send_one(chatrooms, summary)
                print("\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": kakaotalk successfully sent\n")
                logger.log_result(summary_log, "Message Sent", 1)

                while bot.service.last_log_case_result[0] == False:
                    print("[!] Retry: Failed to send, trying again...")
                    time.sleep(2)  # optional: avoid spamming server
                    result = bot.send_one(chatrooms, summary)
            else:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Didn't send kakaotalk because content was same")
                logger.log_result(summary_log, "No Change", 0)

        except Exception as e:
            print(f"[ERROR] {e}")
            logger.log_result(summary_log if 'summary' in locals() else "N/A", f"[ERROR] {e}", -1)

            # Retry loop
            attempt = 1
            while True:
                try:
                    print(f"[Retry Attempt #{attempt}] Retrying send after error...")
                    result = bot.send_one(chatrooms, summary)
                    if bot.service.last_log_case_result[0]:
                        print(f"[{datetime.now()}] Retry succeeded.")
                        logger.log_result(summary_log, "Message Sent After Exception", 2)
                        break
                    else:
                        print(f"[{datetime.now()}] Retry failed. Will try again...\n")
                except Exception as send_exception:
                    print(f"[Retry Error] Another exception occurred: {send_exception}")
                    logger.log_result(summary_log, f"Retry Error: {send_exception}", -2)

                print(bot.service.last_log_case_result[0])
                attempt += 1
                time.sleep(2)

        finally:
            time.sleep(30)

except KeyboardInterrupt:
    print("\n[!] Program stopped by user.")
