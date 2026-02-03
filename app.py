import streamlit as st
import time

# ==============================================================================
# 1. [시스템 설정 & 프리미엄 스타일(CSS)]
# ==============================================================================
st.set_page_config(
    page_title="Schneider AI Advisor",
    page_icon="🇩🇪",
    layout="centered"
)

# --- [디자인: 슈나이더 프리미엄 테마 적용] ---
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* 슈나이더 블루 컬러 정의: #004B87 */
    
    /* 진행바 (Progress Bar) 커스텀 */
    .stProgress > div > div > div > div {
        background-color: #004B87;
    }

    /* 버튼 스타일 (Primary) */
    div.stButton > button:first-child {
        background-color: #004B87;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #003366;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* 질문 카드 스타일 (컨테이너 박스) */
    .question-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-top: 5px solid #004B87;
    }
    
    /* 라디오 버튼 선택 강조 */
    .stRadio label {
        font-size: 16px;
        font-weight: 500;
        color: #333;
    }

    /* 헤더 텍스트 */
    h1, h2, h3 {
        color: #004B87;
        font-weight: 700;
    }
    
    /* 결과 박스 디자인 */
    .final-result-box {
        background: linear-gradient(135deg, #004B87 0%, #0066CC 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,75,135,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1

# 렌즈 데이터베이스
lens_catalog = {
    "prog_flagship": {
        "name": "S-90 Starlight Lifestyle +", 
        "price": "₩800,000~", 
        "desc": "100% 개인맞춤형 하이엔드 누진",
        "features": ["라이프스타일 3Type(Static/Allround/Dynamic) 선택", "동공 크기 반영 고해상도", "양안시 최적화 기술"]
    },
    "prog_high": {
        "name": "S-90 Starlight +", 
        "price": "₩650,000~", 
        "desc": "슈나이더 광학 기술의 시그니처 모델",
        "features": ["넓은 원/중/근 시야 밸런스", "자연스러운 시선 이동", "디지털 기기 피로 감소"]
    },
    "prog_premium": {
        "name": "S-90 Platinum +", 
        "price": "₩520,000~", 
        "desc": "울렁임 제어에 특화된 안정적 설계",
        "features": ["Swim Effect Control (울렁임 제어)", "주변부 왜곡 최소화", "빠른 적응력"]
    },
    "prog_standard": {
        "name": "S-90 Gold +", 
        "price": "₩360,000~", 
        "desc": "실패 없는 베스트셀러 모델",
        "features": ["합리적인 가격과 성능의 밸런스", "표준적인 누진 설계", "소프트한 시야감"]
    },
    "prog_entry": {
        "name": "S-90 Pro +", 
        "price": "₩270,000~", 
        "desc": "누진다초점 입문자를 위한 합리적 선택",
        "features": ["경제적인 가격", "기본에 충실한 원용/근용 시야"]
    },
    "hue_plus": {
        "name": "S-90 Hue +", 
        "price": "₩360,000~", 
        "desc": "초기 노안 및 디지털 눈 피로 완화",
        "features": ["8가지 정밀 조절력 타입", "스마트폰 피로 완화", "부드러운 도수 변화"]
    },
    "office_350": {
        "name": "S-90 Office 350+", 
        "price": "₩470,000~", 
        "desc": "실내 이동이 가능한 오피스 렌즈 (4m)",
        "features": ["회의실 및 프레젠테이션 거리 확보", "편안한 자세 유지", "실내 공간 시야 확장"]
    },
    "office_150": {
        "name": "S-90 Office 150+", 
        "price": "₩470,000~", 
        "desc": "데스크 업무 최적화 오피스 렌즈 (2m)",
        "features": ["PC와 서류, 내방 고객 응대", "넓은 중근거리 시야", "고개 듦 현상 방지"]
    },
    "office_80": {
        "name": "S-90 Office 80+", 
        "price": "₩360,000~", 
        "desc": "집중 업무형 오피스 렌즈 (1m)",
        "features": ["모니터와 키보드, 독서 거리 특화", "최대 시야폭 제공", "목/어깨 피로 최소화"]
    },
    "drive_stock": {
        "name": "Schneider Drive", 
        "price": "₩300,000", 
        "desc": "야간 운전 특화 렌즈",
        "features": ["대향차 라이트 눈부심 차단", "대비감도 향상", "동공 확장 시 수차 제어"]
    },
    "bp_stock": {
        "name": "Schneider BP 174", 
        "price": "₩380,000", 
        "desc": "초고굴절 블루라이트 차단",
        "features": ["세계 최고 굴절률 1.74 소재", "유해 블루라이트 차단", "가장 얇은 두께"]
    },
    "reins_custom": {
        "name": "S-90 Reins +", 
        "price": "₩300,000~", 
        "desc": "개인맞춤형 고해상도 단초점",
        "features": ["주변부 흐림/왜곡 제거", "360도 수차 제어 기술", "가장 선명한 시야"]
    }
}

def get_estimated_add(age):
    if age < 38: return "가입도 불필요 (조절력 양호)"
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
# 2. [UI 헤더]
# ==============================================================================
# 로고 영역
col_logo, col_empty = st.columns([1, 2])
try:
    st.image("logo.png", width=220)
except:
    st.markdown("## 🇩🇪 Schneider")

# 진행바
st.progress(st.session_state.step * 20)
st.markdown("---")

# ==============================================================================
# 3. [통합 정밀 문진 - 카드 UI 적용]
# ==============================================================================

# [STEP 1] 기본 프로필
if st.session_state.step == 1:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("Step 1. 고객 프로필")
    st.info("정확한 분석을 위해 기본 데이터를 입력해주세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.age = st.number_input("고객 연령", 10, 100, 45)
    with col2:
        st.session_state.gender = st.selectbox("성별", ["남성", "여성"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**현재 안경 착용 상태**")
    st.session_state.history = st.radio(
        "현재 안경 상태를 선택하세요",
        ["안경 없음(나안)", "단초점 안경", "기능성(피로완화)", "누진다초점 안경"],
        label_visibility="collapsed"
    )
    
    if st.session_state.history == "누진다초점":
        st.warning("⚠️ 과거 누진 안경 적응에 어려움이 있었습니까?")
        st.session_state.fail_check = st.checkbox("네, 적응이 힘들었습니다.")
    else:
        st.session_state.fail_check = False
    
    st.markdown('</div>', unsafe_allow_html=True) # 카드 닫기
    st.button("다음 (Next) 👉", on_click=next_step, type="primary", use_container_width=True)


# [STEP 2] 시각적 불편 정밀 분석
elif st.session_state.step == 2:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("Step 2. 시각적 불편 정밀 분석")
    
    st.markdown("**1. 주된 불편 증상 (CC)**")
    st.session_state.main_cc = st.radio(
        "가장 해결하고 싶은 불편함 하나를 선택하세요",
        ["근거리 흐림 (작은 글씨/폰)", "원거리 흐림 (표지판/TV)", "오후 시간대 눈의 피로/충혈", "야간 운전 시 빛 번짐/눈부심"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("**2. 정밀 상세 증상 (Associated Symptoms)**")
    st.caption("해당되는 항목을 모두 선택하세요.")
    st.session_state.sub_symptoms = st.multiselect(
        "상세 증상",
        [
            "초점 전환 딜레이 (멀리/가까이 볼 때 늦게 보임)", 
            "대비 감도 저하 (흐린 날/저녁에 유독 침침함)", 
            "야간 시력 저하 (밤이나 비 올 때 잘 안 보임)",
            "광과민 (터널 진출입/밝은 빛에 눈부심)",
            "주변부 울렁임 (고개를 돌릴 때 어지러움)"
        ],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.button("👈 이전", on_click=prev_step, use_container_width=True)
    col2.button("다음 (Next) 👉", on_click=next_step, type="primary", use_container_width=True)


# [STEP 3] 시습관 및 자세
elif st.session_state.step == 3:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("Step 3. 시습관 및 자세 분석")
    
    st.markdown("**1. 작은 글씨를 볼 때의 자세 (Posture)**")
    st.session_state.posture = st.radio(
        "독서/스마트폰 자세",
        ["자연스러운 자세 유지", "안경을 벗거나 고개를 뒤로 젖힘", "팔을 멀리 뻗거나 당겨서 거리 조절"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br>**2. 이동 중 시각 활동 (Dynamic Vision)**", unsafe_allow_html=True)
    st.session_state.dynamic_vision = st.radio(
        "이동 간 스마트폰 사용",
        ["정적 (멈춰서 확인)", "동적 (걸으면서 자주 확인)"],
        horizontal=True
    )
    
    st.markdown("<br>**3. 운전 시 시선 패턴 (Drive)**", unsafe_allow_html=True)
    st.session_state.drive_pattern = st.radio(
        "운전 습관",
        ["운전 안 함", "전방 주시 위주", "멀티 태스킹 (네비/사이드미러 교차 확인)"],
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.button("👈 이전", on_click=prev_step, use_container_width=True)
    col2.button("다음 (Next) 👉", on_click=next_step, type="primary", use_container_width=True)


# [STEP 4] 환경 및 민감도
elif st.session_state.step == 4:
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("Step 4. 환경 및 민감도")
    
    st.markdown("**1. 주된 활동 공간 (Indoor/Outdoor)**")
    st.session_state.env_ratio = st.select_slider(
        "실내 vs 실외 비중",
        options=["실내 90% (사무직/가사)", "실내 70%", "밸런스 (50:50)", "실외 70%", "실외 90% (현장/영업)"]
    )
    
    st.markdown("<br>**2. 디지털 기기 사용 비중**", unsafe_allow_html=True)
    st.session_state.digital_intensity = st.radio(
        "하루 디지털 기기 사용량",
        ["Light (3시간 미만)", "Moderate (4~6시간)", "Heavy (7시간 이상)"],
        horizontal=True
    )
    
    st.markdown("<br>**3. 공간 감각 예민도 (Sensitivity)**", unsafe_allow_html=True)
    st.session_state.sensitivity_check = st.multiselect(
        "예민도 체크 (해당 시 선택)",
