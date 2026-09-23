import os
import re
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="LeetCode Solutions Hub",
    page_icon="🧩",
    layout="wide"
)

# 2. Permanent Dark Theme CSS Injection
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%) !important;
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
    }
    div[data-testid="stMainBlockContainer"] {
        padding-bottom: 8rem !important;
    }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.85) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
    }
    section[data-testid="stSidebar"] *, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }

    /* 🔍 Complete Dark Mode Fix for Search Input Box */
    div[data-baseweb="input"],
    div[data-baseweb="input"] > div,
    [data-baseweb="base-input"],
    .stTextInput input {
        background-color: #090d16 !important;
        background: #090d16 !important;
    }

    div[data-baseweb="input"] {
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stTextInput input::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }

    /* Filter Buttons Styling */
    .stButton > button {
        background-color: #090d16 !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 20px !important;
        padding: 0.35rem 0.85rem !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        border-color: #818cf8 !important;
        color: #ffffff !important;
        background-color: #131b2e !important;
    }

    .gradient-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        color: #94a3b8 !important;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }

    .stat-card {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
        padding: 18px 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
    }
    .stat-num {
        font-size: 2rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .stat-label {
        color: #94a3b8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #e2e8f0 !important;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    .badge-lang { background-color: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    .badge-topic { background-color: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    .badge-easy { background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    .badge-medium { background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    .badge-hard { background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    </style>
""", unsafe_allow_html=True)

# Data Mapping
LANGUAGE_MAP = {
    "Python": [".py"],
    "C++": [".cpp", ".cc", ".cxx"],
    "Java": [".java"],
    "JavaScript": [".js"],
    "TypeScript": [".ts"],
    "Go": [".go"],
    "Rust": [".rs"],
    "C#": [".cs"],
    "C": [".c"],
    "Kotlin": [".kt"]
}

TOPIC_KEYWORDS = {
    "Arrays & Hashing": ["contains-duplicate", "valid-anagram", "two-sum", "group-anagrams", "top-k-frequent", "product-of-array", "long-consecutive"],
    "Two Pointers": ["valid-palindrome", "two-sum-ii", "3sum", "container-with-most-water", "trapping-rain-water"],
    "Sliding Window": ["best-time-to-buy", "longest-substring", "longest-repeating-character", "permutation-string"],
    "Stack": ["valid-parentheses", "min-stack", "evaluate-reverse-polish", "generate-parentheses", "daily-temperatures"],
    "Binary Search": ["binary-search", "search-a-2d-matrix", "koko-eating-bananas", "find-minimum-in-rotated"],
    "Linked List": ["reverse-linked-list", "merge-two-sorted", "reorder-list", "remove-nth-node", "linked-list-cycle"],
    "Trees": ["invert-binary-tree", "maximum-depth", "diameter-of-binary-tree", "balanced-binary-tree", "same-tree"],
    "Backtracking": ["subsets", "combination-sum", "permutations", "word-search", "n-queens"],
    "Graphs": ["number-of-islands", "clone-graph", "max-area-of-island", "pacific-atlantic"],
    "1-D Dynamic Programming": ["climbing-stairs", "min-cost-climbing", "house-robber", "coin-change"]
}

def detect_topic(filename):
    clean_fn = filename.lower()
    for category, keywords in TOPIC_KEYWORDS.items():
        if any(kw in clean_fn for kw in keywords):
            return category
    return "Other Solutions"

def detect_difficulty(filename, rel_path):
    path_lower = (rel_path + "/" + filename).lower()
    if "easy" in path_lower:
        return "Easy"
    elif "hard" in path_lower:
        return "Hard"
    elif "medium" in path_lower:
        return "Medium"
    
    easy_keywords = ["two-sum", "valid-anagram", "contains-duplicate", "valid-palindrome", "binary-search", "reverse-linked-list", "invert-binary-tree"]
    hard_keywords = ["n-queens", "trapping-rain-water", "word-search-ii", "median-of-two-sorted"]
    
    if any(kw in path_lower for kw in easy_keywords):
        return "Easy"
    elif any(kw in path_lower for kw in hard_keywords):
        return "Hard"
    return "Medium"

def generate_leetcode_url(filename):
    name_without_ext = os.path.splitext(filename)[0]
    slug = re.sub(r'^\d+[-_]?', '', name_without_ext).strip().lower().replace("_", "-")
    if slug:
        return f"https://leetcode.com/problems/{slug}/"
    return None

@st.cache_data
def load_all_solutions():
    solutions = []
    ignore_dirs = {'.git', '.github', 'venv', '__pycache__', 'node_modules'}
    
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            for lang, exts in LANGUAGE_MAP.items():
                if ext in exts:
                    rel_path = os.path.relpath(os.path.join(root, file), ".")
                    clean_name = os.path.splitext(file)[0].replace("-", " ").replace("_", " ").title()
                    topic = detect_topic(file)
                    difficulty = detect_difficulty(file, rel_path)
                    leetcode_url = generate_leetcode_url(file)
                    
                    solutions.append({
                        "filename": file,
                        "title": clean_name,
                        "path": rel_path,
                        "language": lang,
                        "topic": topic,
                        "difficulty": difficulty,
                        "url": leetcode_url
                    })
                    break
    return solutions

all_solutions = load_all_solutions()

# Initialize session state for filters
if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = "All"
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "All"
if "selected_diff" not in st.session_state:
    st.session_state.selected_diff = "All"

# Header Section
st.markdown('<div class="gradient-title">🧩 LeetCode Solutions Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Explore algorithmic solutions with interactive language, category, and difficulty filters.</div>', unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(f'''
        <div class="stat-card">
            <div class="stat-num">{len(all_solutions)}</div>
            <div class="stat-label">Total Solutions</div>
        </div>
    ''', unsafe_allow_html=True)
with col_b:
    st.markdown(f'''
        <div class="stat-card">
            <div class="stat-num" style="color: #a855f7;">{len(LANGUAGE_MAP)}</div>
            <div class="stat-label">Languages Supported</div>
        </div>
    ''', unsafe_allow_html=True)
with col_c:
    st.markdown(f'''
        <div class="stat-card">
            <div class="stat-num" style="color: #ec4899;">{len(TOPIC_KEYWORDS)}</div>
            <div class="stat-label">Categories</div>
        </div>
    ''', unsafe_allow_html=True)

st.write("")
st.markdown("---")

# Sidebar Search Box
st.sidebar.markdown("### 🔍 Search")
search_query = st.sidebar.text_input("Problem Title / Name", "", placeholder="e.g. 3Sum, Two Sum...")

# 1. Select Language
st.markdown('<div class="section-header">1. Select Language</div>', unsafe_allow_html=True)
available_languages = ["All"] + sorted(list(set(s["language"] for s in all_solutions)))
lang_cols = st.columns(min(len(available_languages), 8))
for i, lang in enumerate(available_languages):
    col_idx = i % len(lang_cols)
    with lang_cols[col_idx]:
        is_active = (st.session_state.selected_lang == lang)
        btn_label = f"✨ {lang}" if is_active else lang
        if st.button(btn_label, key=f"lang_{lang}", use_container_width=True):
            st.session_state.selected_lang = lang
            st.rerun()

lang_filtered = all_solutions if st.session_state.selected_lang == "All" else [s for s in all_solutions if s["language"] == st.session_state.selected_lang]

# 2. Select Category / Topic
st.markdown('<div class="section-header">2. Select Category / Topic</div>', unsafe_allow_html=True)
available_topics = ["All"] + sorted(list(set(s["topic"] for s in lang_filtered)))
topic_cols = st.columns(min(len(available_topics), 6))
for i, topic in enumerate(available_topics):
    col_idx = i % len(topic_cols)
    with topic_cols[col_idx]:
        is_active = (st.session_state.selected_topic == topic)
        btn_label = f"📌 {topic}" if is_active else topic
        if st.button(btn_label, key=f"topic_{topic}", use_container_width=True):
            st.session_state.selected_topic = topic
            st.rerun()

topic_filtered = lang_filtered if st.session_state.selected_topic == "All" else [s for s in lang_filtered if s["topic"] == st.session_state.selected_topic]

# 3. Select Difficulty
st.markdown('<div class="section-header">3. Select Difficulty</div>', unsafe_allow_html=True)
difficulty_options = ["All", "Easy", "Medium", "Hard"]
diff_cols = st.columns(4)
for i, diff in enumerate(difficulty_options):
    with diff_cols[i]:
        is_active = (st.session_state.selected_diff == diff)
        btn_label = f"🎯 {diff}" if is_active else diff
        if st.button(btn_label, key=f"diff_{diff}", use_container_width=True):
            st.session_state.selected_diff = diff
            st.rerun()

IGNORE_FILES = {"updatesitedata.js", "verifysitedata.js", "updatecompletiontable.js"}
filtered = [s for s in topic_filtered if s["filename"].lower() not in IGNORE_FILES]

if st.session_state.selected_diff != "All":
    filtered = [s for s in filtered if s["difficulty"] == st.session_state.selected_diff]
if search_query:
    filtered = [s for s in filtered if search_query.lower() in s["filename"].lower() or search_query.lower() in s["title"].lower()]

st.markdown("---")

# Display Cards
has_selection = (st.session_state.selected_lang != "All") or (st.session_state.selected_topic != "All") or (st.session_state.selected_diff != "All") or search_query

if has_selection:
    st.markdown(f"### Found **{len(filtered)}** solution(s)")

    if not filtered:
        st.warning("No solutions found matching your selection.")
    else:
        for idx, item in enumerate(filtered[:20]):
            with st.container(border=True):
                col_title, col_link = st.columns([3, 1])
                with col_title:
                    st.markdown(f"#### 📄 {item['title']}")
                with col_link:
                    if item["url"]:
                        st.link_button("🔗 Open LeetCode", item["url"])

                diff_class = "badge-easy" if item["difficulty"] == "Easy" else ("badge-hard" if item["difficulty"] == "Hard" else "badge-medium")
                st.markdown(f'''
                    <div style="margin: 10px 0 15px 0; display: flex; gap: 10px;">
                        <span class="badge-lang">⚡ {item["language"]}</span>
                        <span class="badge-topic">🏷️ {item["topic"]}</span>
                        <span class="{diff_class}">📊 {item["difficulty"]}</span>
                    </div>
                ''', unsafe_allow_html=True)
                
                with st.expander("👁️ View Code Solution"):
                    try:
                        with open(item["path"], "r", encoding="utf-8", errors="ignore") as f:
                            code_content = f.read()
                        st.code(code_content, language=item["language"].lower())
                    except Exception as e:
                        st.error(f"Error loading code file: {e}")
