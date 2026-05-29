import streamlit as st

# 1. 초기 데이터 설정 (재고 및 가격)
if 'inventory' not in st.session_state:
    st.session_state.inventory = {
        "콜라": {"price": 1500, "stock": 5},
        "사이다": {"price": 1200, "stock": 3},
        "생수": {"price": 800, "stock": 10},
        "커피": {"price": 2000, "stock": 2}
    }

if 'balance' not in st.session_state:
    st.session_state.balance = 0

# 앱 타이틀
st.title("🤖 AI 스마트 자판기")
st.markdown("---")

# 2. 사이드바 - 돈 투입
with st.sidebar:
    st.header("💰 금액 투입")
    money_input = st.number_input("금액을 입력하세요 (원)", min_value=0, step=100)
    if st.button("돈 넣기"):
        st.session_state.balance += money_input
        st.success(f"{money_input}원이 투입되었습니다!")

    st.metric("현재 잔액", f"{st.session_state.balance}원")
    
    if st.button("잔액 반환"):
        change = st.session_state.balance
        st.session_state.balance = 0
        st.warning(f"잔액 {change}원이 반환되었습니다.")

# 3. 메인 화면 - 상품 목록 전시
st.subheader("🛒 판매 중인 상품")
cols = st.columns(len(st.session_state.inventory))

for i, (item, info) in enumerate(st.session_state.inventory.items()):
    with cols[i]:
        st.write(f"**{item}**")
        st.write(f"💰 {info['price']}원")
        st.write(f"📦 재고: {info['stock']}개")
        
        # 구매 버튼 logic
        if st.button(f"{item} 구매", key=item):
            if info['stock'] <= 0:
                st.error("품절되었습니다!")
            elif st.session_state.balance < info['price']:
                st.error("잔액이 부족합니다!")
            else:
                # 처리
                st.session_state.balance -= info['price']
                st.session_state.inventory[item]['stock'] -= 1
                st.balloons()
                st.success(f"{item} 구매 완료!")

# 4. 하단 상태 표시
st.divider()
st.info(f"현재 이용 가능한 잔액은 **{st.session_state.balance}원** 입니다.")