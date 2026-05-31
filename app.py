import streamlit as st
import json
from google import genai
from google.genai import types

# 1. การตั้งค่าหน้าเพจ (คำสั่งนี้ต้องอยู่บรรทัดบนสุดเสมอ)
st.set_page_config(page_title="AI ติวเตอร์ภาษาอังกฤษ", page_icon="🎓", layout="wide")
# ==========================================
# 🌟 ส่วนที่เพิ่มเข้ามา: แทรกโค้ด CSS เพื่อปรับแต่งกล่องข้อความ
# ==========================================
st.markdown("""
<style>
/* ค้นหากล่องข้อความของ Streamlit และบังคับกฎใหม่ */
div[data-baseweb="textarea"] textarea {
    resize: none !important;          /* 1. ปิดไม่ให้ผู้ใช้ลากปรับขนาดเองได้ */
    field-sizing: content !important; /* 2. เวทมนตร์ที่ทำให้กล่องขยายความสูงเองอัตโนมัติตามบรรทัดที่พิมพ์ */
    min-height: 120px !important;     /* 3. กำหนดความสูงเริ่มต้นให้ดูสวยงาม */
    line-height: 1.5 !important;      /* 4. ปรับระยะห่างระหว่างบรรทัดให้อ่านง่าย */
}
/* 2. ซ่อนลายน้ำ "Press Ctrl+Enter to apply" */
div[data-testid="InputInstructions"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)
# ==========================================
# แอบดึงกุญแจลับ
SECRET_API_KEY = st.secrets["GEMINI_API_KEY"]

# 2. สร้างแถบด้านข้าง (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1903/1903162.png", width=100) # ใส่ภาพไอคอน
    st.header("เกี่ยวกับระบบ")
    st.write("ระบบนี้พัฒนาขึ้นเพื่อประเมินความสามารถทางภาษาอังกฤษ อ้างอิงตามมาตรฐาน CEFR")

# 3. ส่วนหัวของเว็บ
st.title("🎓 AI ติวเตอร์ตรวจภาษาอังกฤษ (CEFR Evaluator)")

# 4. กล่องคำอธิบายแบบพับเก็บได้
# with st.expander("📖 อ่านคำแนะนำวิธีใช้งานที่นี่"):
#     st.markdown("""
#     1. พิมพ์ประโยคภาษาอังกฤษของคุณลงในกล่องข้อความ
#     2. กดปุ่ม **'ส่งให้ AI ตรวจ'**
#     3. รอสักครู่เพื่อรับผลคะแนนและคำแนะนำ
#     """)

# 5. แบ่งหน้าจอเป็น 2 ฝั่งเพื่อจัดระเบียบ
col_input, col_result = st.columns([1, 1]) # แบ่งซ้ายขวา สัดส่วน 1:1

with col_input:
    st.subheader("พิมพ์ประโยคภาษาอังกฤษของคุณที่นี่")
    student_text = st.chat_input("พิมพ์ประโยคของคุณที่นี่...")

with col_result:
    st.subheader("ผลการประเมิน")
    if student_text:
        with st.spinner('AI กำลังวิเคราะห์โครงสร้างประโยค...'):
            try:
                client = genai.Client(api_key=SECRET_API_KEY)
                system_prompt = """
                วิเคราะห์ประโยคภาษาอังกฤษของนักเรียนมัธยม ส่งคืนผลลัพธ์เป็น JSON
                รูปแบบ:
                {
                  "cefr_level": "A1/A2/B1/B2",
                  "grammar_score": 10,
                  "feedback": "คำแนะนำภาษาไทยสั้นๆ"
                }
                """
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=student_text,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        response_mime_type="application/json",
                        temperature=0.2
                    )
                )
                
                result = json.loads(response.text)
                
                st.success("✨ ประเมินเสร็จสิ้น!")
                
                # โชว์คะแนนแบบการ์ด
                score_col1, score_col2 = st.columns(2)
                score_col1.metric(label="ระดับมาตรฐาน CEFR", value=result['cefr_level'])
                score_col2.metric(label="คะแนนไวยากรณ์", value=f"{result['grammar_score']} / 10")
                
                st.info(f"💡 **คำแนะนำจาก AI:**\n{result['feedback']}")
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.write("กรุณากดส่งคำตอบเพื่อดูผลการประเมินตรงนี้")