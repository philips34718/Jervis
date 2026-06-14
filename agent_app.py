import streamlit as st
import json
import requests
from datetime import datetime

# এজেন্ট ড্যাশবোর্ড সেটআপ
st.set_page_config(page_title="TBS Multi-Channel Dispatch Agent", page_icon="🤖", layout="wide")
st.title("🤖 TBS AI Multi-Channel Dispatch Agent (v1.0)")
st.caption("এটি একটি অ্যাডভান্সড ওয়ার্কফ্লো এজেন্ট। নিউজ ইনপুট দিন, এজেন্ট বাকি প্ল্যাটফর্মের ট্র্যাকিং হ্যান্ডেল করবে।")

# অটোমেশন হুক (n8n বা অন্য কোনো ফ্রি অটোমেশন টুলের Webhook URL এখানে বসানো যাবে)
# আপাতত এটি অপশনাল, খালি থাকলেও অ্যাপ চমৎকার কাজ করবে
webhook_url = st.sidebar.text_input("Webhook URL (n8n/Make):", type="password", placeholder="https://primary-production.news.site/...")

# সেশন স্টেট ট্র্যাকিং (ভুল এড়ানোর জন্য লাইভ মেমোরি)
if 'dispatch_history' not in st.session_state:
    st.session_state['dispatch_history'] = []

# --- ইনপুট হাব ---
st.markdown("### 📥 সেন্ট্রাল ডেটা ইনপুট")
col_in1, col_in2 = st.columns([2, 1])

with col_in1:
    raw_title = st.text_input("খবরের মূল হেডলাইন (Headline):", placeholder="এখানে মূল খবরটি লিখুন...")
    raw_desc = st.text_area("মূল বিবরণ (Description):", placeholder="কোম্পানির দেওয়া বিবরণটি এখানে দিন...")

with col_in2:
    editor_name = st.text_input("আপনার নাম/আইডি (Uploader Initials):", value="SEO-Specialist")
    content_type = st.selectbox("কন্টেন্টের ধরন (Format):", ["Regular Video", "Reels/Shorts Video", "Urgent Breaking"])

# --- এজেন্ট প্রসেসিং ইঞ্জিন ---
if st.button("🤖 রান অল প্ল্যাটফর্ম অটো-ইঞ্জিন 🚀"):
    if not raw_title:
        st.warning("দয়া করে একটি হেডলাইন দিন!")
    else:
        with st.spinner("AI এজেন্ট মেটাডেটা প্রসেস করছে এবং প্ল্যাটফর্ম ম্যাট্রিক্স তৈরি করছে..."):
            
            # নিখুঁত ক্লিন ও লোয়ারকেস প্রসেস
            clean_title = raw_title.strip()
            clean_desc = raw_desc.strip() if raw_desc else "No description provided."
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # প্ল্যাটফর্ম অনুযায়ী কাস্টম অপ্টিমাইজেশন ম্যাট্রিক্স
            payload = {
                "id": len(st.session_state['dispatch_history']) + 1,
                "timestamp": timestamp,
                "uploader": editor_name,
                "format": content_type,
                "youtube": {
                    "title": f"{clean_title} | The Business Standard"[:100],
                    "desc": f"{clean_desc}\n\n#tbs #tbsnews #banglanews"
                },
                "facebook": {
                    "title": clean_title,
                    "desc": f"{clean_desc}\n\n#tbs #tbsnews #facebookvideo"
                },
                "tiktok": {
                    "title": f"{clean_title} #tbs #tbsnews #tiktoknews #trending"[:150]
                },
                "cms_bangla": {
                    "title": clean_title,
                    "body": clean_desc
                },
                "cms_english": {
                    "title": clean_title,
                    "body": clean_desc
                }
            }
            
            # সেশন মেমোরিতে সেভ (জিরো মিস্টেক পলিসি)
            st.session_state['dispatch_history'].insert(0, payload)
            
            # যদি n8n/অটোমেশন ওয়েবপয়েন্ট কানেক্টেড থাকে তবে ব্যাকএন্ডে ডেটা পাঠিয়ে দেবে
            if webhook_url:
                try:
                    requests.post(webhook_url, json=payload, timeout=5)
                    st.sidebar.success("✅ n8n অটোমেশন এজেন্টে ডেটা পুশ করা হয়েছে!")
                except Exception:
                    st.sidebar.error("⚠️ Webhook কানেকশন ফেল করেছে, তবে লোকাল ডেটা রেডি।")

# --- এজেন্ট লাইভ ওয়ার্কস্পেস (The Command Center) ---
if st.session_state['dispatch_history']:
    current_job = st.session_state['dispatch_history'][0]
    
    st.markdown("---")
    st.markdown(f"### ⚡ বর্তমান সেশন ওয়ার্কস্পেস (রান টাইম: `{current_job['timestamp']}`)")
    
    # ৫টি প্ল্যাটফর্মের জন্য ৫টি কলাম লেআউট
    yt_col, fb_col, tt_col, cms_b_col, cms_e_col = st.columns(5)
    
    with yt_col:
        st.error("📺 YouTube Studio")
        st.caption("টাইটেল কপি করুন:")
        st.code(current_job['youtube']['title'], language="")
        st.caption("ডেসক্রিপশন কপি করুন:")
        st.code(current_job['youtube']['desc'], language="")
        st.checkbox("YT Upload Done", key=f"yt_{current_job['id']}")
        
    with fb_col:
        st.warning("🔵 FB Business Suite")
        st.caption("টাইটেল কপি করুন:")
        st.code(current_job['facebook']['title'], language="")
        st.caption("ডেসক্রিপশন কপি করুন:")
        st.code(current_job['facebook']['desc'], language="")
        st.checkbox("FB Upload Done", key=f"fb_{current_job['id']}")
        
    with tt_col:
        st.info("🎵 TikTok Creator")
        st.caption("রিলস/শর্টস ক্যাপশন কপি:")
        st.code(current_job['tiktok']['title'], language="")
        st.write("")
        st.write("")
        st.checkbox("TikTok Done", key=f"tt_{current_job['id']}")
        
    with cms_b_col:
        st.success("📰 TBS Bangla CMS")
        st.caption("হেডলাইন কপি করুন:")
        st.code(current_job['cms_bangla']['title'], language="")
        st.caption("বডি টেক্সট কপি করুন:")
        st.code(current_job['cms_bangla']['body'][:100] + "...", language="")
        st.checkbox("Bangla CMS Done", key=f"cmsb_{current_job['id']}")
        
    with cms_e_col:
        st.success("🇬🇧 TBS English CMS")
        st.caption("হেڈলাইন কপি করুন:")
        st.code(current_job['cms_english']['title'], language="")
        st.caption("বডি টেক্সট কপি করুন:")
        st.code(current_job['cms_english']['body'][:100] + "...", language="")
        st.checkbox("English CMS Done", key=f"cmse_{current_job['id']}")

    # --- অপারেশনাল হিস্ট্রি লগ ---
    st.markdown("---")
    with st.expander("📊 আজকের কাজের লাইভ লগ (History Log)"):
        st.write("ভুল সংশোধনের জন্য আপনার আজকের সেশনের হিস্ট্রি ট্র্যাক করা হচ্ছে:")
        st.json(st.session_state['dispatch_history'])
