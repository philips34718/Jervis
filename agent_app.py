import streamlit as st
from googleapiclient.discovery import build
import re
import urllib.request
import urllib.parse
import json

# এজেন্ট ড্যাশবোর্ড সেটআপ
st.set_page_config(page_title="TBS Sovereign SEO Agent 2.0", page_icon="🤖", layout="wide")
st.title("🤖 TBS Sovereign SEO Agent 2.0 (Auto-Pilot Edition)")
st.caption("লেটেস্ট ইউটিউব অ্যালগরিদম ও মেটা-ডেনসিটি অপ্টিমাইজড। ৬টি প্ল্যাটফর্মের জন্য এক ক্লিকে এলিট কন্টেন্ট ডিস্ট্রিবিউশন।")

# সাইডবারে API Key
api_key = st.sidebar.text_input("ইউটিউব API Key দিন:", type="password")

# ইনপুট হাব
st.markdown("### 📥 সেন্ট্রাল ডেটা ইনপুট")
headline = st.text_input("কোম্পানি থেকে দেওয়া মূল Headline বা context টি দিন:", placeholder="যেমন: বাজেট নিয়ে ড. দেবপ্রিয় ভট্টাচার্যের তাৎক্ষণিক বিশ্লেষণ")
given_desc = st.text_area("কোম্পানি থেকে দেওয়া বিবরণ (Description/Article Body):", placeholder="এখানে মূল বিবরণ বা খবরের ভেতরের অংশ পেস্ট করুন...")

if st.button("🤖 জেনারেট অল-চ্যানেল এলিট মেটাডেটা 🚀"):
    if not headline:
        st.warning("দয়া করে প্রথমে একটি হেডলাইন ইনপুট দিন।")
    else:
        with st.spinner("AI এজেন্ট অ্যালগরিদম ম্যাট্রিক্স প্রসেস করছে..."):
            headline_clean = headline.strip()
            
            # --- ১. প্রফেশনাল নিউজের গভীরতা অনুযায়ী এলিট সাফিক্স ইঞ্জিন ---
            suffix_pool = ["Bangla News", "Latest Update"]
            category = "general"
            
            # নিখুঁত কিওয়ার্ড ম্যাচিং এবং সাফিক্স নির্ধারণ
            if any(x in headline_clean for x in ["প্রতিরক্ষা", "সেনাবাহিনী", "সামরিক", "অস্ত্র", "military", "army", "যুদ্ধ"]):
                suffix_pool = ["Military Power", "Defense News", "Geopolitics"]
                category = "defense"
            elif any(x in headline_clean for x in ["বাজেট", "অর্থনীতি", "টাকা", "অর্থ", "budget", "economy", "ব্যাংক", "রাজস্ব"]):
                suffix_pool = ["Budget 2026", "Economy Update", "Finance Analysis"]
                category = "economy"
            elif any(x in headline_clean for x in ["জুলাই", "আন্দোলন", "বিপ্লব", "শহীদ", "যোদ্ধা", "uprising", "মুক্তিযোদ্ধা", "ছাত্র"]):
                suffix_pool = ["July Uprising", "Mass Movement", "Bangladesh Crisis"]
                category = "politics"
            elif any(x in headline_clean for x in ["আদালত", "মামলা", "গ্রেপ্তার", "পুলিশ", "র্যাব", "কোর্ট", "court", "verdict"]):
                suffix_pool = ["High Court", "Law and Order", "Crime News"]
                category = "law"
            elif any(x in headline_clean for x in ["খেলা", "বিশ্বকাপ", "ক্রিকেট", "ফুটবল", "ম্যাচ", "sports", "t20"]):
                suffix_pool = ["Sports Update", "Cricket Live", "Match Analysis"]
                category = "sports"

            suffix_combined = " | ".join(suffix_pool)
            branding_long = " | The Business Standard"
            branding_short = " | TBS News"
            
            # ১০০ ক্যারেক্টার সিকিউরিটি লজিক
            final_title = f"{headline_clean} | {suffix_combined}{branding_long}"
            if len(final_title) > 100:
                final_title = f"{headline_clean} | {suffix_combined}{branding_short}"
            if len(final_title) > 100:
                final_title = f"{headline_clean} | {suffix_combined}"
            if len(final_title) > 100:
                final_title = f"{headline_clean} | {suffix_pool[0]}{branding_short}"
            if len(final_title) > 100:
                final_title = headline_clean[:100]

            # --- ২. ফ্রি গুগল সাজেস্ট এপিআই থেকে লাইভ ট্যাগ এক্সট্রাকশন ---
            words = re.findall(r'[\u0980-\u09fa\w]+', headline_clean)
            stop_words = ["নিয়ে", "ও", "এবং", "এর", "জানুন", "কী", "কেন", "হলো", "নিয়ে", "করেছেন", "চলছে", "হবে"]
            core_keywords = [w for w in words if w not in stop_words and len(w) > 1]
            
            search_seed = core_keywords[0] if core_keywords else headline_clean
            yt_suggestions = []
            try:
                url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&hl=bn&q={urllib.parse.quote(search_seed)}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode('utf-8', errors='ignore'))
                    yt_suggestions = [item[0] for item in res_data[1]]
            except Exception:
                pass

            # --- ৩. এলিট লোয়ারকেস হ্যাশট্যাগ ও ট্যাগস ইঞ্জিন ---
            base_tags = ["tbs", "tbsnews", "thebusinessstandard", "banglanews", "trending"]
            category_tags = [kw.lower().replace(" ", "") for kw in suffix_pool]
            all_tags_raw = category_tags + base_tags
            clean_lowercase_tags = list(dict.fromkeys([t.strip().lower() for t in all_tags_raw]))
            formatted_hashtags = " ".join([f"#{t}" for t in clean_lowercase_tags[:6]])

            # মেটা ট্যাগ কম্বিনেশন
            tbs_meta = ["tbs news", "the business standard", "bangla news live"]
            combined_meta_box = list(dict.fromkeys(core_keywords + yt_suggestions[:5] + tbs_meta))
            meta_tags_string = ", ".join(combined_meta_box)

            # --- ৪. আলটিমেট ইউটিউব কমিউনিটি পোস্ট জেনারেটর ---
            community_text = f"📢 আজকের বিশেষ প্রতিবেদন:\n\n{headline_clean}\n\n"
            if given_desc:
                community_text += f"📌 খবরের বিবরণ:\n{given_desc.strip()[:150]}...\n\n"
            community_text += f"👇 সম্পূর্ণ ভিডিওটি দেখতে নিচের লিংকে ক্লিক করুন:\n🔗 [ভিডিওর লিংক এখানে পেস্ট করুন]\n\n{formatted_hashtags}"

            # --- ৫. গ্রিড লেআউট আউটপুট প্যানেল ---
            st.markdown("---")
            st.success("🎯 AI এজেন্ট সফলভাবে সব প্ল্যাটফর্মের জন্য মেটাডেটা অপ্টিমাইজ করেছে!")
            
            row1_col1, row1_col2, row1_col3 = st.columns(3)
            row2_col1, row2_col2, row2_col3 = st.columns(3)

            # কলাম ১: ইউটিউব ভিডিও
            with row1_col1:
                st.error("📺 YouTube Video SEO")
                st.write("**Title (১০০ অক্ষরের নিচে সুরক্ষিত):**")
                st.code(final_title, language="")
                st.write("**Description (কোম্পানির বিবরণ + এলিট হ্যাশট্যাগ):**")
                desc_content = given_desc.strip() if given_desc else headline_clean
                st.code(f"{desc_content}\n\n{formatted_hashtags}", language="")
                st.write("**🎯 সার্চ ট্যাগস (Tag Box):**")
                st.code(meta_tags_string, language="")

            # কলাম ২: ইউটিউব কমিউনিটি পোস্ট
            with row1_col2:
                st.error("📊 YouTube Community Post")
                st.write("**কমিউনিটি ট্যাব টেক্সট (অডিয়েন্স এনগেজমেন্ট বুস্টার):**")
                st.code(community_text, language="")
                st.info("💡 টিপস: এই পোস্টটি করার সময় চ্যানেলে একটি পোল (Poll) ক্রিয়েট করে দিলে ইমপ্রেশন ৩ গুণ বেড়ে যায়।")

            # কলাম ৩: ফেসবুক ভিডিও
            with row1_col3:
                st.warning("🔵 FB Business Suite")
                st.write("**FB Title:**")
                st.code(headline_clean, language="")
                st.write("**FB Description:**")
                st.code(f"{desc_content}\n\n{formatted_hashtags} #facebookvideo", language="")

            # কলাম ৪: টিকটক ও রিলস
            with row2_col1:
                st.info("🎵 TikTok & Reels")
                st.write("**Reels/Shorts Title:**")
                st.code(final_title, language="")
                st.write("**Smart Lowercase Hashtags:**")
                st.code(f"{formatted_hashtags} #shorts #reelsviral", language="")

            # কলাম ৫: টিবিএস বাংলা সিএমএস
            with row2_col2:
                st.success("📰 TBS Bangla CMS")
                st.write("**Headline:**")
                st.code(headline_clean, language="")
                st.write("**Video Description Box:**")
                st.code(desc_content, language="")

            # কলাম ৬: টিবিএস ইংলিশ সিএমএস
            with row2_col3:
                st.success("🇬🇧 TBS English CMS")
                st.write("**Headline:**")
                st.code(headline_clean, language="")
                st.write("**Embed Body:**")
                st.code(desc_content, language="")

# ----------------- 🔍 ট্যাব ২: প্রতিদ্বন্দী স্ক্র্যাপার (সুরক্ষিত) -----------------
with tab2:
    st.header("প্রতিদ্বন্দী ভিডিওর ভেতরের আসল Tags এবং Hashtags স্ক্র্যাপার")
    keyword = st.text_input("সার্চ কিওয়ার্ডটি লিখুন:", placeholder="যেমন: বাজেট ২০২৬ বাংলাদেশ", key="tab2_kw")
    max_results = st.slider("কয়টি প্রতিদ্বন্দী ভিডিও অ্যানালাইসিস করবেন?", 5, 20, 10)

    if st.button("SEO এনালাইসিস শুরু করুন 🚀", key="tab2_btn"):
        if not api_key:
            st.error("দয়া করে বাম পাশের সাইডবারে আপনার ইউটিউব API Key টি দিন।")
        elif not keyword:
            st.warning("আগে একটি কিওয়ার্ড লিখুন!")
        else:
            with st.spinner("ইউটিউব থেকে আসল Tags স্ক্র্যাপ করা হচ্ছে..."):
                try:
                    youtube = build('youtube', 'v3', developerKey=api_key)
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
