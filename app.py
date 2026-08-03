import streamlit as st
from pipeline import run_research_pipeline

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Research Report Generator",
    page_icon="🔍",
    layout="wide",
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.main-title{
    font-size:42px;
    font-weight:700;
}

.subtitle{
    color:#888;
    margin-bottom:30px;
}

.metric-box{
    background:#262730;
    padding:18px;
    border-radius:12px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">🔍 AI Research Report Generator</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Generate professional research reports using live web information powered by LangChain Agents.</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("⚙️ Research Pipeline")

    st.markdown("""
This application follows four AI agents:

- 🔍 **Search Agent**
- 🌐 **Reader Agent**
- ✍️ **Writer**
- 🧐 **Critic**

The report is generated from live web information.
    """)

    st.divider()

    st.info(
        "Built with\n\n"
        "- LangChain\n"
        "- Streamlit\n"
        "- OpenAI\n"
        "- BeautifulSoup"
    )

# -----------------------------
# Input
# -----------------------------
topic = st.text_input(
    "Research Topic",
    placeholder="Example: Artificial General Intelligence",
)

generate = st.button(
    "🚀 Generate Report",
    use_container_width=True,
)

# -----------------------------
# Run
# -----------------------------
if generate:

    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    def update(step):

        mapping = {
            "search": (25, "🔍 Searching the web..."),
            "reader": (50, "🌐 Reading the best source..."),
            "writer": (75, "✍️ Writing report..."),
            "critic": (100, "🧐 Reviewing report...")
        }

        if step in mapping:
            value, text = mapping[step]
            progress.progress(value)
            status.info(text)

    # Since your current pipeline doesn't support callbacks yet,
    # we'll manually animate the progress.

    with st.spinner("Generating report..."):

        update("search")
        update("reader")
        update("writer")
        update("critic")

        state = run_research_pipeline(topic)

    progress.progress(100)
    status.success("✅ Report Generated Successfully!")

    st.divider()

    # -----------------------------
    # Metrics
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Topic",
            topic,
        )

    with col2:
        st.metric(
            "Report Words",
            len(state["report"].split()),
        )

    with col3:
        st.metric(
            "Status",
            "Completed",
        )

    st.divider()

    # -----------------------------
    # Tabs
    # -----------------------------
    report_tab, research_tab, critic_tab = st.tabs(
        [
            "📑 Final Report",
            "🔍 Research Details",
            "📝 Critic Feedback",
        ]
    )

    # -----------------------------
    # Report
    # -----------------------------
    with report_tab:

        st.markdown(state["report"])

        st.download_button(
            label="⬇️ Download Markdown",
            data=state["report"],
            file_name=f"{topic.replace(' ','_')}.md",
            mime="text/markdown",
        )

    # -----------------------------
    # Research
    # -----------------------------
    with research_tab:

        with st.expander("🔍 Search Results", expanded=True):
            st.write(state["search_results"])

        with st.expander("📄 Scraped Content", expanded=False):
            st.write(state["scraped_content"])

    # -----------------------------
    # Critic
    # -----------------------------
    with critic_tab:

        st.markdown(state["feedback"])