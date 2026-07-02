
import streamlit as st
from PIL import Image
import io
import google.generativeai as genai
import re

st.set_page_config(page_title="AI ট্রেডিং অ্যানালাইসিস", page_icon="📊")

# ========== আপনার API Key ==========
GEMINI_API_KEY = "AQ.Ab8RN6J83KUvmO-pv7W34aJ5a7mwic3azgDbLXS4w0P-OvFA6g"  # ← এখানে বসান
# ===================================

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
তুমি একজন প্রফেশনাল ফরেক্স ও বাইনারি ট্রেডিং অ্যানালিস্ট।
চার্ট ইমেজ দেখে টেকনিক্যাল অ্যানালাইসিস করো।

গুরুত্বপূর্ণ নিয়ম:
- কনফিডেন্স ৭০% এর নিচে হলে বলবে "ট্রেড নেবেন না"
- ফরেক্সের জন্য SL/TP দিবে
- বাইনারির জন্য এক্সপাইরি টাইম দিবে

আউটপুট:
📊 অ্যানালাইসিস
📈 কনফিডেন্স: XX%
🎯 সিগন্যাল: BUY/SELL/NO TRADE
⛔ SL / ✅ TP (ফরেক্স)
⏱ এক্সপাইরি (বাইনারি)
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

st.title("📊 AI ট্রেডিং অ্যানালাইসিস")
st.write("কোটেক্স ও এক্সনেসের জন্য চার্ট অ্যানালাইসিস")

trade_type = st.radio("ট্রেড টাইপ:", ["বাইনারি (কোটেক্স)", "ফরেক্স (এক্সনেস)"])

if "বাইনারি" in trade_type:
    expiry = st.selectbox("এক্সপাইরি টাইম:", ["1M", "5M", "15M"])
else:
    expiry = "ফরেক্স"

uploaded_file = st.file_uploader("চার্টের স্ক্রিনশট আপলোড করুন", type=["png", "jpg", "jpeg"])

if uploaded_file and st.button("অ্যানালাইসিস করুন 🚀"):
    with st.spinner("🔍 অ্যানালাইসিস চলছে..."):
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="আপনার চার্ট", use_container_width=True)

            if "বাইনারি" in trade_type:
                prompt = f"ট্রেড টাইপ: বাইনারি\nএক্সপাইরি টাইম: {expiry}\nউপরের চার্ট অ্যানালাইসিস করে কনফিডেন্স % সহ সিগন্যাল দাও।"
            else:
                prompt = "ট্রেড টাইপ: ফরেক্স\nউপরের চার্ট অ্যানালাইসিস করে SL/TP সহ পূর্ণ সেটআপ দাও।"

            response = model.generate_content([prompt, image])
            st.success("✅ অ্যানালাইসিস:")
            st.markdown(response.text)
            st.warning("⚠️ নিজের রিস্কে ট্রেড করুন। এটি শুধু টেকনিক্যাল অ্যানালাইসিস।")

        except Exception as e:
            st.error(f"❌ এরর: {e}")
