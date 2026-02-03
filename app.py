import streamlit as st
import time

# ==============================================================================
# 1. [시스템 설정 & 스타일 정의]
# ==============================================================================
st.set_page_config(
    page_title="Schneider AI Advisor",
    page_icon="🇩🇪",
    layout="centered"
)

# --- [CSS: 다크모드 방지 & 가독성 최적화] ---
st.markdown("""
    <style>
    /* [기본 설정] 스마트폰 다크모드 무시 -> 흰 배경/검은 글씨 강제 */
    :root {
        --primary-color: #004B87;
        --background-color: #ffffff;
        --secondary-background-color: #f0f2f6;
        --text-color: #000000;
        --font: sans-serif;
    }
    
    /* 앱 전체 배경 흰색 고정 */
    [data-testid="stAppViewContainer"] {
        background-color: #F8F9FA;
        color: #000000 !important;
    }
    
    /* 기본 텍스트 검은색 고정 (!important로 강제) */
    h1, h2, h3, h4, h5, h6, p, li, div, label, input, textarea {
        color: #000000 !important;
    }
    
    /* 라디오/체크박스 라벨 검은색 */
    .stRadio label, .stCheckbox label, .stMultiSelect label {
        color: #333333 !important;
        font-weight: 600;
    }

    /* [중요] 파란 배경 위 흰색 글씨 강제 설정 */
    /* 1. 버튼 (Button) */
    div.stButton > button:first-child {
        background-color: #004B87 !important;
        color: #ffffff !important; /* 흰색 글씨 */
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #003366 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    div.stButton > button p {
        color: #ffffff !important; /* 버튼 내부 텍스트 흰색 강제 */
    }

    /* 2. 진행바 (Progress Bar) */
    .stProgress > div > div > div > div {
        background-color: #004B87;
    }

    /* 3. 결과 박스 (Result Box) - 파란 그라데이션 배경 */
    .final-result-box {
        background: linear-gradient(135deg, #004B87 0%, #0066CC 100%);
        padding: 35px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0, 75, 135, 0.4);
    }
    
    /* 결과 박스 내부의 모든 텍스트는 흰색이어야 함 */
    .final-result-box h1, 
    .final-result-box h2,
    .final-result-box p, 
    .final-result-box span, 
    .final-result-box div {
        color: #ffffff !important;
    }

    /* [UI 카드 스타일] */
    .question-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-top: 5px solid #004B87;
    }
    
    /* Why 설명 박스 */
    .why-box {
        background-color: #f0f7ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #004B87;
        margin-bottom: 15px;
    }
    .why-box p, .why-box b {
        color: #333333 !important; /* 여기는 검은 글씨 */
    }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1

# 렌즈 데이터베이스
lens_catalog = {
    "prog_flagship": {"name": "S-90 Starlight Lifestyle +", "price": "₩800,000~", "features": ["라이프스타일 3Type 개인맞춤", "동공 크기 반영 고해상도", "양안시 최적화 기술"]},
    "prog_high":     {"name": "S-90 Starlight +", "price": "₩650,000~", "features": ["넓은 원/중/근 시야 밸런스", "자연스러운 시선 이동", "디지털 기기 피로 감소"]},
    "prog_premium":  {"name": "S-90 Platinum +", "price": "₩520,000~", "features": ["Swim Effect Control (울렁임 제어)", "주변부 왜곡 최소화", "빠른 적응력"]},
    "prog_standard": {"name": "S-90 Gold +", "price": "₩360,000~", "features": ["합리적인 가격과 성능 밸런스", "표준적인 누진 설계", "소프트한 시야감"]},
    "prog_entry":    {"name": "S-90 Pro +", "price": "₩270,000~", "features": ["경제적인 가격", "기본에 충실한 원용/근용 시야"]},
    "hue_plus":      {"name": "S-90 Hue +", "price": "₩360,000~", "features": ["8가지 정밀 조절력 타입", "스마트폰 피로 완화", "부드러운 도수 변화"]},
    "office_350":    {"name": "S-90 Office 350+", "price": "₩470,000~", "features": ["회의실 및 프레젠테이션 거리(4m)", "편안한 자세 유지", "실내 공간 시야 확장"]},
    "office_150":    {"name": "S-90 Office 150+", "price": "₩470,000~", "features": ["PC와 서류, 고객 응대(2m)", "넓은 중근거리 시야", "고개 듦 현상 방지"]},
    "office_80":     {"name": "S-90 Office 80+", "price": "₩360,000~", "features": ["모니터/키보드/독서(1m) 특화", "최대 시야폭 제공", "목/어깨 피로 최소화"]},
    "drive_stock":   {"name": "Schneider Drive", "price": "₩300,000", "features": ["대향차 라이트 눈부심 차단", "대비감도 향상", "동공 확장 시 수차 제어"]},
    "bp_stock":      {"name": "Schneider BP 174", "price": "₩380,000", "features": ["세계 최고 굴절률 1.74 소재", "유해 블루라이트 차단", "가장 얇은 두께"]},
    "reins_custom":  {"name": "S-90 Reins +", "price": "₩300,000~", "features": ["주변부 흐림/왜곡 제거", "360도 수차 제어 기술", "가장 선명한 시야"]}
}

def get_estimated_add(age):
    if age < 38: return "가입도 불필요"
    elif age < 42: return "+0.75 ~ +1.00 D"
    elif age < 45: return "+1.00 ~ +1.25 D"
    elif age < 48: return "+1.50 ~ +1.75 D"
    elif age < 52: return "+1.75 ~ +2.00 D"
    elif age < 56: return "+2.00 ~ +2.25 D"
    elif age < 60: return "+2.25 ~ +2.50 D"
    else: return "+2.50 D (Max)"

def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1
def restart(): 
    st.session_state.step = 1
    st.rerun()

# ==============================================================================
# 2. [UI 헤더] 고화질 로고 적용
# ==============================================================================
# [수정] 파일 대신 공식 SVG URL 사용 (해상도 문제 해결)
logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Schneider_Kreuznach_Logo.svg/2560px-Schneider_Kreuznach_Logo.svg.png"

col_logo, col_empty = st.columns([1, 1.5])
# width를 300으로 키워 더 시원하게 보이게 조정
st.image(logo_url, width=300) 

st.progress(st.session_state.step * 20)
st.markdown("---")

# ==============================================================================
# 3. [문진 프로세스]
# ==============================================================================

# [STEP 1] 기본 프로필
if st.session_state.step == 1:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("Step 1. 고객 프로필")
    col1, col2 = st.columns(2)
    with col1: st.session_state.age = st.number_input("고객 연령", 10, 100, 45)
    with col2: st.session_state.gender = st.selectbox("성별", ["남성", "여성"])
    
    st.markdown("<br>**현재 안경 착용 상태**", unsafe_allow_html=True)
    st.session_state.history = st.radio("상태 선택", ["안경 없음(나안)", "단초점 안경", "기능성(피로완화)", "누진다초점 안경"], label_visibility="collapsed")
    
    st.session_state.fail_check = False
    if st.session_state.history == "누진다초점":
        st.warning("⚠️ 과거 누진 안경 적응에 어려움이 있었습니까?")
        st.session_state.fail_check = st.checkbox("네, 적응이 힘들었습니다.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.button("다음 (Next) 👉", on_click=next_step, type="primary", use_container_width=True)

# [STEP 2] 불편 증상
elif st.session_state.step == 2:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("Step 2. 시각적 불편 정밀 분석")
    st.markdown("**1. 주된 불편 증상 (CC)**")
    st.session_state.main_cc = st.radio("CC 선택", ["근거리 흐림 (작은 글씨/폰)", "원거리 흐림 (표지판/TV)", "오후 시간대 눈의 피로/충혈", "야간 운전 시 빛 번짐/눈부심"], label_visibility="collapsed")
    
    st.markdown("<br>**2. 상세 증상 (Associated Symptoms)**", unsafe_allow_html=True)
    st.session_state.sub_symptoms = st.multiselect("상세 선택", ["초점 전환 딜레이", "대비 감도 저하", "야간 시력 저하", "광과민 (눈부심)", "주변부 울렁임"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.button("👈 이전", on_click=prev_step, use_container_width=True)
    c2.button("다음 (Next) 👉", on_click=next_step, type="primary", use_container_width=True)

# [STEP 3] 시습관
elif st.session_state.step == 3:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("Step 3. 시습관 및 자세")
    st.markdown("**1. 작은 글씨 볼 때 자세 (Posture)**")
    st.session_state.posture = st.radio("자세", ["자연스러운 자세", "안경 벗거나 고개 젖힘", "팔을 멀리/가까이 조절"], label_visibility="collapsed")
    
    st.markdown("<br>**2. 이동 중 시각 활동**", unsafe_allow_html=True)
    st.session_state.dynamic_vision = st.radio("동적 시야", ["정적 (멈춰서 확인)", "동적 (걸으면서 확인)"], horizontal=True)
    
    st.markdown("<br>**3. 운전 습관**", unsafe_allow_html=True)
    st.session_state.drive_pattern = st.radio("운전", ["운전 안 함", "전방 주시 위주", "멀티 태스킹 (네비/사이드 교차)"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.button("👈 이전", on_click=prev_step, use_container_width=True)
    c2.button("다음 (Next) 👉", on_click=next_step, type="primary", use_container_width=True)

# [STEP 4] 환경
elif st.session_state.step == 4:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("Step 4. 환경 및 민감도")
    st.markdown("**1. 활동 공간 (Indoor/Outdoor)**")
    st.session_state.env_ratio = st.select_slider("비중", options=["실내 90%", "실내 70%", "밸런스 (50:50)", "실외 70%", "실외 90%"])
    
    st.markdown("<br>**2. 디지털 기기 사용량**", unsafe_allow_html=True)
    st.session_state.digital_intensity = st.radio("디지털", ["Light (3시간 미만)", "Moderate (4~6시간)", "Heavy (7시간 이상)"], horizontal=True)
    
    st.markdown("<br>**3. 예민도 체크**", unsafe_allow_html=True)
    st.session_state.sensitivity_check = st.multiselect("예민도", ["계단 내려갈 때 울렁임", "고개 돌릴 때 어지러움", "새 안경 적응 느림"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("**4. 선호 등급**")
    st.session_state.grade_pref = st.selectbox("등급", ["Flagship (최고 사양)", "High-End (고성능)", "Premium (안정성)", "Standard (가성비)", "Entry (입문)"], index=2)
    st.markdown('</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.button("👈 이전", on_click=prev_step, use_container_width=True)
    c2.button("🔍 AI 분석 실행", on_click=next_step, type="primary", use_container_width=True)

# [STEP 5] 결과
elif st.session_state.step == 5:
    with st.spinner('🇩🇪 Schneider Optical Brain 분석 중...'):
        time.sleep(1.5)

    # 변수 할당
    age = st.session_state.age
    history = st.session_state.history
    main_cc = st.session_state.main_cc
    sub_symptoms = st.session_state.sub_symptoms
    posture = st.session_state.posture
    dynamic = st.session_state.dynamic_vision
    drive = st.session_state.drive_pattern
    env = st.session_state.env_ratio
    digital = st.session_state.digital_intensity
    sens_list = st.session_state.sensitivity_check
    grade_pref = st.session_state.grade_pref
    
    key = ""
    why_text = ""
    sub_type = ""
    is_sensitive = len(sens_list) > 0 or st.session_state.fail_check
    
    # 로직 (Ver 5.0과 동일)
    if (age >= 38 and "근거리" in main_cc) or (age >= 45):
        if "실내" in env and history != "누진다초점" and drive == "운전 안 함":
            if "자세" in posture or "팔을" in posture: 
                if "Light" not in digital: 
                    key = "office_150"
                    why_text = "데스크 업무와 실내 생활 비중이 높습니다. 누진보다 넓은 중근거리 시야를 제공하는 오피스 렌즈가 업무 효율을 높여줍니다."
        if key == "":
            if "실외" in env or "동적" in dynamic or "멀티" in drive:
                lifestyle_type = "Dynamic"
                why_text = "활동적인 라이프스타일과 잦은 시선 이동을 고려하여, 원거리 시야가 넓고 울렁임이 적은 설계를 채택했습니다."
            elif "실내 90%" in env:
                lifestyle_type = "Static"
                why_text = "근거리 집중도가 높은 환경입니다. 스마트폰과 독서 영역이 강화된 정밀 근용 설계를 채택했습니다."
            else:
                lifestyle_type = "Allround"
                why_text = "실내외 활동의 밸런스가 중요합니다. 모든 거리에서 균형 잡힌 시야를 제공하는 표준 설계를 채택했습니다."

            if is_sensitive or "초점 전환 딜레이" in sub_symptoms:
                key = "prog_premium" if lifestyle_type == "Static" else "prog_high"
                why_text += " 특히 예민한 시각 특성과 울렁임을 제어하기 위해 상위 등급의 [Swim Effect Control] 기술이 필수적입니다."
            else:
                if "Flagship" in grade_pref: key = "prog_flagship"
                elif "High-End" in grade_pref: key = "prog_high"
                elif "Premium" in grade_pref: key = "prog_premium"
                elif "Standard" in grade_pref: key = "prog_standard"
                else: key = "prog_entry"
                why_text += " 고객님의 예산 선호도와 필요 성능을 고려하여 최적의 가성비를 갖춘 모델을 매칭했습니다."
            sub_type = lifestyle_type

    elif "피로" in main_cc:
        key = "hue_plus"
        why_text = "오후 시간대의 눈 피로는 '조절력 부족' 신호입니다. 8가지 정밀 타입으로 눈의 힘을 덜어주는 기능성 렌즈가 필요합니다."
    elif "야간" in main_cc or "야간 시력 저하" in sub_symptoms:
        key = "drive_stock"
        why_text = "야간 운전 시 대향차 라이트 눈부심과 대비감도 저하를 호소하셨습니다. 특수 코팅으로 빛 번짐을 억제해야 합니다."
    else:
        if "Heavy" in digital:
            key = "bp_stock"
            why_text = "디지털 기기 노출이 많아 시력 보호가 시급합니다. 강력한 블루라이트 차단 소재(Blue Protect)를 처방합니다."
        else:
            key = "reins_custom"
            why_text = "주변부 왜곡이나 흐림 없는 가장 맑고 깨끗한 해상도를 위해, 개인맞춤 단초점 렌즈를 추천합니다."

    final_lens = lens_catalog.get(key, lens_catalog["prog_standard"])
    add_val = get_estimated_add(age)

    # [결과 화면 UI]
    st.balloons()
    
    # 1. 메인 결과 박스 (파란 배경 + 흰색 글씨 강제)
    st.markdown(f"""
    <div class="final-result-box">
        <p style="font-size: 1.2rem; margin-bottom: 5px; opacity: 0.9;">AI Recommendation</p>
        <h1 style="font-size: 2.5rem; margin-top: 0;">{final_lens['name']}</h1>
        <p style="font-size: 1.5rem; font-weight: bold; margin-top: 10px;">가격: {final_lens['price']}</p>
        {'<span style="background:rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size:0.9rem;">Type: '+sub_type+'</span>' if sub_type else ''}
    </div>
    """, unsafe_allow_html=True)

    # 2. 분석 리포트 (Why)
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown("### 📊 분석 리포트")
    
    # Why 설명 박스 (흰색/연한 파란 배경 + 검은 글씨)
    st.markdown(f"""
    <div class="why-box">
        <b>💡 Why:</b> {why_text}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>**🛠️ 핵심 기술 (Key Features)**", unsafe_allow_html=True)
    for feat in final_lens['features']:
        st.markdown(f"- ✅ {feat}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. 임상 데이터
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown("### 👓 Clinical Data")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("고객 프로필")
        st.write(f"- 연령: {age}세 ({st.session_state.gender})")
        st.write(f"- 디지털: {digital}")
        if is_sensitive: st.write("- **⚠️ 예민도 높음**")
    with c2:
        st.caption("전문가 소견")
        st.write(f"- 권장 가입도: **{add_val}**")
        st.write(f"- 분류: {'기능성/오피스' if 'Office' in final_lens['name'] or 'Hue' in final_lens['name'] else '누진 다초점'}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.button("🔄 새로운 고객 상담하기", on_click=restart, type="primary", use_container_width=True)
