from imap_tools import MailBox, AND
import re

class EmailSummaryExtractor:
    def __init__(self, email, password, sender):
        self.email = email
        self.password = password
        self.sender = sender

    def get_latest_email(self):
        try:
            with MailBox('imap.gmail.com').login(self.email, self.password, initial_folder='INBOX') as mailbox:
                criteria = AND(from_=self.sender)
                messages = list(mailbox.fetch(criteria, limit=1, reverse=True))
                if messages:
                    latest_msg = messages[0]
                    print("Email subject : ", latest_msg.subject)
                    return (latest_msg.text or latest_msg.html or "No content", latest_msg.subject)
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def extract_summary(self, email_text):
        match = re.search(r"\*(.*?)\*", email_text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            filtered_lines = []
            for line in content.splitlines():
                if "________________________________" in line:
                    break
                filtered_lines.append(line)
            return "\n".join(filtered_lines).strip()
        return "*Summary section not found*"
    
    def split_summary(self, text: str):
        # Split the text at the word "Anode" and preserve the keyword
        parts = text.split("Anode", 1)

        if len(parts) < 2:
            return [text.strip()]  # Only one section (Cathode or other)

        cathode_part = parts[0].strip()
        anode_part = "Anode" + parts[1]  # Add back the keyword to Anode section

        return [cathode_part, anode_part]


if __name__ == "__main__":
      # Replace with your actual password securely
    extractor = EmailSummaryExtractor(
        email="lgesmivisionautomated@gmail.com",
        password = "nuwm bbco vmso lngs",
        sender="junyoungbae@lgensol.com"
    )
    content = extractor.get_latest_email()
    if content:
        summary = extractor.extract_summary(content)
        # print("Summary:\n", summary)
    else:
        print("No email found")
