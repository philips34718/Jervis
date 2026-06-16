import streamlit as st
from googleapiclient.discovery import build
import re
import urllib.request
import urllib.parse
import urllib.error
import json

# পেজ সেটআপ
st.set_page_config(page_title="TBS Sovereign Agent 3.0", page_icon="🧠", layout="wide")
st.title("🧠 TBS Sovereign SEO Agent 3.0 (Super Brain Edition)")
st.caption("Google Gemini AI (Stable) এবং YouTube Live Search API দ্বারা চালিত সর্বাধুনিক অটো-পাইলট engine।")

# সাইডবার কন্ট্রোল প্যানেল
st.sidebar.header("🔑 AI Brain Activation")
gemini_key = st.sidebar.text_input("Gemini AI Key দিন (ফ্রি):", type="password")
api_key = st.sidebar.text_input("ইউটিউব Data API Key দিন:", type="password")

# ডাইনামিক মডেল সিলেক্টর
model_type = st.sidebar.selectbox(
    "🤖 AI Model সিলেক্ট করুন:",
    ["gemini-2.0-flash", "gemini-1.5-flash-latest", "gemini-2.5-flash"]
)

# স্পেস ট্রিম করা নিশ্চিত করা
clean_gemini_key = gemini_key.strip() if gemini_key else ""
clean_api_key = api_key.strip() if api_key else ""
clean_model_type = model_type.strip()

# 🧠 স্ট্রিমলিট লাইভ মেমোরি লক ইনিশিয়ালাইজেশন (যাতে টিক দিলে ডেটা না হারায়)
if 'ai_output' not in st.session_state:
    st.session_state['ai_output'] = None

# 🖥️ ট্যাব বিন্যাস
tab1, tab2 = st.tabs(["⚡ Super Brain Optimizer", "🔍 Deep Competitor Scraper"])

# ----------------- ⚡ ট্যাব ১: সুপার ব্রেন অপ্টিমাইজার -----------------
with tab1:
    st.markdown("### 📥 সেন্ট্রাল ডেটা ইনপুট হাব")
    
    # ডিরেক্ট প্ল্যাটফর্ম লিংক (ক্লিন ভিউ)
    st.markdown("""
    | 📺 YouTube Studio | 🔵 Meta Business Suite | 📰 TBS Bangla CMS | 🇬🇧 TBS English CMS |
    | :---: | :---: | :---: | :---: |
    """, unsafe_allow_html=True)
    
    headline = st.text_input("১. কোম্পানি থেকে দেওয়া মূল Headline বা নিউজ কনটেক্সট দিন:", placeholder="যেমন: প্রতিরক্ষায় আরও শক্তিশালী হবে বাংলাদেশ")
    given_desc = st.text_area("২. কোম্পানি থেকে দেওয়া বিবরণ (Description/Article Body):", placeholder="এখানে বিবরণটি পেস্ট করুন...")

    if st.button("🧠 সুপার ব্রেন অপ্টিমাইজেশন রান করুন 🚀"):
        if not headline:
            st.warning("আগে একটি হেডлайн ইনপুট দিন!")
        elif not clean_gemini_key:
            st.error("দয়া করে বাম পাশের সাইডবারে আপনার ফ্রি Gemini AI Key টি দিন।")
        else:
            with st.spinner(f"গুগল জেমিনি এআই ({clean_model_type}) আপনার নিউজের কন্টেক্সট ও অ্যালগরিদম অ্যানালাইসিস করছে..."):
                
                # --- এআই প্রম্পট ইঞ্জিনিয়ারিং ---
                prompt = f"""
                Act as an elite YouTube News SEO Specialist for 'The Business Standard (TBS)' news channel.
                Analyze the following news headline and description to generate hyper-optimized metadata for maximum views and organic reach.
                
                Current Context: Year 2026 Search Trends. All hashtags MUST be 100% lowercase with no spaces.
                
                News Headline: {headline}
                News Description: {given_desc if given_desc else "No description provided."}
                
                Strict Output Rules:
                Your response must contain these exact section markers so the app can parse them:
                [YT_TITLE]: Generate a high-CTR title. STRICT 100 character limit. Based on context, add smart English keywords/suffix (e.g., | Military | Budget | Politics). If the headline is too long, dynamically drop the branding '| The Business Standard' or shorten to '| TBS News' to keep it under 100 chars. Prioritize news keywords.
                [YT_DESC]: Keep the original description exactly as provided by the user. Do not add conversational fillers. At the end of the description, append 5 highly viral, completely lowercase hashtags (e.g., #tbsnews #banglanews).
                [YT_TAGS]: 15 highly searched semantic keywords separated by commas for the YouTube tags box.
                [COMMUNITY]: A catchy YouTube Community Post text. Include an engaging hook question, a 2-line summary, a Call-to-Action to watch the video, lowercase hashtags, and suggest a 4-option interactive Poll question.
                [FB_META]: Facebook Title and optimized Facebook Description with hashtags.
                [ENGLISH_CMS]: Translate or adapt the Bengali headline into a powerful, professional English headline for the TBS English Website CMS.
                """
                
                try:
                    url = f"https://generativelanguage.googleapis.com/v1/models/{clean_model_type}:generateContent?key={clean_gemini_key}"
                    payload = {"contents": [{"parts": [{"text": prompt}]}]}
                    headers = {'Content-Type': 'application/json'}
                    
                    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
                    with urllib.request.urlopen(req) as response:
                        res_data = json.loads(response.read().decode('utf-8'))
                        ai_response = res_data['candidates'][0]['content']['parts'][0]['text']
                    
                    # --- ডাটা পার্সিং ---
                    def extract_section(marker, text):
                        pattern = rf"\[{marker}\]:(.*?)(?=\[\w+\||\Z)"
                        match = re.search(pattern, text, re.DOTALL)
                        if match:
                            return match.group(1).strip()
                        try:
                            return text.split(f"[{marker}]:")[1].split("[")[0].strip()
                        except:
                            return "AI Generation failed for this block."

                    # সেশন স্টেটে ডেটা সেভ (লক) করা হচ্ছে
                    st.session_state['ai_output'] = {
                        "yt_title": extract_section("YT_TITLE", ai_response),
                        "yt_desc": extract_section("YT_DESC", ai_response),
                        "yt_tags": extract_section("YT_TAGS", ai_response),
                        "comm_post": extract_section("COMMUNITY", ai_response),
                        "fb_meta": extract_section("FB_META", ai_response),
                        "eng_cms": extract_section("ENGLISH_CMS", ai_response),
                        "headline_clean": headline.strip(),
                        "desc_clean": given_desc.strip() if given_desc else headline.strip()
                    }

                except urllib.error.HTTPError as he:
                    try:
                        err_body = json.loads(he.read().decode('utf-8'))
                        err_detail = err_body.get('error', {}).get('message', 'Unknown Google API Issue')
                        st.error(f"❌ গুগল এআই সার্ভার এরর (400): {err_detail}")
                    except:
                        st.error(f"❌ HTTP Error 400: {he.reason}")
                except Exception as e:
                    st.error(f"সাধারণ সমস্যা: {e}")

    # --- মেমোরি থেকে আউটপুট ডিসপ্লে (বাটন ক্লিকের বাইরে, ফলে টিক দিলে মুছবে না) ---
    if st.session_state['ai_output'] is not None:
        data = st.session_state['ai_output']
        
        st.markdown("---")
        st.success("🎯 মেটাডেটা সফলভাবে জেনারেট এবং মেমোরিতে লক হয়েছে। এখন নিচে নির্ভয়ে টিক দিন!")
        
        # ১. ইউটিউব ভিডিও সেকশনকে সবার ওপরে বড় করে দেখানো হলো
        st.error("📺 YouTube Video SEO Panel (প্রধান ভিউ)")
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            st.write("**AI Target Title (<100 Chars):**")
            st.code(data["yt_title"], language="")
        with col_t2:
            st.write("**🎯 সার্চ Tags (YouTube Tag Box):**")
            st.code(data["yt_tags"], language="")
            
        st.write("**📝 Optimized YouTube Description (কপি করার জন্য এটি বড় বক্সে দেওয়া হলো):**")
        st.text_area("ইউটিউব ডেসক্রিপশন বক্স (One-Click Copy):", value=data["yt_desc"], height=250)
        
        st.markdown("---")
        
        # ২. বাকি প্ল্যাটফর্মগুলোর কন্টেন্ট গ্রিড লেআউট
        row2_c1, row2_c2, row2_c3, row2_c4 = st.columns(4)
        
        with row2_c1:
            st.error("📊 YT Community Post & Poll")
            st.write("**কমিউনিটি কন্টেন্ট:**")
            st.code(data["comm_post"], language="")
            
        with row2_c2:
            st.warning("🔵 FB Business Suite")
            st.write("**ফেসবুক কন্টেন্ট মেটা:**")
            st.code(data["fb_meta"], language="")
            
        with row2_c3:
            st.success("📰 TBS Bangla CMS")
            st.write("**বাংলা ওয়েবসাইট হেডলাইন:**")
            st.code(data["headline_clean"], language="")
            st.write("**ভিডিও বডি বিবরণ:**")
            st.code(data["desc_clean"], language="")
            
        with row2_c4:
            st.success("🇬🇧 TBS English CMS")
            st.write("**অটো-অনূদিত ইংলিশ হেডলাইন:**")
            st.code(data["eng_cms"], language="")

        # --- ৩. নিখুঁত ডিস্ট্রিবিউশন চেকলিস্ট (টিক দিলে ডেটা উধাও হবে না) ---
        st.markdown("---")
        st.subheader("🚨 লাইভ পাবলিশিং চেকলিস্ট (এখানে জাস্ট টিক মার্ক দিন)")
        
        ch1, ch2, ch3, ch4, ch5 = st.columns(5)
        ch1.checkbox("YouTube Video Done", key="chk_yt_v")
        ch2.checkbox("YT Community Done", key="chk_yt_c")
        ch3.checkbox("Facebook Post Done", key="chk_fb")
        ch4.checkbox("Bangla CMS Done", key="chk_cms_b")
        ch5.checkbox("English CMS Done", key="chk_cms_e")

# ----------------- 🔍নোট: ফিক্সডস ট্যাব ২ (Deep Competitor Scraper) -----------------
with tab2:
    st.header("প্রতিদ্বন্দী ভিডিওর ভেতরের
