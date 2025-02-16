import streamlit as st
from rdflib import Graph, URIRef, Literal, Namespace

g = Graph()
g.parse("mytourism.owl", format="xml")

tourism = Namespace("http://www.my_ontology.edu/mytourism#")

def get_province_mapping():
    provinces = ["ChiangMai", "NakhonSawan", "Phitsanulok", "Pichit", "Uthaithani"]
    mapping = {}
    
    for province in provinces:
        province_uri = URIRef(f"http://www.my_ontology.edu/mytourism#{province}")
        # Fetch Thai name
        for thai_name in g.objects(province_uri, tourism.hasNameOfProvince):
            if isinstance(thai_name, Literal) and thai_name.language == "th":
                mapping[str(thai_name)] = province
        # Fetch English name
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

st.set_page_config(page_title="ค้นหาจังหวัดในประเทศไทย")

st.markdown("""
            <style>
            .CT{
                text-align: center;
              
            }
            """, unsafe_allow_html=True)
st.markdown('<h1 class="CT">ค้นหาจังหวัดในประเทศไทย</h1>', unsafe_allow_html=True)


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
    </style>
""", unsafe_allow_html=True)

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
            st.write(f"รายละเอียดของจังหวัด {province_name}:")
            for key, value in details.items():
                st.write(f"{key}: {value}")
        else:
            st.write("ไม่พบข้อมูลจังหวัดนี้")
    else:
        st.write("ไม่พบจังหวัดที่ตรงกับคำค้นหา")
