import streamlit as st
from PIL import Image
import io
import google.generativeai as genai
import re

st.set_page_config(page_title="AI ট্রেডিং অ্যানালাইসিস", page_icon="📊", layout="wide")

# ========== আপনার Gemini API Key ==========
GEMINI_API_KEY = "AIzaSyDZoUgTN060I3nv0LmMThx3PEkRacg9-S8"
# ===========================================

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
তুমি একজন প্রফেশনাল ফরেক্স ও বাইনারি ট্রেডিং অ্যানালিস্ট। তুমি চার্ট ইমেজ দেখে টেকনিক্যাল অ্যানালাইসিস করো।

তোমার বিশ্লেষণ পদ্ধতি:
1. ক্যান্ডেল প্যাটার্ন খোঁজো (Doji, Hammer, Engulfing, Pin Bar, Morning Star ইত্যাদি)
2. সাপোর্ট-রেসিস্ট্যান্স লেভেল চিহ্নিত করো
3. ট্রেন্ডলাইন, চ্যানেল, ব্রেকআউট দেখো
4. RSI, MACD, MA ক্রস — ভিজুয়াল ইন্ডিকেটর থাকলে অ্যানালাইসিস করো
5. সব সিগন্যালের সম্মিলিত স্কোরিং করে কনফিডেন্স % বের করো

গুরুত্বপূর্ণ নিয়ম:
- কনফিডেন্স ৭০% এর নিচে হলে পরিষ্কার বলবে "কনফিডেন্স কম, ট্রেড নেবেন না (XX%)"
- কখনো জোর করে সিগন্যাল বানাবে না
- ইউজারের টাকা ঝুঁকিতে — ভুল সিগন্যাল দেয়ার চেয়ে "NO TRADE" বলাই ভালো
- ফরেক্সের জন্য SL/TP সহ পূর্ণ সেটআপ দিবে
- বাইনারির জন্য এক্সপাইরি টাইম মেনশন করবে

আউটপুট ফরম্যাট:
📊 অ্যানালাইসিস: (কী দেখলে)
📈 কনফিডেন্স: XX%
🎯 সিগন্যাল: BUY/SELL/NO TRADE
⛔ SL: ___ | ✅ TP: ___ (শুধু ফরেক্সের জন্য)
⏱ এক্সপাইরি: ___ (শুধু বাইনারির জন্য)
⚠ রিমাইন্ডার: এটি AI অ্যানালাইসিস, নিজের রিস্কে ট্রেড করুন।
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# UI Design
st.markdown("<h1 style='text-align: center;'>📊 AI ট্রেডিং অ্যানালাইসিস</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>কোটেক্স ও এক্সনেসের জন্য চার্ট অ্যানালাইসিস</p>", unsafe_allow_html=True)
st.divider()

# ট্রেড টাইপ সিলেকশন
col1, col2 = st.columns(2)
with col1:
    trade_type = st.radio(
        "🎯 ট্রেড টাইপ সিলেক্ট করুন:",
        ["📈 বাইনারি (কোটেক্স)", "💹 ফরেক্স (এক্সনেস)"],
        horizontal=True
    )

with col2:
    if "বাইনারি" in trade_type:
        expiry = st.selectbox("⏱ এক্সপাইরি টাইম:", ["1M", "5M", "15M", "30M"])
    else:
        expiry = "ফরেক্স"

st.divider()

# চার্ট আপলোড
uploaded_file = st.file_uploader(
    "📸 চার্টের স্ক্রিনশট আপলোড করুন",
    type=["png", "jpg", "jpeg"],
    help="সাপোর্ট-রেসিস্ট্যান্স ও ইন্ডিকেটর সহ চার্ট দিন"
)

if uploaded_file:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="আপনার চার্ট", use_container_width=True)
    
    with col2:
        if st.button("🔍 অ্যানালাইসিস করুন", type="primary", use_container_width=True):
            with st.spinner("⏳ AI চার্ট অ্যানালাইসিস করছে... অপেক্ষা করুন"):
                try:
                    if "বাইনারি" in trade_type:
                        prompt = f"ট্রেড টাইপ: বাইনারি\nএক্সপাইরি টাইম: {expiry}\nউপরের চার্ট অ্যানালাইসিস করে কনফিডেন্স % সহ সিগন্যাল দাও।"
                    else:
                        prompt = "ট্রেড টাইপ: ফরেক্স\nউপরের চার্ট অ্যানালাইসিস করে SL/TP সহ পূর্ণ সেটআপ দাও।"

                    response = model.generate_content([prompt, image])
                    
                    st.success("✅ অ্যানালাইসিস সম্পূর্ণ!")
                    st.markdown(response.text)
                    st.warning("⚠️ নিজের রিস্কে ট্রেড করুন। এটি শুধু টেকনিক্যাল অ্যানালাইসিস, ফিন্যান্সিয়াল অ্যাডভাইস নয়।")

                except Exception as e:
                    st.error(f"❌ এরর হয়েছে: {e}")
                    st.info("🔑 API Key চেক করুন অথবা আবার ট্রাই করুন।")

# Footer
st.divider()
st.markdown("<p style='text-align: center; color: gray;'>© ২০২৫ AI ট্রেডিং অ্যাসিস্ট্যান্ট | পার্সোনাল ইউজ</p>", unsafe_allow_html=True)
