import streamlit as st
import time

# ==============================================================================
# 1. [시스템 설정 & 스타일]
# ==============================================================================
st.set_page_config(
    page_title="Schneider AI Advisor",
    page_icon="🇩🇪",
    layout="centered" # 집중도를 위해 중앙 정렬
)

# 세션 상태 초기화 (단계별 진행을 위해 필요)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# 렌즈 데이터베이스
lens_catalog = {
    "prog_flagship": {"name": "S-90 Starlight Lifestyle +", "price": "₩800,000~", "desc": "라이프스타일 3Type(Static/Allround/Dynamic) 개인맞춤"},
    "prog_high":     {"name": "S-90 Starlight +", "price": "₩650,000~", "desc": "슈나이더 기술력의 정점, 시그니처 모델"},
    "prog_premium":  {"name": "S-90 Platinum +", "price": "₩520,000~", "desc": "어지러움에 예민한 분들을 위한 넓은 시야 (마스터피스)"},
    "prog_standard": {"name": "S-90 Gold +", "price": "₩360,000~", "desc": "실패 없는 베스트셀러, 가격/성능 밸런스 최상"},
    "prog_entry":    {"name": "S-90 Pro +", "price": "₩270,000~", "desc": "합리적인 가격의 입문용 누진 렌즈"},
    "hue_plus":      {"name": "S-90 Hue +", "price": "₩360,000~", "desc": "8가지 타입 조절력 케어 (피로완화)"},
    "office_350":    {"name": "S-90 Office 350+ (4m)", "price": "₩470,000~", "desc": "회의실 및 실내 이동이 잦은 분 (4m)"},
    "office_150":    {"name": "S-90 Office 150+ (2m)", "price": "₩470,000~", "desc": "데스크 업무와 고객 응대 (2m)"},
    "office_80":     {"name": "S-90 Office 80+ (1m)", "price": "₩360,000~", "desc": "PC와 독서 집중형 (1m)"},
    "drive_stock":   {"name": "Schneider Drive (여벌)", "price": "₩300,000", "desc": "야간 빛 번짐 차단 (즉시 가공 가능)"},
    "bp_stock":      {"name": "Schneider BP 174 (여벌)", "price": "₩380,000", "desc": "1.74 초고굴절 + 블루라이트 소재 차단"},
    "reins_custom":  {"name": "S-90 Reins + (개인맞춤)", "price": "₩300,000~", "desc": "주변부 왜곡을 줄인 스마트 고해상도 단초점"}
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

# 다음 단계로 이동 함수
def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def restart():
    st.session_state.step = 1
    st.session_state.user_data = {}

# ==============================================================================
# 2. [UI 구성] 헤더 및 로고
# ==============================================================================
# 로고 표시 (logo.png가 같은 폴더에 있어야 함. 없으면 텍스트로 대체)
try:
    st.image("logo.png", width=300) # 슈나이더 로고 크기 조절
except:
    st.markdown("# 🇩🇪 Schneider")

st.markdown("### Professional AI Vision Advisor")
st.progress(st.session_state.step * 20) # 진행률 표시줄 (총 5단계 가정)

# ==============================================================================
# 3. [단계별 화면]
# ==============================================================================

# [STEP 1] 기본 프로필
if st.session_state.step == 1:
    st.header("Step 1. 고객 프로필")
    st.info("고객님의 기본 정보를 입력해주세요.")
    
    st.session_state.age = st.number_input("고객 연령", 10, 100, 45, key="age_input")
    st.session_state.gender = st.selectbox("성별", ["남성", "여성"], key="gender_input")
    
    st.session_state.current_glasses = st.radio(
        "현재 착용 안경", 
        ["없음(나안)", "일반 단초점", "기능성(피로완화)", "누진다초점"],
        key="glasses_input"
    )

    if st.session_state.current_glasses == "누진다초점":
        st.session_state.fail_check = st.checkbox("과거 누진 적응에 실패하거나 불편했던 경험이 있습니까?", key="fail_input")
    else:
        st.session_state.fail_check = False

    st.button("다음 단계 👉", on_click=next_step, type="primary")


# [STEP 2] 자각 증상
elif st.session_state.step == 2:
    st.header("Step 2. 불편 증상 확인")
    st.info("가장 해결하고 싶은 시각적 불편함은 무엇인가요?")
    
    st.session_state.symptoms = st.multiselect(
        "증상을 모두 선택하세요",
        [
            "작은 글씨 흐림 (스마트폰/서류)", 
            "오후 시간대 눈의 피로/충혈", 
            "야간 운전 시 빛 번짐/눈부심",
            "원거리 흐림 (표지판/TV)",
            "디지털 기기 장시간 사용"
        ],
        default=["작은 글씨 흐림 (스마트폰/서류)"],
        key="symptoms_input"
    )
    
    col1, col2 = st.columns(2)
    col1.button("👈 이전", on_click=prev_step)
    col2.button("다음 단계 👉", on_click=next_step, type="primary")


# [STEP 3] 라이프스타일
elif st.session_state.step == 3:
    st.header("Step 3. 라이프스타일")
    st.info("하루 중 눈을 가장 많이 사용하는 환경은?")
    
    st.session_state.work_dist = st.radio(
        "주된 작업 거리",
        [
            "A. 손 닿는 거리 (30~40cm) : 스마트폰, 독서",
            "B. 팔 뻗은 거리 (60~80cm) : PC, 데스크 업무",
            "C. 실내 공간 (1~4m) : 회의, 가사, 상담",
            "D. 원거리 (5m~) : 운전, 외근, 현장"
        ],
        key="dist_input"
    )
    
    st.session_state.digital_hours = st.slider("하루 디지털 기기 사용 시간 (시간)", 0, 24, 6, key="digital_input")
    st.session_state.driving = st.radio("운전 빈도", ["거의 안 함", "주간 위주", "야간 위주/장거리"], key="driving_input")

    col1, col2 = st.columns(2)
    col1.button("👈 이전", on_click=prev_step)
    col2.button("다음 단계 👉", on_click=next_step, type="primary")


# [STEP 4] 선호도 조사
elif st.session_state.step == 4:
    st.header("Step 4. 정밀 옵션")
    st.info("마지막으로 고객님의 성향을 체크합니다.")
    
    st.session_state.sensitivity = st.slider("시각적 예민도 (5: 매우 예민)", 1, 5, 3, key="sens_input")
    
    st.session_state.grade_pref = st.selectbox(
        "선호하는 렌즈 등급",
        ["Flagship (최고 사양)", "High-End (고성능)", "Premium (안정성)", "Standard (가성비)", "Entry (입문)"],
        index=2,
        key="grade_input"
    )

    col1, col2 = st.columns(2)
    col1.button("👈 이전", on_click=prev_step)
    col2.button("🔍 AI 분석 결과 보기", on_click=next_step, type="primary")


# [STEP 5] 최종 결과 리포트
elif st.session_state.step == 5:
    with st.spinner('🇩🇪 슈나이더 광학 알고리즘이 분석 중입니다...'):
        time.sleep(1.5)

    # --- 분석 로직 (Brain) ---
    age = st.session_state.age
    symptoms = st.session_state.symptoms
    work_dist = st.session_state.work_dist
    digital_hours = st.session_state.digital_hours
    driving = st.session_state.driving
    sensitivity = st.session_state.sensitivity
    fail_check = st.session_state.fail_check
    grade_pref = st.session_state.grade_pref
    current_glasses = st.session_state.current_glasses

    key = ""
    reason = ""
    sub_type = ""
    
    is_presbyopia = age >= 38 and ("작은 글씨 흐림 (스마트폰/서류)" in symptoms)
    is_fatigue = "오후 시간대 눈의 피로/충혈" in symptoms
    is_night_drive = "야간 운전 시 빛 번짐/눈부심" in symptoms or driving == "야간 위주/장거리"
    is_sensitive = sensitivity >= 4 or fail_check
    is_heavy_digital = digital_hours >= 7

    # 로직 적용
    if is_presbyopia:
        # 오피스 렌즈 체크
        if "D. 원거리" not in work_dist and is_heavy_digital and current_glasses != "누진다초점":
            if "A. 손 닿는 거리" in work_dist:
                key = "office_80"
                reason = "서류와 모니터(1m) 집중형. 고개를 들지 않아도 편안한 [오피스 80] 처방"
            elif "B. 팔 뻗은 거리" in work_dist:
                key = "office_150"
                reason = "데스크 업무와 내방 고객 응대(2m) 최적화. [오피스 150] 처방"
            else:
                key = "office_350"
                reason = "회의실 및 실내 이동(4m) 최적화. [오피스 350] 처방"
        # 누진 다초점
        else:
            if "D. 원거리" in work_dist or driving != "거의 안 함":
                lifestyle_type = "Dynamic"
            elif "A. 손 닿는 거리" in work_dist:
                lifestyle_type = "Static"
            else:
                lifestyle_type = "Allround"

            if is_sensitive:
                key = "prog_premium" if lifestyle_type == "Static" else "prog_high"
                reason = "예민한 시각 특성과 과거 불편 이력 고려. 울렁임 제어 기술이 적용된 상위 등급 필수"
            else:
                if "Flagship" in grade_pref: key = "prog_flagship"
                elif "High-End" in grade_pref: key = "prog_high"
                elif "Premium" in grade_pref: key = "prog_premium"
                elif "Standard" in grade_pref: key = "prog_standard"
                else: key = "prog_entry"
                reason = f"라이프스타일 [{lifestyle_type}] 타입과 예산 선호도를 반영한 최적의 매칭"
            sub_type = lifestyle_type

    elif is_fatigue:
        key = "hue_plus"
        reason = "오후 시간대 조절력 부족 케어. [Hue+] 렌즈 추천"

    elif is_night_drive:
        key = "drive_stock"
        reason = "야간 빛 번짐과 눈부심 억제. [슈나이더 드라이브] 추천"

    else:
        if is_heavy_digital:
            key = "bp_stock"
            reason = "디지털 기기 과다 노출. [블루라이트 차단] 소재 렌즈 추천"
        else:
            key = "reins_custom"
            reason = "맑고 선명한 시야를 위한 [개인맞춤 단초점 Reins+] 추천"

    final_lens = lens_catalog.get(key, lens_catalog["prog_standard"])
    add_val = get_estimated_add(age)

    # --- [결과 화면 디자인] (슈나이더 가격표 스타일) ---
    st.balloons()
    
    # 1. 헤더 박스
    st.markdown("""
    <style>
    .result-box {
        border: 2px solid #0055A4; 
        border-radius: 10px; 
        padding: 20px; 
        background-color: #F0F8FF;
        text-align: center;
    }
    .lens-name {
        color: #0055A4;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .price-tag {
        color: #333;
        font-size: 22px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # Native Components로 안전하게 구현
    st.success("✅ 분석이 완료되었습니다.")
    
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align: center; color: #0055A4;'>🏆 {final_lens['name']}</h2>", unsafe_allow_html=True)
        if sub_type:
            st.markdown(f"<p style='text-align: center; font-weight: bold; color: #666;'>Type: {sub_type}</p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"<h3 style='text-align: center;'>시작 가격: {final_lens['price']}</h3>", unsafe_allow_html=True)
        st.info(f"💡 **처방 근거:** {reason}")

    # 2. 상세 데이터
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**👤 고객 프로필**")
            st.write(f"- {st.session_state.gender}, {age}세")
            st.write(f"- 디지털 사용: {digital_hours}시간")
            if is_sensitive:
                st.write("- **⚠️ 예민도 높음**")
    
    with col2:
        with st.container(border=True):
            st.markdown("**👓 전문 소견**")
            st.write(f"- 권장 가입도: **{add_val}**")
            st.write(f"- 분류: {'기능성/오피스' if 'Office' in final_lens['name'] or 'Hue' in final_lens['name'] else '누진 다초점'}")

    if fail_check:
        st.error("⚠️ 과거 실패 이력 있음: 클레임 방지를 위해 적응이 쉬운 상위 등급을 권장합니다.")

    st.markdown("---")
    st.button("🔄 처음부터 다시 하기", on_click=restart)
