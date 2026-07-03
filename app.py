import streamlit as st
from PIL import Image
import io
import base64
import requests

st.set_page_config(page_title="AI ট্রেডিং অ্যানালাইসিস", page_icon="📊", layout="wide")

# ========== আপনার OpenAI API Key ==========
OPENAI_API_KEY = "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"
# ==========================================

# OpenAI API কল ফাংশন
def analyze_chart_openai(image, trade_type, expiry=None):
    # ইমেজকে base64-তে কনভার্ট
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # প্রম্পট তৈরি
    if "বাইনারি" in trade_type:
        user_prompt = f"""তুমি একজন প্রফেশনাল ফরেক্স ও বাইনারি ট্রেডিং অ্যানালিস্ট।

ট্রেড টাইপ: বাইনারি
এক্সপাইরি টাইম: {expiry}

উপরের চার্ট অ্যানালাইসিস করে বলো:
- ক্যান্ডেল প্যাটার্ন কী দেখছ?
- সাপোর্ট-রেসিস্ট্যান্স লেভেল
- RSI, MACD, MA ট্রেন্ড
- সব মিলিয়ে কনফিডেন্স কত %?
- BUY নাকি SELL নাকি NO TRADE?

গুরুত্বপূর্ণ:
- কনফিডেন্স ৭০% এর নিচে হলে "NO TRADE" বলবে
- জোর করে সিগন্যাল দেবে না

আউটপুট ফরম্যাট:
📊 অ্যানালাইসিস: (কী দেখলে)
📈 কনফিডেন্স: XX%
🎯 সিগন্যাল: BUY/SELL/NO TRADE
⏱ এক্সপাইরি: {expiry}
⚠ নিজের রিস্কে ট্রেড করুন।"""
    else:
        user_prompt = """তুমি একজন প্রফেশনাল ফরেক্স ট্রেডিং অ্যানালিস্ট।

ট্রেড টাইপ: ফরেক্স

উপরের চার্ট অ্যানালাইসিস করে বলো:
- ক্যান্ডেল প্যাটার্ন কী দেখছ?
- সাপোর্ট-রেসিস্ট্যান্স লেভেল
- RSI, MACD, MA ট্রেন্ড
- সব মিলিয়ে কনফিডেন্স কত %?
- BUY নাকি SELL নাকি NO TRADE?
- SL এবং TP লেভেল দাও

গুরুত্বপূর্ণ:
- কনফিডেন্স ৭০% এর নিচে হলে "NO TRADE" বলবে
- জোর করে সিগন্যাল দেবে না
- Risk:Reward 1:2 বা তার বেশি হতে হবে

আউটপুট ফরম্যাট:
📊 অ্যানালাইসিস: (কী দেখলে)
📈 কনফিডেন্স: XX%
🎯 সিগন্যাল: BUY/SELL/NO TRADE
⛔ SL: ___ | ✅ TP: ___
⚠ নিজের রিস্কে ট্রেড করুন।"""

    # API কল
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.3
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ API এরর: {response.status_code}\n{response.text}"


# ═══════════════════════════
# UI Design
# ═══════════════════════════

st.markdown("<h1 style='text-align: center;'>📊 AI ট্রেডিং অ্যানালাইসিস</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>কোটেক্স ও এক্সনেসের জন্য | Powered by GPT-4o</p>", unsafe_allow_html=True)
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
        expiry = None

st.divider()

# চার্ট আপলোড
uploaded_file = st.file_uploader(
    "📸 চার্টের স্ক্রিনশট আপলোড করুন",
    type=["png", "jpg", "jpeg"],
    help="সাপোর্ট-রেসিস্ট্যান্স ও ইন্ডিকেটর সহ পরিষ্কার চার্ট দিন"
)

if uploaded_file:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="আপনার চার্ট", use_container_width=True)
    
    with col2:
        if st.button("🔍 অ্যানালাইসিস করুন", type="primary", use_container_width=True):
            with st.spinner("⏳ GPT-4o চার্ট অ্যানালাইসিস করছে... অপেক্ষা করুন (১৫-২০ সেকেন্ড)"):
                try:
                    result = analyze_chart_openai(image, trade_type, expiry)
                    
                    st.success("✅ অ্যানালাইসিস সম্পূর্ণ!")
                    st.markdown(result)
                    st.warning("⚠️ নিজের রিস্কে ট্রেড করুন। এটি শুধু টেকনিক্যাল অ্যানালাইসিস, ফিন্যান্সিয়াল অ্যাডভাইস নয়।")
                    st.info("💡 টিপ: কনফিডেন্স ৭০% এর নিচে হলে ট্রেড নেবেন না।")

                except Exception as e:
                    st.error(f"❌ এরর হয়েছে: {str(e)[:300]}")
                    st.info("🔑 API Key চেক করুন অথবা আবার ট্রাই করুন।")

# Footer
st.divider()
st.markdown("<p style='text-align: center; color: gray;'>© ২০২৫ AI ট্রেডিং অ্যাসিস্ট্যান্ট | Powered by GPT-4o</p>", unsafe_allow_html=True)
