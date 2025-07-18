from pre_message import KakaoChatConfig, KakaoChatService, KakaoBot
import random
import uuid
from datetime import datetime
import time

# Set up
config = KakaoChatConfig()
service = KakaoChatService()
bot = KakaoBot(config, service)

chatrooms = [
    "김지희 (Jihee Kim)", "NND alert test 1", "NND alert test 2", 
    "NND alert test 3", "test 4", "test 5", "test 6", 
    "test 7", "test 8", "test 9", "test 10"
]

def generate_random_message():
    c_or_a = random.choice(["C", "A"])
    line = random.randint(1, 6)
    vision = random.choice(["INTEGRATION", "FOIL", "NGMARKING"])
    LOT_ID = uuid.uuid4().hex[:10]
    rate = random.uniform(0, 20)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    surface = random.randint(0, 100)
    dimension = random.randint(0, 100)
    total = surface + dimension
    return (
        f"MI2 NND({c_or_a}) #0{line} {vision} LOT_ID: {LOT_ID} has NG Rate of {rate:.2f}% "
        f"at {now}. Total defect count is {total}. Surface defect count: {surface}, "
        f"Dimension defect count: {dimension}. Please Check!!"
    )

try:
    while True:
        # Choose up to 30 chatrooms (without exceeding total number)
        num_rooms = random.randint(1, 30)
        selected_rooms = random.choices(chatrooms, k=num_rooms)  # allow duplicates

        print(f"\n[+] Sending messages to {num_rooms} rooms at {datetime.now().strftime('%H:%M:%S')}")
        for room in selected_rooms:
            msg = generate_random_message()
            print(f"→ {room}")
            result = bot.send_one(room, msg)
            time.sleep(1)  # short delay between messages

        print("[*] Waiting 5 minutes...\n")
        time.sleep(5 * 60)

except KeyboardInterrupt:
    print("\n[!] Program stopped by user.")