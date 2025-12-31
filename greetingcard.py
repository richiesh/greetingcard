import streamlit as st
import time
from PIL import Image, ImageDraw, ImageFont
import io
import os

# Set page configuration
st.set_page_config(
    page_title="2026 马年贺卡",
    page_icon="🐴",
    layout="centered"
)

# Custom CSS to inject for "Rich Aesthetics"
st.markdown("""
<style>
    /* Animated Gradient Background */
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background: linear-gradient(-45deg, #c0392b, #f1c40f, #e74c3c, #8e44ad);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Glassmorphism Card Container */
    .greeting-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        text-align: center;
        margin-top: 20px;
        border: 2px solid #ffd700;
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0% {transform: translatey(0px);}
        50% {transform: translatey(-10px);}
        100% {transform: translatey(0px);}
    }
    
    /* Text Styles */
    h1 {
        background: linear-gradient(to right, #e60000, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 3.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #333;
        font-size: 1.8rem !important;
        margin-bottom: 20px;
        font-weight: 700;
    }
    
    p {
        color: #444;
        font-size: 1.2rem;
        line-height: 1.8;
        font-weight: 500;
    }
    
    .gold-text {
        background: linear-gradient(45deg, #b8860b, #ffd700, #b8860b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.2rem;
        margin: 10px 0;
        text-shadow: 0px 2px 2px rgba(0,0,0,0.1);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #ff512f, #dd2476);
        color: white;
        border-radius: 50px;
        border: none;
        padding: 15px 40px;
        font-weight: bold;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 25px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)


def create_share_image(title_lines, recipient, body_lines, footer_lines):
    """Generates a static image card for sharing using PIL."""
    # Image config
    width = 800
    height = 1000
    bg_color = (255, 250, 240) # FloralWhite
    
    # Create image
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw border
    border_color = (255, 215, 0) # Gold
    draw.rectangle([20, 20, width-20, height-20], outline=border_color, width=10)
    
    # Fonts
    try:
        # Prioritize customized/downloaded calligraphy font
        if os.path.exists("wangxizhi.ttf"):
            font_path = "wangxizhi.ttf"
            # Calligraphy fonts are often stylized and might need slight size adjustment, 
            # but we stick to defaults first.
            title_font = ImageFont.truetype(font_path, 70) # slightly larger for title
            body_font = ImageFont.truetype(font_path, 45)
            footer_font = ImageFont.truetype(font_path, 35)
        else:
            # Fallback to Mac system fonts
            font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
            if not os.path.exists(font_path):
                 font_path = "/System/Library/Fonts/PingFang.ttc"
            
            title_font = ImageFont.truetype(font_path, 60)
            body_font = ImageFont.truetype(font_path, 40)
            footer_font = ImageFont.truetype(font_path, 30)
    except Exception as e:
        print(f"Font loading error: {e}")
        # Fallback default
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()

    # Draw Title
    y_pos = 100
    for line in title_lines:
        # Centering logic relies on getbbox or textlength, doing simple approximation or using anchors
        # anchor="mm" aligns middle-middle
        draw.text((width/2, y_pos), line, font=title_font, fill=(220, 20, 60), anchor="mm")
        y_pos += 80
    
    y_pos += 40
    
    # Draw Recipient
    draw.text((width/2, y_pos), recipient, font=body_font, fill=(0, 0, 0), anchor="mm")
    y_pos += 60
    
    # Draw Body
    for line in body_lines:
        draw.text((width/2, y_pos), line, font=body_font, fill=(50, 50, 50), anchor="mm")
        y_pos += 60

    y_pos += 40
    # Draw Footer
    for line in footer_lines:
        draw.text((width/2, y_pos), line, font=footer_font, fill=(100, 100, 100), anchor="mm")
        y_pos += 50
        
    # Draw Logo at the bottom if exists
    if os.path.exists("logo.png"):
        try:
            logo = Image.open("logo.png")
            # Resize
            logo_width = 150
            aspect_ratio = logo.height / logo.width
            logo_height = int(logo_width * aspect_ratio)
            logo = logo.resize((logo_width, logo_height))
            
            # Position at bottom center
            x_pos = (width - logo_width) // 2
            # Ensure it fits at the bottom, adjust if needed based on footer lines
            logo_y_pos = height - logo_height - 50 
            
            # Paste with mask for transparency
            if logo.mode == 'RGBA':
                img.paste(logo, (x_pos, logo_y_pos), logo)
            else:
                img.paste(logo, (x_pos, logo_y_pos))
        except Exception as e:
            print(f"Could not load logo for image: {e}")
            
    # Return bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def main():
    # --- Sidebar Configuration ---
    st.sidebar.markdown("---")
    st.sidebar.header("✍️ 定制祝福内容")
    
    recipient_name = st.sidebar.text_input("📝 对方称呼 (如: 奶奶, 张总)", value="亲爱的朋友")
    
    relation_type = st.sidebar.selectbox(
        "👥 关系类型",
        options=["朋友/同事", "长辈/亲戚", "领导/老师", "伴侣/爱人", "晚辈/孩子", "客户/合作伙伴"]
    )
    
    event_focus = st.sidebar.multiselect(
        "🎯 祝福主题 (可多选)",
        options=["新年通用", "事业高升", "发财/生意", "健康平安", "学业进步", "爱情甜蜜"],
        default=["新年通用"]
    )
    
    # Music
    st.sidebar.markdown("### 🎵 背景音乐设置")
    music_options = {
        "🧨 欢快喜庆 (默认)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "🥁 动感节奏": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "🏮 舒缓祥和": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
        "🎹 钢琴优美": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3",
        "🔗 自定义链接": "custom"
    }
    selected_music_name = st.sidebar.selectbox("选择背景音乐", list(music_options.keys()))
    if selected_music_name == "🔗 自定义链接":
        music_url = st.sidebar.text_input("请输入音频链接 (.mp3)", "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    else:
        music_url = music_options[selected_music_name]
    
    if st.sidebar.checkbox("🔊 开启音乐", value=True):
         st.audio(music_url, format='audio/mp3', loop=True)

    # --- Logic Generators ---
    salutations = {
        "朋友/同事": "亲爱的",
        "长辈/亲戚": "尊敬的",
        "领导/老师": "尊敬的",
        "伴侣/爱人": "亲爱的",
        "晚辈/孩子": "可爱的",
        "客户/合作伙伴": "尊贵的"
    }
    
    tone_phrases = {
        "朋友/同事": ["新的一年，咱们继续并肩作战！", "愿你依然自由如风，潇洒如马！"],
        "长辈/亲戚": ["祝您福如东海，寿比南山。", "愿您在新的一年里精神矍铄，神采飞扬。"],
        "领导/老师": ["感谢您一直以来的提携与指导。", "祝您的事业版图如骏马奔腾，再创新高。"],
        "伴侣/爱人": ["感谢这一路有你相伴。", "这是我们一起度过的又一个新年。"],
        "晚辈/孩子": ["看着你一天天长大真开心。", "愿你像小马驹一样快乐奔跑。"],
        "客户/合作伙伴": ["感谢该年度的信任与支持。", "愿我们来年合作更上一层楼。"]
    }
    
    wishes_db = {
        "新年通用": ["龙马精神，万事如意", "马到成功，好运连连", "万马奔腾，气势如虹"],
        "事业高升": ["一马当先，独占鳌头", "快马加鞭，更上一层楼", "鹏程万里，马到功成"],
        "发财/生意": ["马上发财，财源广进", "金马送福，富贵盈门", "招财进宝，日进斗金"],
        "健康平安": ["人欢马叫，阖家幸福", "身体健康，神采飞扬", "生活更有好马力"],
        "学业进步": ["天马行空，才思泉涌", "学业有成，金榜题名", "智慧如马，一日千里"],
        "爱情甜蜜": ["马上有对象，甜蜜久久", "青梅竹马，情比金坚", "心猿意马只为你"]
    }

    # Construct content
    # Handle empty selection
    if not event_focus:
        event_focus = ["新年通用"]

    selected_wishes = []
    for focus in event_focus:
        phrases = wishes_db.get(focus, wishes_db["新年通用"])
        selected_wishes.extend(phrases[:2])
    
    unique_wishes = list(set(selected_wishes))
    if len(unique_wishes) > 3:
        unique_wishes = unique_wishes[:3]

    full_name_display = f"{salutations.get(relation_type, '')} {recipient_name}："
    intro_sentence = tone_phrases.get(relation_type, [""])[0]
    
    main_wish_str = selected_wishes[0]

    # --- Display ---
    
    # Logo Display at Top Center
    if os.path.exists("logo.png"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("logo.png", use_container_width=True)

    st.markdown('<div class="greeting-card">', unsafe_allow_html=True)
    st.title("🎉 2026 丙午马年快乐! 🐴")
    
    if "balloons_shown" not in st.session_state:
        st.balloons()
        st.session_state.balloons_shown = True
    
    st.markdown(f"""
    ## 🌟 {main_wish_str} 🌟
    
    **{full_name_display}**
    
    值此 **2026** 新春佳节之际，
    {intro_sentence}
    
    祝您在**马年**里：
    """, unsafe_allow_html=True)

    for wish in unique_wishes:
         st.markdown(f'<div class="gold-text">{wish}</div>', unsafe_allow_html=True)
    
    st.markdown("""
    愿您的事业如骏马奔腾，生活如春风得意！
    身体健康，阖家幸福！
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("✨ 点击下方按钮领取好运 ✨")
    
    if st.button("🧧 领取红包"):
        st.success(f"💰 给 {recipient_name} 的专属红包已发送！恭喜发财，大吉大利！")
        st.snow()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- Sidebar: Share & Export ---
    st.sidebar.markdown("---")
    st.sidebar.header("📤 转发/分享")
    
    share_text = f"""🎉 2026 丙午马年快乐！🐴

{full_name_display}
{intro_sentence}

愿您在马年里：
{' '.join([f'✨ {w}' for w in unique_wishes])}

愿您的事业如骏马奔腾，生活如春风得意！
身体健康，阖家幸福！

(来自您的好友定制祝福)"""

    st.sidebar.text_area("复制下方文字发送给微信好友：", value=share_text, height=200)
    
    st.sidebar.info("💡 **提示**: 您可以使用下方的按钮生成图片，保存后直接发送给微信好友！")

    # Generate Image Logic
    if st.sidebar.button("🖼️ 生成分享图片"):
        with st.spinner("正在绘制贺卡..."):
            # Prepare separate lines for image
            img_title = ["🎉 2026 马年快乐 🐴"]
            img_body = [
                intro_sentence,
                " ", # spacer
                "愿您在马年里：",
                *([f"✨ {w}" for w in unique_wishes]),
                " ",
                "愿您的事业如骏马奔腾",
                "生活如春风得意！"
            ]
            img_footer = [" ", " "] # Leave content empty so logo has space, spacer for aesthetic
            
            image_buffer = create_share_image(img_title, full_name_display, img_body, img_footer)
            
            # Store in session state to persist download button
            st.session_state['generated_image'] = image_buffer
            st.session_state['generated_image_name'] = f"马年祝福_{recipient_name}.png"
            
            st.sidebar.success("图片已生成！")
            
    # Show download button independent of generation button
    if 'generated_image' in st.session_state:
        st.sidebar.download_button(
            label="📥 点击下载贺卡图片",
            data=st.session_state['generated_image'],
            file_name=st.session_state.get('generated_image_name', 'greeting_card.png'),
            mime="image/png"
        )

if __name__ == "__main__":
    main()