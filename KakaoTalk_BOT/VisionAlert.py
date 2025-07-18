import requests
import json
import csv
import os
import logging
import time
from datetime import datetime, timezone, timedelta
import win32com.client as win32

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class LotInfoFetcher:
    def __init__(self):
        self.lot_id_counters = {}
        self.formatted_messages = []

    def fetch_and_process(self):
        headers = {
            "accept": "application/json",
            "authorization": "vJhKxImcxWJUX+n98PnAYnN/3CZKSg1i3W9Jg2V2qeWtTSgInn3GPWatrvsHV92HGCDZeM0AeD72TogjZZxvXIBO0XUz7DpBFTq3NiLbNKlUIM8feoCOdAEarj1Cdx/0cEkAw6YQVh3PKmd8MaJl/2Zxn5FNI7/vAbJEl73k/HuvWP1WpcLiaw0Gj1ryiTiAam6PJQR6bX+z2pemriW1uu03/oSOLjiFdYOeknlUjy5EMNkoOXp2qAazqf/crdcT",
            "content-type": "application/json",
            "userfacility": "S8",
            "userid": "junyoungbae",
            "userlangid": "ko-KR",
            "userplant": "G381",
            "x-language-code": "ko"
        }

        now = datetime.now(timezone.utc)
        one_day_ago = now - timedelta(days=1)

        def fmt(dt): return dt.strftime('%Y%m%d000000')

        url = "http://spcp-mi.lgensol.com:8082/spcp/battery/searchDefectRate"

        bodies = [
            {
                "equipGroupId": "NND",
                "lineId": "S8E03",
                "equipmentIds": ["G2ANND051", "G2ANND05A", "G2ANND061", "G2ANND06A", "G2ANND071", "G2ANND07A"],
                "inspEquipIds": ["INTEGRATION"],
                "apdTable": "TB_SPC_APD_ACP_ASSY_H01",
                "apdEtcTable": "TB_SPC_APD_ACP_ASSY_DETAIL_ETC_H01",
                "apdTableInfo": {
                    "EQUIPMENT_GROUP_ID": "NND",
                    "PROCESS_GROUP_ID": "A",
                    "TARGET_TABLE_NAME": "TB_SPC_APD_ACP_ASSY_H01",
                    "DEFECT_INFO": "TB_SPC_APD_ACP_ASSY_DETAIL_DEFECT_H01",
                    "TABLE_NO": "01",
                    "ETC": "TB_SPC_APD_ACP_ASSY_DETAIL_ETC_H01",
                    "DIMENSION_INFO": "TB_SPC_APD_ACP_ASSY_DETAIL_DIMENSION_H01",
                    "ALIGN_INFO": "TB_SPC_APD_ACP_ASSY_DETAIL_ALIGN_H01",
                    "PROD_TYPE": "ACP",
                    "IQ_INFO": "TB_SPC_APD_ACP_ASSY_DETAIL_IQ_H01"
                },
                "fromDate": fmt(now),
                "toDate": fmt(now),
                "endTime": now.isoformat() + "Z",
                "startTime": one_day_ago.isoformat() + "Z",
                "txnType": "ASSY",
                "userId": "junyoungbae",
                "langCode": "ko-KR",
                "langId": "ko-KR",
                "prodType": "ACP",
                "facilityCode": "S8",
                "idType": "lotId",
                "laneId": "ALL",
                "querySeq": "1",
                "idSearchFlag": False
            },
            {
                "equipGroupId": "NND",
                "lineId": "S8E04",
                "equipmentIds": ["G2ANND081", "G2ANND08A", "G2ANND091", "G2ANND09A", "G2ANND101", "G2ANND10A"],
                "inspEquipIds": ["FOIL-EXP", "INTEGRATION"],
                "apdTable": "TB_SPC_APD_ACP_ASSY_H01",
                "apdEtcTable": "TB_SPC_APD_ACP_ASSY_DETAIL_ETC_H01",
                "apdTableInfo": {
                    "EQUIPMENT_GROUP_ID": "NND",
                    "PROCESS_GROUP_ID": "A",
                    "TARGET_TABLE_NAME": "TB_SPC_APD_ACP_ASSY_H01",
                    "DEFECT_INFO": "TB_SPC_APD_ACP_ASSY_DETAIL_DEFECT_H01",
                    "TABLE_NO": "01",
                    "ETC": "TB_SPC_APD_ACP_ASSY_DETAIL_ETC_H01",
                    "DIMENSION_INFO": "TB_SPC_APD_ACP_ASSY_DETAIL_DIMENSION_H01",
                    "ALIGN_INFO": "TB_SPC_APD_ACP_ASSY_DETAIL_ALIGN_H01",
                    "PROD_TYPE": "ACP",
                    "IQ_INFO": "TB_SPC_APD_ACP_ASSY_DETAIL_IQ_H01"
                },
                "fromDate": fmt(now),
                "toDate": fmt(now),
                "endTime": now.isoformat() + "Z",
                "startTime": one_day_ago.isoformat() + "Z",
                "txnType": "ASSY",
                "userId": "junyoungbae",
                "langCode": "ko-KR",
                "langId": "ko-KR",
                "prodType": "ACP",
                "facilityCode": "S8",
                "idType": "lotId",
                "laneId": "ALL",
                "querySeq": "1",
                "idSearchFlag": False
            }
        ]

        all_results = []
        for body in bodies:
            try:
                #Make the POST request
                response = requests.post(url, headers=headers, json=body, timeout=30)
                #Check for HTTP errors
                response.raise_for_status()
                #Pares JSON response
                result = response.json()
                #Accumualte results
                all_results.extend(result)
            except Exception as e:
                logging.error(f"Error fetching data: {e}")

        return all_results

    def format_latest_info(self, result_data):
        latest_info_by_lane = {}
        for record in result_data:
            lane = record.get("LANE_NAME")
            timestamp = record.get("INSPECTION_END_DATE")
            # Skip records with missing lane or timestamp
            if not lane or not timestamp:
                continue

            # Keep only the latest record per Lane
            if lane not in latest_info_by_lane or timestamp > latest_info_by_lane[lane]["timestamp"]:
                latest_info_by_lane[lane] = {
                    "timestamp": timestamp,
                    "line": record.get("EQUIPMENT_NAME"),
                    "equipid": record.get("VISION_TYPE_CODE"),
                    "lot_id": record.get("LOT_ID"),
                    "ng_rate": record.get("NG_RATE"),
                    "ng_count": record.get("NG_COUNT"),
                    "surface_ng": record.get("APPEARANCE_NG_COUNT"),
                    "dimension_ng": record.get("DIMENSION_NG_COUNT")
                }

        messages = []
        for lane, info in latest_info_by_lane.items():
            try:
                inspection_time = datetime.strptime(info['timestamp'], '%Y-%m-%d %H:%M:%S')
            except:
                continue

            diff = datetime.now() - inspection_time
            if diff.total_seconds() < 3600 and info["ng_count"] >= 35:
                lot_id = info["lot_id"]
                if self.lot_id_counters.get(lot_id, 0) < 2:
                    msg = (
                        f"{info['line']} {info['equipid']} LOT_ID: {lot_id} has NG Rate of {info['ng_rate']}% "
                        f"at {info['timestamp']}. Total defect count is {info['ng_count']}. "
                        f"Surface defect count: {info['surface_ng']}, Dimension defect count: {info['dimension_ng']}. "
                        f"Please Check!!"
                    )
                    messages.append(msg)
                    self.lot_id_counters[lot_id] = self.lot_id_counters.get(lot_id, 0) + 1

        return messages

    def write_to_csv_and_send_email(self, data):
        base_dir = r"C:\documents\0.LG_project\Log"
        current_time = datetime.now()
        date_folder = current_time.strftime("%Y-%m-%d")
        current_folder_path = os.path.join(base_dir, date_folder)
        os.makedirs(current_folder_path, exist_ok=True)

        filename = os.path.join(current_folder_path, f"alarm_log_{current_time.strftime('%Y-%m-%d')}.csv")
        file_exists = os.path.isfile(filename)

        try:
            with open(filename, 'a', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Timestamp", "Alarm Message"])

                for element in data:
                    writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), element])
            logging.info("Data written to CSV.")
        except Exception as e:
            logging.error(f"Error writing to CSV: {e}")

    def send_csv_at_1159(self):
        current_time = datetime.now()
        start_time = datetime(current_time.year, current_time.month, current_time.day, 23, 50)
        end_time = datetime(current_time.year, current_time.month, current_time.day, 23, 59)
        flag_file = os.path.join(r"C:\documents\0.LG_project\Log", f"email_sent_{current_time.strftime('%Y-%m-%d')}.flag")

        if not os.path.exists(flag_file) and start_time <= current_time <= end_time:
            try:
                csv_filename = f"alarm_log_{current_time.strftime('%Y-%m-%d')}.csv"
                csv_path = os.path.join(r"C:\documents\0.LG_project\Log", current_time.strftime("%Y-%m-%d"), csv_filename)
                self.send_email_with_attachment(csv_path)

                with open(flag_file, 'w') as f:
                    f.write("sent")
                logging.info("CSV email sent and flag created.")
            except Exception as e:
                logging.error(f"Failed to send email: {e}")

    def send_email_with_attachment(self, attachment_path):
        today_date = datetime.now().strftime('%Y-%m-%d')
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)

        mail.To = "junyoungbae@lgensol.com"
        mail.Subject = f"{today_date} Notching alert log"
        mail.Body = f"Attached is the daily notching alarm log for {today_date}.\n\nPlease review any abnormalities."

        try:
            mail.Attachments.Add(attachment_path)
            mail.Send()
            logging.info("Email sent successfully.")
        except Exception as e:
            logging.error(f"Error sending email: {e}")

# Main loop: fetch every minute, log alerts, send email at 11:59 PM

if __name__ == "__main__":
    fetcher = LotInfoFetcher()

    while True:
        try:
            result = fetcher.fetch_and_process()
            messages = fetcher.format_latest_info(result)

            if messages:
                fetcher.write_to_csv_and_send_email(messages)

            fetcher.send_csv_at_1159()
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")

        time.sleep(60)  # Run every 60 seconds

