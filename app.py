import streamlit as st
import json
from google import genai
from google.genai import types

# 1. ออกแบบหน้าตาเว็บแอปเบื้องต้น
st.title("🤖 AI ตรวจภาษาอังกฤษ (CEFR Evaluator)")
st.write("ระบบวิเคราะห์ระดับภาษาและไวยากรณ์สำหรับนักเรียนมัธยม")

# สร้างช่องให้กรอก API Key ผ่านหน้าเว็บ (เพื่อความปลอดภัย จะได้ไม่ต้องฝังในโค้ด)
SECRET_API_KEY = st.secrets["GEMINI_API_KEY"]
#api_key_input = st.text_input("ใส่รหัส API Key ของคุณเพื่อเริ่มใช้งาน:", type="password")

# กล่องข้อความให้นักเรียนพิมพ์
student_text = st.text_area("พิมพ์ประโยคภาษาอังกฤษของคุณที่นี่:", "I has two dog, they is very cute.")

# 2. ลอจิกเมื่อกดปุ่ม "ส่งคำตอบ"
if st.button("ส่งให้ AI ตรวจ"):
    # if not api_key_input:
    #     st.warning("⚠️ กรุณาใส่ API Key ด้านบนก่อนครับ")
    # else:
        # แสดงแอนิเมชันหมุนๆ ระหว่างรอ AI คิด
        with st.spinner('กำลังวิเคราะห์โครงสร้างประโยค...'):
            try:
                # โค้ดเชื่อมต่อ API (เหมือนที่คุณเพิ่งรันผ่าน)
                client = genai.Client(api_key=SECRET_API_KEY)
                #client = genai.Client(api_key=api_key_input)
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
                
                # แปลงผลลัพธ์ JSON เป็น Dictionary
                result = json.loads(response.text)
                
                # 3. นำผลลัพธ์มาแสดงโชว์บนหน้าเว็บ
                st.success("ประเมินเสร็จสิ้น!")
                
                # แบ่งหน้าจอเป็น 2 คอลัมน์เพื่อโชว์คะแนน
                col1, col2 = st.columns(2)
                col1.metric(label="ระดับ CEFR", value=result['cefr_level'])
                col2.metric(label="คะแนนไวยากรณ์", value=f"{result['grammar_score']}/10")
                
                st.info(f"💡 **คำแนะนำจาก AI:** {result['feedback']}")
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")