import streamlit as st
import json
import pandas as pd
from io import BytesIO
import zipfile
from prompt_generator import build_prompt_from_video

st.set_page_config(
    page_title="Viral Video Prompt Generator",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Viral Video Prompt Generator")
st.markdown("Upload your JSON file with viral video data to generate AI prompts")

# Sidebar
with st.sidebar:
    st.header("ℹ️ How to Use")
    st.markdown("""
    1. Upload your JSON file with video data
    2. Click 'Generate Prompts'
    3. Download results as JSON, CSV, or TXT files
    
    **JSON Format:**
    ```json
    [
      {
        "Video ID": "abc123",
        "Video Title": "Title",
        "Views": 100000,
        "Duration (sec)": 15,
        "Niche": "Wealth & Money",
        "Keyword": "success tips"
      }
    ]
    ```
    """)

# File uploader
uploaded_file = st.file_uploader("📁 Upload JSON file", type=['json'])

if uploaded_file is not None:
    try:
        # Load JSON
        videos = json.load(uploaded_file)
        st.success(f"✅ Loaded {len(videos)} videos")
        
        # Show preview
        with st.expander("📊 Preview Data"):
            df_preview = pd.DataFrame(videos)
            columns_to_show = ['Video Title', 'Views', 'Duration (sec)', 'Niche', 'Keyword']
            available_columns = [col for col in columns_to_show if col in df_preview.columns]
            st.dataframe(df_preview[available_columns].head(10))
        
        # Generate prompts button
        if st.button("🚀 Generate Prompts for All Videos", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            all_prompts = []
            
            for idx, v in enumerate(videos):
                status_text.text(f"Processing video {idx+1}/{len(videos)}...")
                progress_bar.progress((idx + 1) / len(videos))
                
                prompt = build_prompt_from_video(v)
                all_prompts.append({
                    "Video ID": v.get("Video ID", ""),
                    "Video Title": v.get("Video Title", ""),
                    "Views": v.get("Views", 0),
                    "Duration (sec)": v.get("Duration (sec)", 0),
                    "Niche": v.get("Niche", ""),
                    "Keyword": v.get("Keyword", ""),
                    "Generated Prompt": prompt
                })
            
            status_text.text("✅ All prompts generated!")
            progress_bar.empty()
            
            # Store in session state
            st.session_state.all_prompts = all_prompts
            
            # Display results
            st.success(f"🎉 Generated {len(all_prompts)} prompts!")
            
            # Create download options
            st.subheader("📥 Download Options")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # JSON download
                json_str = json.dumps(all_prompts, indent=2, ensure_ascii=False)
                st.download_button(
                    label="📄 Download JSON",
                    data=json_str,
                    file_name="generated_prompts.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                # CSV download
                df = pd.DataFrame(all_prompts)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📊 Download CSV",
                    data=csv,
                    file_name="generated_prompts.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                # ZIP of individual text files
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for idx, item in enumerate(all_prompts, 1):
                        content = f"""VIDEO: {item['Video Title']}
VIDEO ID: {item['Video ID']}
VIEWS: {item['Views']:,}
DURATION: {item['Duration (sec)']} seconds
NICHE: {item['Niche']}
KEYWORD: {item['Keyword']}
{'=' * 80}

{item['Generated Prompt']}
"""
                        zip_file.writestr(f"prompt_{idx}_{item['Video ID']}.txt", content)
                
                st.download_button(
                    label="📦 Download All TXT (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="prompts.zip",
                    mime="application/zip",
                    use_container_width=True
                )
            
            # Show sample prompts
            st.markdown("---")
            st.subheader("📝 Sample Prompts Preview")
            
            num_samples = min(3, len(all_prompts))
            for i in range(num_samples):
                with st.expander(f"🎬 Prompt {i+1}: {all_prompts[i]['Video Title'][:60]}..."):
                    st.markdown(f"**Video ID:** {all_prompts[i]['Video ID']}")
                    st.markdown(f"**Views:** {all_prompts[i]['Views']:,}")
                    st.markdown(f"**Duration:** {all_prompts[i]['Duration (sec)']} seconds")
                    st.markdown("---")
                    st.text_area(
                        "Generated Prompt", 
                        all_prompts[i]['Generated Prompt'],
                        height=300,
                        key=f"prompt_{i}"
                    )
    
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON file. Please upload a valid JSON file.")
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")

else:
    st.info("👆 Upload a JSON file to get started")
    
    # Show example format
    with st.expander("📋 Example JSON Format"):
        example = [
            {
                "Video ID": "abc123",
                "Video Title": "#success #shorts",
                "Video URL": "https://youtube.com/shorts/abc123",
                "Views": 1027602,
                "Likes": 1170,
                "Duration (sec)": 4,
                "Niche": "Wealth & Money Stories",
                "Keyword": "success tips",
                "Description": "Motivational content...",
                "Idea Angle": "Recreate this viral format..."
            },
            {
                "Video ID": "xyz789",
                "Video Title": "Poor vs Rich Mindset",
                "Video URL": "https://youtube.com/shorts/xyz789",
                "Views": 500000,
                "Likes": 5000,
                "Duration (sec)": 15,
                "Niche": "Wealth & Money Stories",
                "Keyword": "rich vs poor mindset",
                "Description": "Money psychology...",
                "Idea Angle": "Recreate this trending format..."
            }
        ]
        st.json(example)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for Content Creators | Upload your viral video data and get AI-ready prompts instantly")
