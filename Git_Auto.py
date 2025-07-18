import os
from datetime import datetime

# 🔧 Customize this path to your project folder
PROJECT_PATH = r"C:\Users\webal\OneDrive\Documents\0.LG_Project\0.KakaoTalk_BOT"

# 📦 Your commit message format
COMMIT_MESSAGE = f"Auto update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def auto_push():
    os.chdir(PROJECT_PATH)
    
    print("🔁 Updating files...")
    os.system("git add -A")

    print("💬 Committing...")
    os.system(f'git commit -m "{COMMIT_MESSAGE}"')

    print("📤 Pushing to GitHub...")
    os.system("git push")

    print("✅ Done!")

if __name__ == "__main__":
    auto_push()
