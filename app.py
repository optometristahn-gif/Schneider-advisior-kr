import streamlit as st
import time

# ==============================================================================
# 1. [슈나이더 S-90 마스터 DB] (가격표 100% 일치)
# ==============================================================================
lens_catalog = {
    # [누진] 등급별
    "prog_flagship": {"name": "S-90 Starlight Lifestyle +", "price": "₩800,000~", "desc": "라이프스타일 3Type(Static/Allround/Dynamic) 개인맞춤"},
    "prog_high":     {"name": "S-90 Starlight +", "price": "₩650,000~", "desc": "슈나이더 기술력의 정점, 시그니처 모델"},
    "prog_premium":  {"name": "S-90 Platinum +", "price": "₩520,000~", "desc": "어지러움에 예민한 분들을 위한 넓은 시야 (마스터피스)"},
    "prog_standard": {"name": "S-90 Gold +", "price": "₩360,000~", "desc": "실패 없는 베스트셀러, 가격/성능 밸런스 최상"},
    "prog_entry":    {"name": "S-90 Pro +", "price": "₩270,000~", "desc": "합리적인 가격의 입문용 누진 렌즈"},

    # [기능성]
    "hue_plus":      {"name": "S-90 Hue +", "price": "₩360,000~", "desc": "8가지 타입 조절력 케어 (피로완화)"},
    "office_350":    {"name": "S-90 Office 350+ (4m)", "price": "₩470,000~", "desc": "회의실 및 실내 이동이 잦은 분 (4m)"},
    "office_150":    {"name": "S-90 Office 150+ (2m)", "price": "₩470,000~", "desc": "데스크 업무와 고객 응대 (2m)"},
    "office_80":     {"name": "S-90 Office 80+ (1m)", "price": "₩360,000~", "desc": "PC와 독서 집중형 (1m)"},

    # [단초점/여벌]
    "drive_stock":   {"name": "Schneider Drive (여벌)", "price": "₩300,000", "desc": "야간 빛 번짐 차단 (즉시 가공 가능)"},
    "bp_stock":      {"name": "Schneider BP 174 (여벌)", "price": "₩380,000", "desc": "1.74 초고굴절 + 블루라이트 소재 차단"},
    "reins_custom":  {"name": "S-90 Reins + (개인맞춤)", "price": "₩300,000~", "desc": "주변부 왜곡을 줄인 스마트 고해상도 단초점"}
}

# ==============================================================================
# 2. [함수] 가입도 예측
# ==============================================================================
def get_estimated_add(age):
    if age < 38: return "가입도 불필요 (조절력 충분)"
    elif age < 42: return "+0.75 D ~ +1.00 D (초기)"
    elif age < 45: return "+1.00 D ~ +1.25 D"
    elif age < 48: return "+1.50 D ~ +1.75 D"
    elif age < 52: return "+1.75 D ~ +2.00 D"
    elif age < 56: return "+2.00 D ~ +2.25 D"
    elif age < 60: return "+2.25 D ~ +2.50 D"
    else: return "+2.50 D (Max)"

# ==============================================================================
# 3. [웹사이트 UI 구성]
# ==============================================================================
st.set_page_config(page_title="Schneider AI Advisor", page_icon="🇩🇪")

# 헤더
st.title("🇩🇪 Schneider AI Vision Advisor")
st.caption("독일 슈나이더 S-90 정밀 광학 시스템 기반 컨설팅")
st.divider()

# --- 문진 섹션 (Sidebar 대신 메인 화면 활용) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 기본 정보")
    age = st.number_input("고객님 연령", min_value=10, max_value=100, value=45, step=1)
    
    # Q2. 현재 안경
    cur_glasses_opt = st.radio(
        "현재 착용 중인 안경",
        ("안경 경험 없음 / 일반 단초점", "기능성 / 피로완화 렌즈", "누진다초점 렌즈")
    )
    
    # 꼬리 질문 로직
    needs_upgrade = False
    fail_history = False
    
    if cur_glasses_opt == "기능성 / 피로완화 렌즈":
        if st.radio("현재 만족도", ("만족함", "가까운 게 덜 보임")) == "가까운 게 덜 보임":
            needs_upgrade = True
    elif cur_glasses_opt == "누진다초점 렌즈":
        if st.radio("적응 여부", ("잘 적응함", "실패 / 불편했음")) == "실패 / 불편했음":
            fail_history = True

with col2:
    st.subheader("2. 시각적 불편")
    # Q3. 불편 사항 (코드 매핑을 위해 인덱스 활용하거나 텍스트 매칭)
    symptom_opt = st.radio(
        "가장 큰 불편함",
        (
            "핸드폰, 서류 등 작은 글씨가 흐림 (노안)",
            "오후만 되면 눈이 뻑뻑하고 침침함 (피로)",
            "밤운전 시 빛 번짐이 심함 (야간)",
            "특별한 불편 없으나 더 선명하길 원함 (선명도)"
        )
    )

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("3. 라이프스타일")
    # Q4. 주시 거리
    lifestyle_opt = st.radio(
        "주된 시생활 거리",
        (
            "30~40cm (스마트폰, 독서 위주)",
            "60cm~2m (모니터, 회의, 요리)",
            "5m 이상 (운전, 야외 활동)"
        )
    )
    
    # Q5. 디지털 사용
    digital_opt = st.radio(
        "PC/스마트폰 사용 시간",
        ("8시간 이상 (Heavy)", "4시간 정도 (Average)", "거의 안 함 (Light)")
    )

with col4:
    st.subheader("4. 선호도")
    # Q6. 예민도
    sens_opt = st.radio(
        "평소 예민도",
        ("매우 예민함", "보통", "무던함")
    )
    
    # Q7. 등급 선호
    grade_opt = st.selectbox(
        "렌즈 선택 기준 (등급)",
        (
            "Flagship (최상위 기술력)",
            "High-End (고성능 시그니처)",
            "Premium (어지러움 감소)",
            "Standard (베스트셀러)",
            "Entry (가성비 입문)"
        )
    )

# ==============================================================================
# 4. [분석 버튼 및 로직]
# ==============================================================================
st.divider()
analyze_btn = st.button("🔍 AI 정밀 분석 시작", use_container_width=True, type="primary")

if analyze_btn:
    with st.spinner('독일 슈나이더 광학 알고리즘이 분석 중입니다...'):
        time.sleep(1.2) # 연출용 딜레이

        # --- 로직 변수 매핑 ---
        # 텍스트 입력을 로직 코드로 변환
        lifestyle_code = "2" # 기본 Allround
        if "30~40cm" in lifestyle_opt: lifestyle_code = "1"
        elif "5m" in lifestyle_opt: lifestyle_code = "3"
        
        lifestyle_map = {"1": "Static", "2": "Allround", "3": "Dynamic"}
        lifestyle_str = lifestyle_map[lifestyle_code]

        symptom_code = "4"
        if "노안" in symptom_opt: symptom_code = "1"
        elif "피로" in symptom_opt: symptom_code = "2"
        elif "야간" in symptom_opt: symptom_code = "3"
        
        digital_heavy = "8시간" in digital_opt
        
        sensitivity_high = "매우 예민함" in sens_opt

        # --- 추천 로직 (Brain) ---
        key = ""
        reason = ""
        add_recommendation = get_estimated_add(age)

        force_premium = fail_history or sensitivity_high

        # Case A: 노안
        if age >= 40 and symptom_code == "1":
            # 1. 오피스 특례 (누진 경험 X + 근거리 위주)
            if lifestyle_code == "1" and "누진" not in cur_glasses_opt:
                key = "office_80"
                reason = "이동보다 앉아서 하는 업무가 압도적입니다. 누진보다 시야가 넓고 고개가 편한 '오피스 80+'를 추천합니다."
            
            # 2. 오피스 (디지털 헤비 + Static/Allround) - 정밀 질문 로직 간소화
            elif digital_heavy and lifestyle_code != "3" and "누진" not in cur_glasses_opt:
                key = "office_150" # 기본값
                reason = "실내 업무량이 많으십니다. '오피스 렌즈'로 업무 효율을 높여보세요."

            # 3. 누진 다초점
            else:
                if force_premium:
                    if lifestyle_code == "1":
                        key = "prog_premium"
                        reason = "예민하시거나 실패 이력이 있으시군요. 울렁임을 억제하고 적응이 쉬운 '플래티넘+' 이상을 권장합니다."
                    else:
                        key = "prog_high"
                        reason = "예민하신 눈에는 슈나이더의 시그니처 '스타라이트+'가 필요합니다. 실패 없는 완벽한 시야를 제공합니다."
                else:
                    # 등급 선택 반영
                    if "Flagship" in grade_opt: key = "prog_flagship"
                    elif "High-End" in grade_opt: key = "prog_high"
                    elif "Premium" in grade_opt: key = "prog_premium"
                    elif "Standard" in grade_opt: key = "prog_standard"
                    else: key = "prog_entry" # Entry

                    # 추천 이유 생성
                    if key == "prog_flagship": reason = f"고객님의 라이프스타일({lifestyle_str})에 1:1로 맞춘 최상위 렌즈입니다."
                    elif key == "prog_high": reason = "슈나이더 기술력의 정점, 시그니처 모델입니다."
                    elif key == "prog_premium": reason = "넓은 시야와 적은 어지러움을 제공하는 마스터피스입니다."
                    elif key == "prog_standard": reason = "가장 많이 선택하시는 실패 없는 베스트셀러입니다."
                    else: reason = "부담 없이 시작할 수 있는 합리적인 누진 렌즈입니다."

        # Case B: 피로
        elif symptom_code == "2":
            key = "hue_plus"
            reason = "오후의 눈 피로는 조절력 부족 때문입니다. 8가지 타입 중 최적의 도수를 찾아 눈의 힘을 덜어주는 'Hue+'를 처방합니다."

        # Case C: 야간
        elif symptom_code == "3":
            key = "drive_stock"
            reason = "야간 운전의 주적인 빛 번짐을 잡는 '슈나이더 드라이브(여벌)' 렌즈입니다."

        # Case D: 기타
        else:
            if symptom_code == "4" and digital_heavy:
                key = "bp_stock"
                reason = "가장 얇은 1.74 굴절률에 블루라이트 차단(Blau Protect) 소재가 적용된 렌즈입니다."
            else:
                key = "reins_custom"
                reason = "주변부 왜곡 없이 맑고 깨끗한 시야를 원하신다면 개인맞춤 단초점 'Reins+'가 정답입니다."

        # 결과 매핑
        final_lens = lens_catalog.get(key, lens_catalog["prog_standard"])

        # --- 결과 화면 출력 (Report UI) ---
        st.success("분석이 완료되었습니다!")
        
        # 카드 형태로 결과 보여주기
        with st.container():
            st.markdown(f"### 🏆 최종 처방: **{final_lens['name']}**")
            st.markdown(f"**💰 가격:** {final_lens['price']}")
            st.info(f"💡 **진단 소견:** {reason}")
            
            if "Lifestyle" in final_lens['name']:
                 st.caption(f"📍 권장 설계 타입: **{lifestyle_str} Type**")

            st.divider()
            st.markdown("#### 👓 Clinical Note (전문가용)")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("고객 연령", f"{age}세")
            col_b.metric("라이프스타일", lifestyle_str)
            col_c.metric("권장 가입도(ADD)", add_recommendation.split(" ")[0]) # 앞부분만 표시
            
            if fail_history:
                st.error("⚠️ 주의: 과거 누진 실패 이력 있음 (High-End급 권장)")
                