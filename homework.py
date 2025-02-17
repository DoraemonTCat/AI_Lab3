import streamlit as st
from rdflib import Graph, URIRef, Literal, Namespace

g = Graph()
g.parse("mytourism.owl", format="xml")

tourism = Namespace("http://www.my_ontology.edu/mytourism#")

def get_province_mapping():
    provinces = ["ChiangMai", "NakhonSawan", "Phitsanulok", "Pichit", "Uthaithani"] #เอาไว้เช็คดูว่าในไฟล์ที่อัปโหลดมามีชื่อพวกนี้อยู่มั้ยและชื่อที่สอดคล้องกัน
    mapping = {}
    
    for province in provinces:
        province_uri = URIRef(f"http://www.my_ontology.edu/mytourism#{province}")
       #ไว้ดูภาษาไทยนะ
        for thai_name in g.objects(province_uri, tourism.hasNameOfProvince):
            if isinstance(thai_name, Literal) and thai_name.language == "th":
                mapping[str(thai_name)] = province
        #ไว้ดูอังกฤษนะ
        for english_name in g.objects(province_uri, tourism.hasNameOfProvince):
            if isinstance(english_name, Literal) and (english_name.language == "en" or english_name.language is None):
                mapping[str(english_name)] = province
    return mapping

def get_province_details(province_name, lang):
    province_uri = URIRef(f"http://www.my_ontology.edu/mytourism#{province_name}")
    details = {}
    
    properties = {
        "hasFlower": "ดอกไม้ประจำจังหวัด",
        "hasImageOfProvince": "รูปภาพของจังหวัด",
        "hasLatitudeOfProvince": "ละติจูดของจังหวัด",
        "hasLongitudeOfProvince": "ลองจิจูดของจังหวัด",
        "hasMotto": "คำขวัญของจังหวัด",
        "hasNameOfProvince": "ชื่อจังหวัด",
        "hasSeal": "สัญลักษณ์ประจำจังหวัด",
        "hasTraditionalNameOfProvince": "ชื่ออื่น ๆ ของจังหวัด",
        "hasTree": "ต้นไม้ประจำจังหวัด",
        "hasURLOfProvince": "เว็บไซต์ของจังหวัด"
    }
    
    for prop, label in properties.items():
        prop_uri = URIRef(f"http://www.my_ontology.edu/mytourism#{prop}")
        for obj in g.objects(province_uri, prop_uri):
            if isinstance(obj, Literal) and obj.language == lang:
                details[label] = str(obj)
            elif isinstance(obj, Literal) and obj.language is None:
                details[label] = str(obj)
    
    return details

st.set_page_config(page_title="ค้นหาจังหวัดในประเทศไทย", layout="wide")

st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f9;
        color: #333;
    }
    .stTextInput, .stRadio {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px;
        font-size: 16px;
    }
    .stButton {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 8px;
    }
    .stText {
        font-size: 16px;
    }
    .stMarkdown {
        font-size: 18px;
        font-weight: bold;
    }
    .stTitle {
        font-size: 24px;
        font-weight: 600;
    }
    .stRadio label {
        font-size: 18px;
    }
    .header {
        background-color: orange;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid black;
    }
    .province-details {
        background-color: rgb(224, 159, 39);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .province-details h2 {
        color:rgb(79, 88, 79);
    }
    .province-details p {
        font-size: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1>ค้นหาจังหวัดในประเทศไทย</h1></div>', unsafe_allow_html=True)

province_mapping = get_province_mapping()

province_input = st.text_input("กรอกชื่อจังหวัด:")

lang = st.radio("เลือกภาษา:", ["th", "en"])

if province_input:
    province_name = None
    for name, eng_name in province_mapping.items():
        if province_input.lower() == name.lower() or province_input.lower() == eng_name.lower():
            province_name = eng_name
            break
    
    if province_name:
        details = get_province_details(province_name, lang)
        if details:
            st.markdown("""<hr style="border: 1px solid black;">""", unsafe_allow_html=True)
            st.markdown(f'<div class="province-details"><h5>รายละเอียดของจังหวัด {province_name}</h5>', unsafe_allow_html=True)
            for key, value in details.items():
                st.markdown(f'<p><strong>{key}:</strong> {value}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("ไม่พบข้อมูลจังหวัดนี้")
    else:
        st.error("ไม่พบจังหวัดที่ตรงกับคำค้นหา")
