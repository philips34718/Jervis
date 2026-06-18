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

# 🧠 স্ট্রিমলিট লাইভ মেমোরি লক (যাতে টিক দিলে ডেটা না হারায়)
if 'ai_output' not in st.session_state:
    st.session_state['ai_output'] = None

# 🖥️ ট্যাব বিন্যাস
tab1, tab2 = st.tabs(["⚡ Super Brain Optimizer", "🔍 Deep Competitor Scraper"])

# ----------------- ⚡ ট্যাব ১: সুপার ব্রেন অপ্টিমাইজার -----------------
with tab1:
    st.markdown("### 📥 সেন্ট্রাল ডেটা ইনপুট হাব")
    
    headline = st.text_input("১. কোম্পানি থেকে দেওয়া মূল Headline বা নিউজ কনটেক্সট দিন:", placeholder="যেমন: প্রতিরক্ষায় আরও শক্তিশালী হবে বাংলাদেশ")
    given_desc = st.text_area("২. কোম্পানি থেকে দেওয়া বিবরণ (Description/Article Body):", placeholder="এখানে বিবরণটি পেস্ট করুন...")

    if st.button("🧠 সুপার ব্রেন অপ্টিমাইজেশন রান করুন 🚀"):
        if not headline:
            st.warning("আগে একটি হেডলাইন ইনপুট দিন!")
        elif not clean_gemini_key:
            st.error("দয়া করে বাম পাশের সাইডবারে আপনার ফ্রি Gemini AI Key টি দিন।")
        else:
            with st.spinner(f"গুগল ஜেমিনি এআই ({clean_model_type}) আপনার নিউজ অ্যানালাইসিস করছে..."):
                
                # এআই শুধু রিলিজ এলিমেন্ট জেনারেট করবে, ফরম্যাটিং পাইথন নিজে হ্যান্ডেল করবে
                prompt = f"""
                Act as an elite YouTube News SEO Specialist for 'The Business Standard (TBS)'.
                Analyze the headline and description to provide elements for 2026 search trends.
                
                Headline: {headline}
                Description: {given_desc}
                
                Strict Output Rules:
                Your response must contain these exact section markers:
                [ENGLISH_TITLE]: Accurate high-quality professional English translation of the headline.
                [SUFFIX]: A clean English SEO suffix based on context (e.g., | Military | Budget | World Cup 2026).
                [CONTEXT_HASHTAGS]: 2 or 3 completely lowercase viral hashtags separated by spaces related specifically to the news context (DO NOT include brand names like tbs).
                [KEYWORDS]: 10 viral semantic keywords separated by commas for the tag box.
                [COMMUNITY]: A catchy text for YouTube Community Post with hook question, summary, and a 4-option Poll suggestion.
                """
                
                try:
                    url = f"https://generativelanguage.googleapis.com/v1/models/{clean_model_type}:generateContent?key={clean_gemini_key}"
                    payload = {"contents": [{"parts": [{"text": prompt}]}]}
                    headers = {'Content-Type': 'application/json'}
                    
                    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
                    with urllib.request.urlopen(req) as response:
                        res_data = json.loads(response.read().decode('utf-8'))
                        ai_response = res_data['candidates'][0]['content']['parts'][0]['text']
                    
                    # --- ডাটা পার্সিং লজিক ---
                    def extract_section(marker, text):
                        pattern = rf"\[{marker}\]:(.*?)(?=\[\w+\]|\Z)"
                        match = re.search(pattern, text, re.DOTALL)
                        if match:
                            return match.group(1).strip()
                        try:
                            return text.split(f"[{marker}]:")[1].split("[")[0].strip()
                        except:
                            return ""

                    eng_title = extract_section("ENGLISH_TITLE", ai_response)
                    ai_suffix = extract_section("SUFFIX", ai_response)
                    context_hashtags = extract_section("CONTEXT_HASHTAGS", ai_response)
                    ai_keywords = extract_section("KEYWORDS", ai_response)
                    comm_post = extract_section("COMMUNITY", ai_response)

                    # --- পাইথন ডিটারমিনিস্টিক ইঞ্জিন (আপনার রুল বুক অনুযায়ী সাজানো) ---
                    headline_clean = headline.strip()
                    desc_clean = given_desc.strip() if given_desc else headline_clean
                    
                    # ১. ইউনিভার্সাল ব্র্যান্ডেড হ্যাশট্যাগ কম্বো (ম্যাক্স ৩টি ব্র্যান্ড হ্যাশট্যাগ)
                    brand_hashtags = "#tbsnews #thebusinessstandard #tbs"
                    final_shared_hashtags = f"{brand_hashtags} {context_hashtags.lower()}"

                    # ২. টাইটেল ১০০ ক্যারেক্টার সিকিউরিটি লজিক
                    suffix_formatted = f" {ai_suffix}" if ai_suffix else ""
                    yt_title = f"{headline_clean}{suffix_formatted} | The Business Standard"
                    if len(yt_title) > 100:
                        yt_title = f"{headline_clean}{suffix_formatted} | TBS News"
                    if len(yt_title) > 100:
                        yt_title = f"{headline_clean}{suffix_formatted}"
                    if len(yt_title) > 100:
                        yt_title = headline_clean[:100]

                    # ৩. সুনির্দিষ্ট প্ল্যাটফর্ম ভিত্তিক ডেসক্রিপশন জেনারেটর (১ লাইন গ্যাপ লজিক)
                    yt_description = f"{eng_title}\n\n{desc_clean}\n\n{final_shared_hashtags}"
                    fb_post_text = f"{headline_clean}\n\n{final_shared_hashtags}"
                    tiktok_post_text = f"{headline_clean}\n{desc_clean}\n\n{final_shared_hashtags}"

                    # ৪. রেডি-টু-পেস্ট ট্যাগ বক্স কম্বিনেশন
                    brand_tags = "tbs, tbs news, the business standard"
                    yt_tags_box = f"{headline_clean}, {eng_title}, {brand_tags}, {ai_keywords}"

                    # লাইভ মেমোরি স্টেটে ডেটা সেভ (লক)
                    st.session_state['ai_output'] = {
                        "yt_title": yt_title,
                        "yt_tags": yt_tags_box,
                        "yt_desc": yt_description,
                        "fb_text": fb_post_text,
                        "tt_text": tiktok_post_text,
                        "comm_post": comm_post
                    }

                except urllib.error.HTTPError as he:
                    try:
                        err_body = json.loads(he.read().decode('utf-8'))
                        st.error(f"❌ গুগল এআই সার্ভার এরর (400): {err_body.get('error', {}).get('message', 'Unknown Issue')}")
                    except:
                        st.error(f"❌ HTTP Error 400")
                except Exception as e:
                    st.error(f"সাধারণ সমস্যা: {e}")

    # --- লাইভ মেমোরি থেকে ডেটা ডিসপ্লে (টিক দিলে ডেটা আর হারাবে না) ---
    if st.session_state['ai_output'] is not None:
        data = st.session_state['ai_output']
        
        st.markdown("---")
        st.success("🎯 মেটাডেটা সফলভাবে জেনারেট এবং মেমোরিতে লক হয়েছে। নিচে নির্ভয়ে টিক মার্ক দিন!")
        
        # 📺 ১. ইউটিউব ভিডিও সেকশন (প্রধান এবং বড় ভিউ)
        st.error("📺 YouTube Video Deployment Hub")
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            st.write("**AI Target Title (<100 Chars):**")
            st.code(data["yt_title"], language="")
        with col_t2:
            st.write("**🎯 সার্চ Tags (ডাইরেক্ট পেস্ট বক্স):**")
            st.code(data["yt_tags"], language="")
            
        st.write("**📝 YouTube Description Box (English Title + Bangla Desc + Gap + Hashtags):**")
        st.text_area("YouTube Copy Area:", value=data["yt_desc"], height=200)
        
        st.markdown("---")
        
        # 📱 ২. ফেসবুক, টিকটক এবং কমিউনিটি পোস্ট গ্রিড (১০০% ক্লিন)
        row2_c1, row2_c2, row2_c3 = st.columns(3)
        
        with row2_c1:
            st.warning("🔵 Facebook Post Hub")
            st.write("**FB Text (Headline + Gap + Hashtags):**")
            st.text_area("Facebook Copy Area:", value=data["fb_text"], height=250)
            
        with row2_c2:
            st.info("🎵 TikTok Dispatch Hub")
            st.write("**TikTok Caption (Headline + Desc + Gap + Hashtags):**")
            st.text_area("TikTok Copy Area:", value=data["tt_text"], height=250)
            
        with row2_c3:
            st.error("📊 YT Community Post & Poll")
            st.write("**কমিউনিটি কন্টেন্ট:**")
            st.text_area("Community Copy Area:", value=data["comm_post"], height=250)

        # --- ৩. নিখুঁত পাবলিশিং চেকলিস্ট (রিলোড প্রবলেম ফিক্সড) ---
        st.markdown("---")
        st.subheader("🚨 লাইভ পাবলিশিং চেকলিস্ট (এখানে জাস্ট টিক মার্ক দিন)")
        
        ch1, ch2, ch3, ch4, ch5 = st.columns(5)
        ch1.checkbox("YouTube Video Done", key="chk_yt_v")
        ch2.checkbox("YT Community Done", key="chk_yt_c")
        ch3.checkbox("Facebook Post Done", key="chk_fb")
        ch4.checkbox("TikTok Pushed", key="chk_tt")
        ch5.checkbox("Bangla/English CMS Done", key="chk_cms_all")

# ----------------- 🔍 ট্যাব ২: প্রতিদ্বন্দী স্ক্র্যাপার (সুরক্ষিত) -----------------
with tab2:
    st.header("প্রতিদ্বন্দী ভিডিওর ভেতরের আসল Tags এবং Hashtags স্ক্র্যাপার")
    keyword = st.text_input("সার্চ কিওয়ার্ডটি লিখুন:", placeholder="যেমন: বাজেট ২০২৬ বাংলাদেশ", key="tab2_kw")
    max_results = st.slider("কয়টি প্রতিদ্বন্দী ভিডিও অ্যানালাইসিস করবেন?", 5, 20, 10)

    if st.button("SEO এনালাইসিস শুরু করুন 🚀", key="tab2_btn"):
        if not clean_api_key:
            st.error("দয়া করে বাম পাশের সাইডবারে আপনার ইউটিউব Data API Key টি দিন।")
        elif not keyword:
            st.warning("আগে একটি কিওয়ার্ড লিখুন!")
        else:
            with st.spinner("ইউটিউব থেকে আসল Tags স্ক্র্যাপ করা হচ্ছে..."):
                try:
                    youtube = build('youtube', 'v3', developerKey=clean_api_key)
                    search_response = youtube.search().list(
                        q=keyword, part='snippet', maxResults=max_results, type='video', relevanceLanguage='bn'
                    ).execute()
                    
                    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
                    if not video_ids:
                        st.warning("কোনো ভিডিও পাওয়া যায়নি।")
                    else:
                        video_response = youtube.videos().list(id=",".join(video_ids), part='snippet').execute()
                        titles = []
                        all_hashtags_t2 = []
                        all_video_tags = []
                        
                        for item in video_response.get('items', []):
                            snippet_data = item.get('snippet', {})
                            titles.append(snippet_data.get('title', ''))
                            tags = snippet_data.get('tags', [])
                            all_video_tags.extend(tags)
                            hashtags = re.findall(r"#\w+", snippet_data.get('description', ''))
                            all_hashtags_t2.extend(hashtags)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("🔥 প্রতিদ্বন্দী চ্যানেলগুলোর টাইটেল ট্রেন্ড")
                            for i, t in enumerate(titles, 1):
                                st.write(f"**{i}.** {t}")
                        with col2:
                            st.subheader("🏷️ ট্রেন্ডিং হ্যাশট্যাগসমূহ")
                            if all_hashtags_t2:
                                hashtag_counts = Counter(all_hashtags_t2)
                                for tag, count in hashtag_counts.most_common(10):
                                    st.write(f" `{tag}` ({count} বার)")
                        
                        st.markdown("---")
                        st.subheader("🎯 কপি করার জন্য আসল ভিডিও ট্যাগ")
                        if all_video_tags:
                            tag_counts = Counter(all_video_tags)
                            top_tags = [tag for tag, count in tag_counts.most_common(20)]
                            st.text_area("Copy-Paste করার জন্য রেদি ট্যাগসমূহ:", value=", ".join(top_tags), height=120)
                except Exception as e:
                    st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
