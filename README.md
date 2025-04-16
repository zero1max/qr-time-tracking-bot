# QR Time Tracking Bot

A Telegram bot built with Aiogram 3.x that tracks employees' work hours using QR code verification. Users can only start their work time after scanning a QR code physically available at the office, ensuring location-based attendance.

## Features

- ⏱ Track work start and end time
- ✅ Verify presence using QR codes
- 🔐 Prevent cheating by enforcing QR scan at the office
- 🧾 Simple integration with Telegram
- 🖼 QR code generation and recognition support

## Tech Stack

- Python 3.10+
- Aiogram 3.x
- OpenCV (`cv2`)
- Pyzbar (for QR code reading)
- Pillow (for image processing)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/qr-time-tracking-bot.git
   cd qr-time-tracking-bot

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Run the bot:**
   ```bash
   python main.py

Usage

    Admin generates a QR code (valid for a specific time).

    Employees scan the QR code by sending a photo to the bot.

    The bot validates the QR and logs their "check-in" time.

    Optionally, a second scan or command can be used for "check-out".
