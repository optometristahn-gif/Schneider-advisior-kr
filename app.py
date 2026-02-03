import streamlit as st
import time

# ==============================================================================
# 1. [시스템 설정 & 데이터]
# ==============================================================================
st.set_page_config(
    page_title="Schneider AI Advisor",
    page_icon="🇩🇪",
    layout="centered"
)

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1

# 렌즈 데이터베이스 (가격표 기반 특장점 데이터 보강)
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
try:
    st.image("logo.png", width=250)
except:
    st.markdown("## 🇩🇪 Schneider")

st.caption("Professional AI Vision Consulting System Ver 5.0")
st.progress(st.session_state.step * 20)
st.markdown("---")

# ==============================================================================
# 3. [통합 정밀 문진 프로세스]
# ==============================================================================

# [STEP 1] 기본 프로필 (Basic Profile)
if st.session_state.step == 1:
    st.subheader("Step 1. 고객 프로필")
    st.info("정확한 분석을 위해 기본 데이터를 입력해주세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.age = st.number_input("고객 연령", 10, 100, 45)
    with col2:
        st.session_state.gender = st.selectbox("성별", ["남성", "여성"])
    
    st.session_state.history = st.radio(
        "현재 안경 착용 상태",
        ["안경 없음(나안)", "단초점 안경", "기능성(피로완화)", "누진다초점 안경"]
    )
    
    if st.session_state.history == "누진다초점":
        st.session_state.fail_check = st.checkbox("과거 누진 안경 적응에 어려움이 있었습니까?")
    else:
        st.session_state.fail_check = False

    st.button("다음 (Next) 👉", on_click=next_step, type="primary", use_container_width=True)


# [STEP 2] 시각적 불편 정밀 분석 (Symptom Detail)
elif st.session_state.step == 2:
    st.subheader("Step 2. 시각적 불편 정밀 분석")
    st.info("현재 가장 해결하고 싶은 주된 불편함(CC)은 무엇입니까?")
    
    st.session_state.main_cc = st.radio(
        "주된 불편 증상 (1개 선택)",
        ["근거리 흐림 (작은 글씨/폰)", "원거리 흐림 (표지판/TV)", "오후 시간대 눈의 피로/충혈", "야간 운전 시 빛 번짐/눈부심"],
        horizontal=False
    )
    
    st.markdown("##### ➕ 추가 정밀 체크 (Associated Symptoms)")
    st.caption("해당되는 항목을 모두 선택하세요.")
    st.session_state.sub_symptoms = st.multiselect(
        "상세 증상",
        [
            "초점 전환 딜레이 (멀리/가까이 볼 때 늦게 보임)", 
            "대비 감도 저하 (흐린 날/저녁에 유독 침침함)", 
            "야간 시력 저하 (밤이나 비 올 때 잘 안 보임)",
            "광과민 (터널 진출입/밝은 빛에 눈부심)",
            "주변부 울렁임 (고개를 돌릴 때 어지러움)"
        ]
    )
    
    col1, col2 = st.columns(2)
    col1.button("👈 이전", on_click=prev_step, use_container_width=True)
    col2.button("다음 (Next) 👉", on_click=next_step, type="primary", use_container_width=True)


# [STEP 3] 시습관 및 자세 (Visual Behavior)
elif st.session_state.step == 3:
    st.subheader("Step 3. 시습관 및 자세 분석")
    st.info("평소 안경을 착용하고 사물을 보는 습관을 체크합니다.")
    
    st.markdown("**1. 작은 글씨를 볼 때의 자세 (Posture)**")
    st.session_state.posture = st.radio(
        "독서/스마트폰 자세",
        ["자연스러운 자세 유지", "안경을 벗거나 고개를 뒤로 젖힘", "팔을 멀리 뻗거나 당겨서 거리 조절"],
        label_visibility="collapsed"
    )
    
    st.markdown("**2. 이동 중 시각 활동 (Dynamic Vision)**")
    st.session_state.dynamic_vision = st.radio(
        "이동 간 스마트폰 사용",
        ["정적 (멈춰서 확인)", "동적 (걸으면서 자주 확인)"],
        horizontal=True
    )
    
    st.markdown("**3. 운전 시 시선 패턴 (Drive)**")
    st.session_state.drive_pattern = st.radio(
        "운전 습관",
        ["운전 안 함", "전방 주시 위주", "멀티 태스킹 (네비/사이드미러 교차 확인)"],
        horizontal=True
    )

    col1, col2 = st.columns(2)
    col1.button("👈 이전", on_click=prev_step, use_container_width=True)
    col2.button("다음 (Next) 👉", on_click=next_step, type="primary", use_container_width=True)


# [STEP 4] 환경 및 민감도 (Env & Risk)
elif st.session_state.step == 4:
    st.subheader("Step 4. 환경 및 민감도")
    
    st.markdown("**1. 주된 활동 공간 (Indoor/Outdoor)**")
    st.session_state.env_ratio = st.select_slider(
        "실내 vs 실외 비중",
        options=["실내 90% (사무직/가사)", "실내 70%", "밸런스 (50:50)", "실외 70%", "실외 90% (현장/영업)"]
    )
    
    st.markdown("**2. 디지털 기기 사용 비중**")
    st.session_state.digital_intensity = st.radio(
        "하루 디지털 기기 사용량",
        ["Light (3시간 미만)", "Moderate (4~6시간)", "Heavy (7시간 이상)"],
        horizontal=True
    )
    
    st.markdown("**3. 공간 감각 예민도 (Sensitivity)**")
    st.session_state.sensitivity_check = st.multiselect(
        "예민도 체크 (해당 시 선택)",
        ["계단 내려갈 때 바닥이 울렁거림", "고개를 빠르게 돌릴 때 어지러움", "새로운 안경 적응이 느린 편"]
    )
    
    st.markdown("---")
    st.markdown("**4. 선호 렌즈 등급 (Budget)**")
    st.session_state.grade_pref = st.selectbox(
        "추천 렌즈 등급",
        ["Flagship (최고 사양)", "High-End (고성능)", "Premium (안정성)", "Standard (가성비)", "Entry (입문)"],
        index=2
    )

    col1, col2 = st.columns(2)
    col1.button("👈 이전", on_click=prev_step, use_container_width=True)
    col2.button("🔍 AI 정밀 분석 실행", on_click=next_step, type="primary", use_container_width=True)


# [STEP 5] 최종 결과 리포트 (Result)
elif st.session_state.step == 5:
    with st.spinner('🇩🇪 Schneider Optical Brain 분석 중...'):
        time.sleep(2)

    # --- [Brain] 분석 알고리즘 ---
    # 변수 로드
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
    fail_check = st.session_state.fail_check

    # 로직 변수
    key = ""
    why_text = ""
    sub_type = ""
    is_sensitive = len(sens_list) > 0 or fail_check or st.session_state.sensitivity_check
    
    # 1. 노안(Presbyopia) 로직
    if (age >= 38 and "근거리" in main_cc) or (age >= 45):
        # 오피스 렌즈 우선 체크 (실내 비중 높음 + 누진 아님 + 운전 안 함)
        if "실내" in env and history != "누진다초점" and drive == "운전 안 함":
            if "자세" in posture or "팔을" in posture: # 거리 조절 습관 -> 오피스 강력 추천
                if "Light" not in digital: # 디지털 사용 많음
                    key = "office_150"
                    why_text = "데스크 업무와 실내 생활 비중이 높습니다. 누진보다 넓은 중근거리 시야를 제공하는 오피스 렌즈가 업무 효율을 극대화합니다."
            
        # 오피스가 아니면 누진 로직
        if key == "":
            # 타입 결정
            if "실외" in env or "동적" in dynamic or "멀티" in drive:
                lifestyle_type = "Dynamic"
                why_text = "활동적인 라이프스타일과 잦은 시선 이동을 고려하여, 원거리 시야가 넓고 울렁임이 적은 설계를 채택했습니다."
            elif "실내 90%" in env:
                lifestyle_type = "Static"
                why_text = "근거리 집중도가 높은 환경입니다. 스마트폰과 독서 영역이 강화된 정밀 근용 설계를 채택했습니다."
            else:
                lifestyle_type = "Allround"
                why_text = "실내외 활동의 밸런스가 중요합니다. 모든 거리에서 균형 잡힌 시야를 제공하는 표준 설계를 채택했습니다."

            # 등급 결정 (예민도/이력 반영)
            if is_sensitive or "초점 전환 딜레이" in sub_symptoms or "주변부 울렁임" in sub_symptoms:
                key = "prog_premium" if lifestyle_type == "Static" else "prog_high"
                why_text += " 특히 예민한 시각 특성과 주변부 울렁임을 제어하기 위해 상위 등급의 **[Swim Effect Control]** 기술이 필수적입니다."
            else:
                # 선호 등급
                if "Flagship" in grade_pref: key = "prog_flagship"
                elif "High-End" in grade_pref: key = "prog_high"
                elif "Premium" in grade_pref: key = "prog_premium"
                elif "Standard" in grade_pref: key = "prog_standard"
                else: key = "prog_entry"
                why_text += f" 고객님의 예산 선호도와 필요 성능을 고려하여 최적의 가성비를 갖춘 모델을 매칭했습니다."
            
            sub_type = lifestyle_type

    # 2. 피로(Fatigue) 로직
    elif "피로" in main_cc:
        key = "hue_plus"
        why_text = "오후 시간대의 눈 피로는 '조절력 부족' 신호입니다. 8가지 정밀 타입으로 눈의 힘을 덜어주는 기능성 렌즈가 필요합니다."

    # 3. 야간(Drive) 로직
    elif "야간" in main_cc or "야간 시력 저하" in sub_symptoms or "광과민" in sub_symptoms:
        key = "drive_stock"
        why_text = "야간 운전 시 대향차 라이트 눈부심과 대비감도 저하를 호소하셨습니다. 특수 코팅으로 빛 번짐을 억제해야 합니다."

    # 4. 기타/디지털
    else:
        if "Heavy" in digital:
            key = "bp_stock"
            why_text = "디지털 기기 노출이 매우 많습니다. 일반 렌즈보다 강력한 블루라이트 차단 소재(Blue Protect)가 시력 보호에 필수입니다."
        else:
            key = "reins_custom"
            why_text = "주변부 왜곡이나 흐림 없이, 가장 맑고 깨끗한 해상도를 원하신다면 개인맞춤 단초점 렌즈가 정답입니다."

    # 최종 매핑
    final_lens = lens_catalog.get(key, lens_catalog["prog_standard"])
    add_val = get_estimated_add(age)

    # --- [결과 화면 출력] ---
    st.balloons()
    
    st.markdown("""
    <style>
    .result-container {
        border: 2px solid #004B87;
        background-color: #F8FBFF;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .feature-box {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
        text-align: left;
        border-left: 5px solid #004B87;
    }
    </style>
    """, unsafe_allow_html=True)

    st.success("✅ AI 정밀 분석이 완료되었습니다.")

    # 1. 메인 결과 카드
    with st.container():
        st.markdown(f"""
        <div class="result-container">
            <h4 style="color: #666; margin: 0;">Final Recommendation</h4>
            <h2 style="color: #004B87; font-size: 28px; margin: 10px 0;">🏆 {final_lens['name']}</h2>
            <p style="font-size: 20px; font-weight: bold; color: #333;">가격: {final_lens['price']}</p>
        </div>
        """, unsafe_allow_html=True)

    # 2. Why & Features (상세 설명)
    st.markdown("### 📊 분석 리포트")
    
    with st.expander("💡 왜 이 렌즈를 추천했나요? (Why)", expanded=True):
        st.info(why_text)
        if sub_type:
             st.markdown(f"**적용 설계:** :blue[{sub_type} Type] (라이프스타일 반영)")

    with st.expander("🛠️ 핵심 기술 (Key Features)", expanded=True):
        for feat in final_lens['features']:
            st.markdown(f"- ✅ **{feat}**")

    # 3. 임상 데이터 (Clinical Data)
    st.markdown("### 👓 Clinical Data")
    col1, col2 = st.columns(2)
    with col1:
        st.caption("고객 프로필")
        st.write(f"- 연령: {age}세")
        st.write(f"- 디지털 사용: {digital}")
        if is_sensitive: st.write("- **⚠️ 예민도 높음**")
    
    with col2:
        st.caption("전문가 소견")
        st.write(f"- 권장 가입도: **{add_val}**")
        st.write(f"- 렌즈 분류: {'기능성/오피스' if 'Office' in final_lens['name'] or 'Hue' in final_lens['name'] else '누진 다초점'}")

    st.markdown("---")
    st.button("🔄 새로운 고객 상담하기", on_click=restart)
