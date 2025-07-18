# KakaoTalk Chat Bot

A Python automation tool for sending messages to KakaoTalk chatrooms programmatically. This bot can send messages to specific chatrooms, verify delivery, and log all activities with detailed results.

## Features

- **Automated Message Sending**: Send messages to specific KakaoTalk chatrooms
- **Message Verification**: Confirms that messages were sent correctly
- **Comprehensive Logging**: Detailed CSV logs with timestamps and status tracking
- **Batch Operations**: Send messages to multiple chatrooms at once
- **Error Handling**: Robust error handling with detailed failure reasons

## Requirements

### Python Packages
```bash
pip install pywin32 pyautogui pyperclip pywinauto
```

### System Requirements
- Windows operating system
- KakaoTalk desktop application installed and logged in
- Python 3.x

## Installation

1. Clone or download the script
2. Install required packages:
   ```bash
   pip install pywin32 pyautogui pyperclip pywinauto
   ```
3. Ensure KakaoTalk is installed and you're logged in

## Usage

### Basic Usage

```python
from kakao_bot import KakaoChatConfig, KakaoChatService, KakaoBot

# Initialize components
config = KakaoChatConfig()
service = KakaoChatService()
bot = KakaoBot(config, service)

# Send a single message
bot.send_one("ChatRoom Name", "Your message here")

# Update configuration and send to multiple rooms
bot.update_message("ChatRoom 1", "Message 1")
bot.update_message("ChatRoom 2", "Message 2")
bot.send_all()
```

### Example Use Cases

The bot is particularly useful for:
- **Industrial Monitoring**: Send automated alerts about production line issues
- **Quality Control**: Notify teams about defect rates and inspection results
- **System Notifications**: Automated status updates and alerts

## Classes Overview

### KakaoChatConfig
Manages chat room configurations and message mappings.

### KakaoChatService
Core service class handling:
- Chat room opening and navigation
- Message sending and verification
- Logging and error handling

### KakaoBot
High-level interface providing:
- Single message sending
- Batch message operations
- Configuration management

## Logging

The bot automatically creates detailed logs at:
```
C:\Users\webal\OneDrive\Documents\0.LG_Project\Log\YYYY\MM\DD\HH\
```

Log files include:
- Timestamp
- Requested vs actual chatroom names
- Input vs output messages
- Success/failure status
- Detailed failure reasons

## How It Works

1. **Chatroom Search**: Uses Windows API to find and interact with KakaoTalk
2. **Message Input**: Copies text to clipboard and pastes into chat
3. **Verification**: Reads back the sent message to confirm delivery
4. **Logging**: Records all activities with comprehensive details
5. **Cleanup**: Closes chatroom windows after operation

## Error Handling

The bot handles various error scenarios:
- Chatroom not found
- Wrong chatroom opened
- Message sending failures
- Window interaction errors

All errors are logged with specific reasons for troubleshooting.

## Configuration Notes

- Update the `base_dir` path in `log_result()` method to match your system
- Ensure KakaoTalk is running and accessible
- The bot requires Windows desktop environment (uses win32 APIs)

## Limitations

- Windows-only (uses Windows API)
- Requires KakaoTalk desktop application
- Depends on GUI automation (may be affected by UI changes)
- Requires proper window focus and timing

## Safety Considerations

- Test with non-critical chatrooms first
- Monitor logs for any unexpected behavior
- Ensure proper timing delays to avoid overwhelming the system
- Keep KakaoTalk application updated

## Example Output

The bot generates CSV logs with entries like:
```
Time,Chatroom (Input),Chatroom (Output),Message (Input),Message (Output),Status,Reason for FAIL
2025-07-15 14:30:15,test 7,test 7,Hello World,Hello World,SUCCESS,
```

This tool provides a reliable way to automate KakaoTalk messaging for business or personal use cases requiring systematic communication.

