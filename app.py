import streamlit as st
import time
import os

# ==============================================================================
# 1. [시스템 설정 & 스타일 정의]
# ==============================================================================
st.set_page_config(
    page_title="슈나이더 AI 어드바이저",
    page_icon="🇩🇪",
    layout="centered"
)

# --- [CSS: 다크모드 방지 & 가독성 최적화 & 한글 폰트] ---
st.markdown("""
    <style>
    /* [기본 설정] 스마트폰 다크모드 무시 -> 흰 배경/검은 글씨 강제 */
    :root {
        --primary-color: #004B87;
        --background-color: #ffffff;
        --secondary-background-color: #f0f2f6;
        --text-color: #000000;
        --font: "Pretendard", "Malgun Gothic", sans-serif; /* 한글 폰트 최적화 */
    }
    
    /* 앱 전체 배경 흰색 고정 */
    [data-testid="stAppViewContainer"] {
        background-color: #F8F9FA;
        color: #000000 !important;
    }
    
    /* 기본 텍스트 검은색 고정 */
    h1, h2, h3, h4, h5, h6, p, li, div, label, input, textarea {
        color: #000000 !important;
        font-family: "Pretendard", "Malgun Gothic", sans-serif;
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
        color: #ffffff !important;
    }

    /* 2. 진행바 (Progress Bar) */
    .stProgress > div > div > div > div {
        background-color: #004B87;
    }

    /* 3. 결과 박스 (Result Box) */
    .final-result-box {
        background: linear-gradient(135deg, #004B87 0%, #0066CC 100%);
        padding: 35px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0, 75, 135, 0.4);
    }
    
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
        color: #333333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1

# 렌즈 데이터베이스 (한글화 완료)
lens_catalog = {
    "prog_flagship": {"name": "S-90 Starlight Lifestyle +", "price": "₩800,000~", "features": ["라이프스타일 3타입(정적/밸런스/동적) 개인맞춤", "동공 크기 반영 고해상도 설계", "양안시 최적화 기술 적용"]},
    "prog_high":     {"name": "S-90 Starlight +", "price": "₩650,000~", "features": ["원/중/근 모든 거리의 넓은 시야 밸런스", "자연스럽고 편안한 시선 이동", "디지털 기기 눈 피로 감소"]},
    "prog_premium":  {"name": "S-90 Platinum +", "price": "₩520,000~", "features": ["Swim Effect Control (울렁임 제어 기술)", "렌즈 주변부 왜곡 최소화", "빠른 적응력 제공"]},
    "prog_standard": {"name": "S-90 Gold +", "price": "₩360,000~", "features": ["합리적인 가격과 우수한 성능의 조화", "한국인에게 최적화된 표준 누진 설계", "부드럽고 소프트한 시야감"]},
    "prog_entry":    {"name": "S-90 Pro +", "price": "₩270,000~", "features": ["경제적인 가격의 슈나이더 입문형", "기본에 충실한 원용/근용 시야 확보"]},
    "hue_plus":      {"name": "S-90 Hue +", "price": "₩360,000~", "features": ["8가지 정밀 조절력(ADD) 타입", "스마트폰/PC 눈 피로 완화", "초기 노안을 위한 부드러운 도수 변화"]},
    "office_350":    {"name": "S-90 Office 350+", "price": "₩470,000~", "features": ["회의실 및 프레젠테이션 거리(4m) 확보", "편안한 자세 유지 및 실내 이동 가능", "실내 공간 시야 확장"]},
    "office_150":    {"name": "S-90 Office 150+", "price": "₩470,000~", "features": ["PC와 서류, 내방 고객 응대(2m) 최적화", "넓은 중근거리 시야 제공", "턱을 드는 현상(거북목) 방지"]},
    "office_80":     {"name": "S-90 Office 80+", "price": "₩360,000~", "features": ["모니터/키보드/독서(1m) 집중형", "화면 전체를 볼 수 있는 최대 시야폭", "목/어깨 피로 최소화"]},
    "drive_stock":   {"name": "Schneider Drive", "price": "₩300,000", "features": ["대향차 라이트 눈부심 획기적 차단", "야간/우천 시 대비감도 향상", "동공 확장 시 발생하는 수차 제어"]},
    "bp_stock":      {"name": "Schneider BP 174", "price": "₩380,000", "features": ["세계 최고 굴절률 1.74(가장 얇은) 소재", "유해 블루라이트 차단 기능", "가볍고 얇은 두께"]},
    "reins_custom":  {"name": "S-90 Reins +", "price": "₩300,000~", "features": ["주변부 흐림/왜곡을 제거한 개인맞춤 단초점", "360도 수차 제어 기술", "가장 선명하고 맑은 해상도"]}
}

def get_estimated_add(age):
    if age < 38: return "가입도 불필요 (조절력 충분)"
    elif age < 42: return "+0.75 ~ +1.00 D (초기)"
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
# 2. [UI 헤더] 로고 3중 안전장치
# ==============================================================================
col_logo, col_empty = st.columns([1, 1.5])

with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=280)
    elif os.path.exists("Logo.png"):
        st.image("Logo.png", width=280)
    else:
        try:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Schneider_Kreuznach_Logo.svg/800px-Schneider_Kreuznach_Logo.svg.png", width=280)
        except:
            st.markdown("## 🇩🇪 Schneider")

st.progress(st.session_state.step * 20)
st.markdown("---")

# ==============================================================================
# 3. [문진 프로세스] (완벽한 한글화)
# ==============================================================================

# [STEP 1] 기본 프로필 (누진 실패 체크 로직 복구됨)
if st.session_state.step == 1:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("1단계. 고객 프로필")
    col1, col2 = st.columns(2)
    with col1: st.session_state.age = st.number_input("고객 연령", 10, 100, 45)
    with col2: st.session_state.gender = st.selectbox("성별", ["남성", "여성"])
    
    st.markdown("<br>**현재 안경 착용 상태**", unsafe_allow_html=True)
    st.session_state.history = st.radio(
        "상태 선택", 
        ["안경 없음(나안)", "단초점 안경", "기능성(피로완화)", "누진다초점 안경"], 
        label_visibility="collapsed"
    )
    
    # [복구된 로직] 누진다초점 선택 시에만 체크박스 등장
    st.session_state.fail_check = False # 기본값 초기화
    if st.session_state.history == "누진다초점 안경":
        st.markdown("<br>", unsafe_allow_html=True)
        st.warning("🔍 **체크포인트:** 과거 누진 안경 사용 시 울렁임이나 부적응 경험이 있습니까?")
        st.session_state.fail_check = st.checkbox("네, 적응이 힘들었습니다.")
        
    st.markdown('</div>', unsafe_allow_html=True)
    st.button("다음 단계로 👉", on_click=next_step, type="primary", use_container_width=True)

# [STEP 2] 불편 증상
elif st.session_state.step == 2:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("2단계. 시각적 불편 정밀 분석")
    st.markdown("**1. 가장 해결하고 싶은 주호소 (CC)**")
    st.session_state.main_cc = st.radio("CC 선택", ["근거리 흐림 (작은 글씨/폰)", "원거리 흐림 (표지판/TV)", "오후 시간대 눈의 피로/충혈", "야간 운전 시 빛 번짐/눈부심"], label_visibility="collapsed")
    
    st.markdown("<br>**2. 동반되는 상세 증상 (복수 선택)**", unsafe_allow_html=True)
    st.session_state.sub_symptoms = st.multiselect("상세 선택", ["초점 전환 딜레이 (초점 늦게 맺힘)", "대비 감도 저하 (흐린 날 침침함)", "야간 시력 저하", "광과민 (빛 번짐/눈부심)", "주변부 울렁임/어지러움"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.button("👈 이전 단계", on_click=prev_step, use_container_width=True)
    c2.button("다음 단계로 👉", on_click=next_step, type="primary", use_container_width=True)

# [STEP 3] 시습관
elif st.session_state.step == 3:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("3단계. 시습관 및 자세 분석")
    st.markdown("**1. 작은 글씨를 볼 때의 자세 (Posture)**")
    st.session_state.posture = st.radio("자세", ["자연스러운 자세 유지", "안경을 벗거나 고개를 뒤로 젖힘", "팔을 멀리 뻗거나 당겨서 거리 조절"], label_visibility="collapsed")
    
    st.markdown("<br>**2. 이동 중 시각 활동 (동적 시야)**", unsafe_allow_html=True)
    st.session_state.dynamic_vision = st.radio("동적 시야", ["정적 (멈춰서 확인)", "동적 (걸으면서 스마트폰 확인)"], horizontal=True)
    
    st.markdown("<br>**3. 운전 시 시선 이동 패턴**", unsafe_allow_html=True)
    st.session_state.drive_pattern = st.radio("운전", ["운전 안 함", "전방 주시 위주", "멀티 태스킹 (네비/사이드 교차 확인)"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.button("👈 이전 단계", on_click=prev_step, use_container_width=True)
    c2.button("다음 단계로 👉", on_click=next_step, type="primary", use_container_width=True)

# [STEP 4] 환경
elif st.session_state.step == 4:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("4단계. 환경 및 민감도 분석")
    st.markdown("**1. 주된 활동 공간 (실내/실외)**")
    st.session_state.env_ratio = st.select_slider("비중", options=["실내 90% (사무직/가사)", "실내 70%", "밸런스 (50:50)", "실외 70%", "실외 90% (현장/영업)"])
    
    st.markdown("<br>**2. 하루 디지털 기기 사용량**", unsafe_allow_html=True)
    st.session_state.digital_intensity = st.radio("디지털", ["Light (3시간 미만)", "Moderate (4~6시간)", "Heavy (7시간 이상)"], horizontal=True)
    
    st.markdown("<br>**3. 시각적 예민도 체크**", unsafe_allow_html=True)
    st.session_state.sensitivity_check = st.multiselect("예민도", ["계단을 내려갈 때 바닥이 울렁거림", "고개를 빠르게 돌릴 때 어지러움", "새로운 안경 적응이 느린 편"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("**4. 선호하는 렌즈 등급**")
    st.session_state.grade_pref = st.selectbox("등급", ["Flagship (최고 사양)", "High-End (고성능)", "Premium (안정성)", "Standard (가성비)", "Entry (입문형)"], index=2)
    st.markdown('</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.button("👈 이전 단계", on_click=prev_step, use_container_width=True)
    c2.button("🔍 AI 정밀 분석 실행", on_click=next_step, type="primary", use_container_width=True)

# [STEP 5] 결과 (완벽한 한글화)
elif st.session_state.step == 5:
    with st.spinner('🇩🇪 슈나이더 광학 알고리즘이 분석 중입니다...'):
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
    
    # 분석 로직 (Ver 5.0 로직 유지)
    if (age >= 38 and "근거리" in main_cc) or (age >= 45):
        if "실내" in env and history != "누진다초점 안경" and drive == "운전 안 함":
            if "자세" in posture or "팔을" in posture: 
                if "Light" not in digital: 
                    key = "office_150"
                    why_text = "데스크 업무와 실내 생활 비중이 높습니다. 일반 누진 렌즈보다 훨씬 넓은 중근거리 시야를 제공하는 오피스 렌즈가 업무 효율을 극대화해 줍니다."
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
                why_text += " 특히 고객님의 예민한 시각 특성과 울렁임을 제어하기 위해 상위 등급의 **[Swim Effect Control]** 기술이 필수적입니다."
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
    
    # 1. 메인 결과 박스
    st.markdown(f"""
    <div class="final-result-box">
        <p style="font-size: 1.2rem; margin-bottom: 5px; opacity: 0.9;">AI 추천 결과</p>
        <h1 style="font-size: 2.5rem; margin-top: 0;">{final_lens['name']}</h1>
        <p style="font-size: 1.5rem; font-weight: bold; margin-top: 10px;">시작 가격: {final_lens['price']}</p>
        {'<span style="background:rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size:0.9rem;">타입: '+sub_type+'</span>' if sub_type else ''}
    </div>
    """, unsafe_allow_html=True)

    # 2. 분석 리포트
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown("### 📊 정밀 분석 리포트")
    
    # Why 설명 박스
    st.markdown(f"""
    <div class="why-box">
        <b>💡 추천 근거:</b> {why_text}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>**🛠️ 제품 핵심 기술 (Key Features)**", unsafe_allow_html=True)
    for feat in final_lens['features']:
        st.markdown(f"- ✅ {feat}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. 임상 데이터
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown("### 👓 문진 데이터 요약")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("고객 프로필")
        st.write(f"- 연령: {age}세 ({st.session_state.gender})")
        st.write(f"- 디지털 사용량: {digital}")
        if is_sensitive: st.write("- **⚠️ 예민도 높음**")
    with c2:
        st.caption("전문가 소견")
        st.write(f"- 권장 가입도(ADD): **{add_val}**")
        st.write(f"- 렌즈 분류: {'기능성/오피스' if 'Office' in final_lens['name'] or 'Hue' in final_lens['name'] else '누진 다초점'}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.button("🔄 새로운 고객 상담하기", on_click=restart, type="primary", use_container_width=True)
