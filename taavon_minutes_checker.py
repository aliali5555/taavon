import streamlit as st
from PIL import Image
import pytesseract
import re

st.set_page_config(page_title="بررسی صورتجلسه تعاونی", page_icon="📄")

# --- عنوان و لوگو ---
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Iran_cooperative_emblem.svg/1200px-Iran_cooperative_emblem.svg.png", width=80)
st.title("📄 سامانه هوشمند بررسی صورتجلسه تعاونی")
st.markdown("این سامانه به شما کمک می‌کند بررسی کنید که صورتجلسه مجمع عمومی یا هیئت‌مدیره مطابق با ضوابط تعاونی‌ها هست یا نه.")

# --- بارگذاری فایل ---
uploaded_file = st.file_uploader("📤 لطفاً تصویر صورتجلسه را بارگذاری کنید", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    text = pytesseract.image_to_string(image, lang='fas')

    st.subheader("📝 متن استخراج‌شده از تصویر:")
    st.text(text)

    # --- بررسی موارد قانونی ---
    st.subheader("🔍 بررسی قانونی:")

    keywords = ["هیئت مدیره", "مجمع عمومی", "صورتجلسه", "شرکت تعاونی", "انتخاب اعضا", "بازرس", "تصویب ترازنامه"]
    found = [kw for kw in keywords if kw in text]

    if len(found) >= 3:
        st.success(f"✅ صورتجلسه شامل {len(found)} مورد از عناصر قانونی مهم است.")
        st.markdown("عبارات شناسایی‌شده:")
        for item in found:
            st.markdown(f"- ✅ **{item}**")
    else:
        st.error("❌ صورتجلسه فاقد برخی کلیدواژه‌های ضروری است. لطفاً بررسی کنید.")

    # --- اطلاعات تکمیلی (مثلاً تاریخ یا تعداد اعضا) ---
    st.subheader("📌 اطلاعات تکمیلی:")

    # پیدا کردن تاریخ شمسی
    date_match = re.search(r'\d{4}/\d{2}/\d{2}', text)
    if date_match:
        st.info(f"📅 تاریخ جلسه: {date_match.group()}")
    else:
        st.warning("⏳ تاریخ جلسه در متن یافت نشد.")

    # پیدا کردن تعداد اعضا (مثلاً "۵ نفر" یا "سه نفر")
    members_match = re.findall(r'(\d+|\w{2,4})\s*نفر', text)
    if members_match:
        st.info(f"👥 تعداد اعضای حاضر (تقریبی): {members_match[0]}")
    else:
        st.warning("👤 تعداد اعضای حاضر در جلسه مشخص نیست.")
