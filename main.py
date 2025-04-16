import logging
import uuid
import qrcode
from io import BytesIO
from datetime import datetime, timedelta
import cv2
import numpy as np

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command

from PIL import Image
from pyzbar.pyzbar import decode

API_TOKEN = "Your_Bot_Token"
ADMIN_IDS = ["Admin_ID"]  # faqat adminlar QR yaratishi mumkin

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# QR tokenlar va vaqtlar
valid_tokens = {}  # token: expiry_time
user_times = {}  # user_id: start_time


def generate_qr_token():
    token = str(uuid.uuid4())
    expiry = datetime.now() + timedelta(hours=1)  # QR 1 soat amal qiladi
    valid_tokens[token] = expiry

    img = qrcode.make(token)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer, token



def extract_qr_data(image):
    # OpenCV yordamida rasmni o'qish
    image = np.array(image)  # PIL rasmni NumPy arrayga o'zgartirish
    qr_code_detector = cv2.QRCodeDetector()
    
    # QR kodni o'qish
    data, pts, qr_code = qr_code_detector.detectAndDecode(image)
    
    if data:
        return data  # QR koddan tokenni olish
    return None


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("👋 Ish vaqtini belgilovchi botga xush kelibsiz!\n\nAdmin QR kod yuboradi, siz esa uni skanerlab botga yuborasiz.")


@router.message(Command("generate_qr"))
async def generate_qr(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Sizda ruxsat yo'q.")
        return

    img_buf, token = generate_qr_token()
    
    # ⬇️ BufferedInputFile orqali yuboramiz
    file = BufferedInputFile(img_buf.getvalue(), filename="qr_code.png")

    await message.answer_photo(
        photo=file,
        caption=f"✅ QR kod generatsiya qilindi.\nKod faqat 1 soat amal qiladi.\nToken: <code>{token[:8]}...</code>"
    )


@router.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    buffer = BytesIO()
    await bot.download_file(file.file_path, destination=buffer)
    buffer.seek(0)

    image = Image.open(buffer)

    # 📝 Rasmni saqlash va tekshirish uchun
    image.save("debug_qr_test.jpg")
    
    token = extract_qr_data(image)

    if not token:
        await message.answer("❗️ QR kod o‘qilmadi. Iltimos, quyidagi maslahatlarga amal qiling:\n\n"
                              "📌 QR kodni to‘g‘ridan-to‘g‘ri suratga olib, fayl sifatida yuboring.\n"
                              "📸 Telegram'da *file* sifatida jo‘nating.")
        return

    # QR tokenni qaytarish
    await message.answer(f"✅ QR kod muvaffaqiyatli o‘qildi: {token}")


# Run
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import asyncio
    asyncio.run(dp.start_polling(bot))
