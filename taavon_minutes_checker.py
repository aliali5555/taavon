import streamlit as st
from PIL import Image
import pytesseract

st.set_page_config(page_title="بررسی صورتجلسه تعاونی", page_icon="📄")

st.title("📄 بررسی قانونی بودن صورتجلسه تعاونی")

uploaded_file = st.file_uploader("لطفاً تصویر صورتجلسه هیئت‌مدیره یا مجمع عمومی را بارگذاری کنید", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    text = pytesseract.image_to_string(image, lang='fas')

    st.subheader("📝 متن استخراج‌شده:")
    st.text(text)

    st.subheader("⚖️ بررسی قانونی:")
    if "هیئت مدیره" in text and "مجمع عمومی" in text:
        st.success("✅ این صورتجلسه دارای عناصر قانونی اولیه است.")
    else:
        st.warning("⚠️ در متن صورتجلسه برخی واژه‌های کلیدی قانونی دیده نمی‌شود.")
