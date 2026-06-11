import streamlit as st

# --- 1. 기존 코드의 초기 데이터 구조 유지 ---
# 스트림릿의 재실행 특성 때문에, 데이터가 초기화되지 않도록 세션 상태에 저장합니다.
if "주차구역" not in st.session_state:
    st.session_state["주차구역"] = ["A구역", "B구역", "C구역"]
if "주차완료_기록" not in st.session_state:
    st.session_state["주차완료_기록"] = []
if "프로그램_종료" not in st.session_state:
    st.session_state["프로그램_종료"] = False

# 사용하기 편하게 기존 변수명으로 연결
주차구역 = st.session_state["주차구역"]
주차완료_기록 = st.session_state["주차완료_기록"]


# --- 2. 스트림릿 UI 구성 ---
st.title("🚗 주차 보조 프로그램")
st.markdown("---")

# 프로그램 종료 상태 처리
if st.session_state["프로그램_종료"]:
    st.error("프로그램이 종료되었습니다. 다시 시작하려면 새로고침(F5)을 눌러주세요.")
    
    # 최종 결과 출력
    st.subheader("----- 최종 주차 현황 -----")
    st.write(f"**남은 주차 구역:** {주차구역}")
    st.write(f"**주차 완료 기록:** {주차완료_기록}")
else:
    # 기존 콘솔의 input()을 스트림릿의 number_input과 버튼으로 대체
    거리 = st.number_input(
        "후방 센서 거리(cm)를 입력해주세요. (0: 완료, 999: 종료)", 
        min_value=0, 
        max_value=999, 
        value=100,
        step=1
    )
    
    # 전송 버튼 (기존 콘솔에서 엔터를 치는 행위와 동일)
    if st.button("센서 값 전송"):
        st.markdown("### 📢 시스템 안내")
        
        # --- 3. 원래 작성하신 조건문 로직 (순서 및 문법 오류 수정 적용) ---
        if 거리 == 999:
            st.warning("프로그램을 종료합니다")
            st.session_state["프로그램_종료"] = True
            st.rerun() # 화면을 즉시 새로고침하여 종료 상태 반영
            
        elif 거리 == 0:
            if len(주차구역) > 0:
                구역 = 주차구역.pop(0)
                주차완료_기록.append(구역) # 기존 코드의 문법 오류 수정 (.append -> .append(구역))
                st.success(f"주차가 완료되었습니다! 배정된 구역: **{구역}**")
            else:
                st.error("더 이상 주차할 수 있는 빈 구역이 없습니다.")
                
        # 기존 로직에서 '위험'이 먼저 체크되도록 순서 보정
        elif 거리 <= 30:
            st.error("[위험] 즉시 정지하세요!")
            
        elif 거리 <= 100:
            st.info("[조심] 속도를 줄이세요!")
            
        elif 거리 > 100:
            st.info("뒤로 더 후진하세요.")
            
        # 세션 상태 갱신
        st.session_state["주차구역"] = 주차구역
        st.session_state["주차완료_기록"] = 주차완료_기록

    # 실시간 주차 구역 현황판
    st.markdown("---")
    st.subheader("----- 실시간 주차 구역 -----")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="남은 주차 구역 수", value=len(주차구역))
        st.json(주차구역)
    with col2:
        st.metric(label="주차 완료 차량 수", value=len(주차완료_기록))
        st.json(주차완료_기록)
