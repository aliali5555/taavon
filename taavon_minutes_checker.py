
import streamlit as st
import re

st.set_page_config(page_title="تحلیل صورتجلسه تعاونی", layout="centered")

st.title("🧾 سامانه بررسی صورتجلسه شرکت‌های تعاونی")
st.write("🔍 این ابزار به‌صورت خودکار صورتجلسه مجامع شرکت‌های تعاونی را بررسی می‌کند و انطباق آن با مقررات قانونی را می‌سنجد.")

# ورود متن صورتجلسه
sample_text = st.text_area("متن صورتجلسه را وارد یا جای‌گذاری کنید:", height=300)

def analyze_quorum(text):
    match = re.search(r"حاضرین:\s*(\d+)\s*نفر.*?(\d+)\s*عضو", text)
    if match:
        present = int(match.group(1))
        total = int(match.group(2))
        quorum = total * 2 / 3  # فرض نوبت اول
        quorum_met = present >= quorum
        return {
            "present": present,
            "total": total,
            "quorum_required": quorum,
            "quorum_met": quorum_met
        }
    return None

def check_structure(text):
    return {
        "تاریخ جلسه": "✅" if "تاریخ جلسه" in text else "❌",
        "محل تشکیل": "✅" if "محل تشکیل" in text else "❌",
        "موضوع جلسه": "✅" if "موضوع جلسه" in text else "❌",
        "تعداد حاضرین": "✅" if "حاضرین" in text else "❌",
        "تصمیمات جلسه": "✅" if "نتایج انتخابات" in text else "❌",
        "امضا": "✅" if "امضا" in text else "❌"
    }

if st.button("🔎 تحلیل صورتجلسه"):
    if not sample_text.strip():
        st.warning("لطفاً ابتدا متن صورتجلسه را وارد کنید.")
    else:
        st.subheader("✅ تحلیل ساختار صورتجلسه:")
        structure = check_structure(sample_text)
        for item, status in structure.items():
            st.write(f"- {item}: {status}")

        st.subheader("📊 بررسی حد نصاب:")
        quorum = analyze_quorum(sample_text)
        if quorum:
            st.write(f"تعداد کل اعضا: {quorum['total']}")
            st.write(f"تعداد حاضرین: {quorum['present']}")
            st.write(f"حد نصاب موردنیاز: {quorum['quorum_required']:.2f}")
            if quorum['quorum_met']:
                st.success("✅ حد نصاب رعایت شده است.")
            else:
                st.error("❌ حد نصاب رعایت نشده است.")
        else:
            st.warning("اطلاعات حد نصاب در متن یافت نشد.")
