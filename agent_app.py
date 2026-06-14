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

# 🖥️ ট্যাব বিন্যাস
tab1, tab2 = st.tabs(["⚡ Super Brain Optimizer", "🔍 Deep Competitor Scraper"])

# ----------------- ⚡ ট্যাব ১: সুপার ব্রেন অপ্টিমাইজার -----------------
with tab1:
    st.markdown("### 📥 সেন্ট্রাল ডেটা ইনপুট হাব")
    
    # ডিরেক্ট প্ল্যাটফর্ম লিংক
    st.markdown("""
    | 🔗 YouTube Studio | 🔗 Meta Business Suite | 🔗 TikTok Upload | 🔗 TBS Bangla CMS | 🔗 TBS English CMS |
    | :---: | :---: | :---: | :---: | :---: |
    | [Open Studio](https://studio.youtube.com) | [Open Meta](https://business.facebook.com) | [Open TikTok](https://www.tiktok.com/creator-center/upload) | [Open Bangla CMS](https://tbsnews.net/bangla) | [Open English CMS](https://tbsnews.net) |
    """, unsafe_allow_html=True)
    
    headline = st.text_input("১. কোম্পানি থেকে দেওয়া মূল Headline বা নিউজ কনটেক্সট দিন:", placeholder="যেমন: প্রতিরক্ষায় আরও শক্তিশালী হবে বাংলাদেশ")
    given_desc = st.text_area("২. কোম্পানি থেকে দেওয়া বিবরণ (Description/Article Body):", placeholder="এখানে বিবরণটি পেস্ট করুন...")

    if st.button("🧠 সুপার ব্রেন অপ্টিমাইজেশন রান করুন 🚀"):
        if not headline:
            st.warning("আগে একটি হেডলাইন ইনপুট দিন!")
        elif not clean_gemini_key:
            st.error("দয়া করে বাম পাশের সাইডবারে আপনার ফ্রি Gemini AI Key টি দিন।")
        else:
            with st.spinner(f"গুগল জেমিনি এআই ({clean_model_type}) আপনার নিউজের কন্টেক্সট ও অ্যালগরিদম অ্যানালাইসিস করছে..."):
                
                # --- এআই প্রম্পট ইঞ্জিনিয়ারিং ---
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
                [TIKTOK_META]: A punchy, short TikTok/Reels caption packed with viral lowercase hashtags.
                [ENGLISH_CMS]: Translate or adapt the Bengali headline into a powerful, professional English headline for the TBS English Website CMS.
                """
                
                try:
                    url = f"https://generativelanguage.googleapis.com/v1/models/{clean_model_type}:generateContent?key={clean_gemini_key}"
                    payload = {"contents": [{"parts": [{"text": prompt}]}]}
                    headers = {'Content-Type': 'application/json'}
                    
                    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
                    with urllib.request.urlopen(req) as response:
                        res_data = json.loads(response.read().decode('utf-8'))
                        # ফিক্সড লাইন: এখানে contents এর বদলে সঠিক 'candidates' রেসপন্স ফরম্যাট ব্যবহার করা হয়েছে
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

                    yt_title = extract_section("YT_TITLE", ai_response)
                    yt_desc = extract_section("YT_DESC", ai_response)
                    yt_tags = extract_section("YT_TAGS", ai_response)
                    comm_post = extract_section("COMMUNITY", ai_response)
                    fb_meta = extract_section("FB_META", ai_response)
                    tt_meta = extract_section("TIKTOK_META", ai_response)
                    eng_cms = extract_section("ENGLISH_CMS", ai_response)

                    # --- আউটপুট ডিসপ্লে ---
                    st.markdown("---")
                    st.success(f"🎯 সুপার ব্রেন ({clean_model_type}) সাকসেসফুলি ৬টি প্ল্যাটফর্মের ডেটা রেডি করেছে!")
                    
                    row1_c1, row1_c2, row1_c3 = st.columns(3)
                    row2_c1, row2_c2, row2_c3 = st.columns(3)
                    
                    with row1_c1:
                        st.error("📺 YouTube Video")
                        st.write("**AI Target Title (<100 Chars):**")
                        st.code(yt_title, language="")
                        st.write("**Optimized Description:**")
                        st.code(yt_desc, language="")
                        st.write("**🎯 সার্চ Tags (Tag Box):**")
                        st.code(yt_tags, language="")
                        
                    with row1_c2:
                        st.error("📊 YT Community Post & Poll")
                        st.write("**কমিউনিটি ট্যাব কন্টেন্ট:**")
                        st.code(comm_post, language="")
                        
                    with row1_c3:
                        st.warning("🔵 FB Business Suite")
                        st.write("**ফেসবুক কন্টেন্ট মেটা:**")
                        st.code(fb_meta, language="")
                        
                    with row2_c1:
                        st.info("🎵 TikTok & Reels")
                        st.write("**শর্টস/টিকটক ক্যাপশন:**")
                        st.code(tt_meta, language="")
                        
                    with row2_c2:
                        st.success("📰 TBS Bangla CMS")
                        st.write("**বাংলা ওয়েবসাইট হেডলাইন:**")
                        st.code(headline.strip(), language="")
                        st.write("**ভিডিও বডি বিবরণ:**")
                        st.code(given_desc if given_desc else headline.strip(), language="")
                        
                    with row2_c3:
                        st.success("🇬🇧 TBS English CMS")
                        st.write("**অটো-অনূদিত ইংলিশ হেডলাইন:**")
                        st.code(eng_cms, language="")

                    # টাস্ক ট্র্যাকার
                    st.markdown("---")
                    st.subheader("🚨 লাইভ ডিস্ট্রিবিউশন ট্র্যাকার")
                    ch1, ch2, ch3, ch4, ch5, ch6 = st.columns(6)
                    ch1.checkbox("YouTube Video Done")
                    ch2.checkbox("YT Community Done")
                    ch3.checkbox("Facebook Post Done")
                    ch4.checkbox("TikTok Pushed")
                    ch5.checkbox("Bangla CMS Done")
                    ch6.checkbox("English CMS Done")

                except urllib.error.HTTPError as he:
                    try:
                        err_body = json.loads(he.read().decode('utf-8'))
                        err_detail = err_body.get('error', {}).get('message', 'Unknown Google API Issue')
                        st.error(f"❌ গুগল এআই সার্ভার এরর (400): {err_detail}")
                    except:
                        st.error(f"❌ HTTP Error 400: {he.reason}. মডেল বা এপিআই কি সঠিক নয়।")
                except Exception as e:
                    st.error(f"সাধারণ সমস্যা: {e}")

# ----------------- 🔍নোট: ফিক্সডস ট্যাব ২ (Deep Competitor Scraper) -----------------
with tab2:
    st.header("প্রতিদ্বন্দী ভিডিওর ভেতরের আসল Tags এবং Hashtags স্ক্র্যাপার")
    keyword = st.text_input("সার্চ কিওয়ার্ডটি লিখুন:", placeholder="যেমন: বাজেট ২০২৬ বাংলাদেশ", key="tab2_kw")
    max_results = st.slider("কয়টি প্রতিদ্বন্দী ভিডিও অ্যানালাইসিস করবেন?", 5, 20, 10)

    if st.button("SEO এনালাইসিস শুরু করুন 🚀", key="tab2_btn"):
        if not clean_api_key:
            st.error("দয়া করে বাম পাশের সাইডবারে আপনার ইউটিউব Data API Key টি দিন।")
        elif not keyword:
            st.warning("আগে একটি কিওয়ার্ড লিখুন!")
        else:
            with st.spinner("ইউটিউব থেকে আসল Tags স্ক্র্যাপ করা হচ্ছে..."):
                try:
                    youtube = build('youtube', 'v3', developerKey=clean_api_key)
                    search_response = youtube.search().list(
                        q=keyword, part='snippet', maxResults=max_results, type='video', relevanceLanguage='bn'
                    ).execute()
                    
                    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
                    if not video_ids:
                        st.warning("কোনো ভিডিও পাওয়া যায়নি।")
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
                    st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
