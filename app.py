
import streamlit as st
import random
import time

st.set_page_config(
    page_title="폐가 : 마지막 방문자",
    page_icon="👻",
    layout="centered"
)

# -------------------------
# 게임 초기 설정
# -------------------------

def init_game():
    st.session_state.started = True
    st.session_state.location = "현관"
    st.session_state.sanity = 100
    st.session_state.battery = 100
    st.session_state.inventory = []
    st.session_state.visited = []
    st.session_state.message = "낡은 철문이 천천히 열린다..."
    st.session_state.ended = False
    st.session_state.turn = 0

if "started" not in st.session_state:
    st.session_state.started = False

if "ended" not in st.session_state:
    st.session_state.ended = False

# -------------------------
# 장소 데이터
# -------------------------

rooms = {
    "현관": {
        "description": "축축한 냄새가 코를 찌른다. 깨진 거울 너머로 무언가 움직인 것 같다.",
        "items": ["손전등"],
        "doors": ["거실", "부엌"]
    },
    "거실": {
        "description": "오래된 텔레비전이 혼자 켜져 있다. 화면에는 당신의 뒷모습이 비친다.",
        "items": ["낡은 사진"],
        "doors": ["현관", "안방", "지하실"]
    },
    "부엌": {
        "description": "싱크대에 검붉은 얼룩이 남아 있다. 서랍 안에서 열쇠가 보인다.",
        "items": ["지하실 열쇠"],
        "doors": ["현관"]
    },
    "안방": {
        "description": "침대 위에 누군가 앉아 있다. 하지만 눈을 깜빡이자 사라졌다.",
        "items": ["녹음기"],
        "doors": ["거실", "다락방"]
    },
    "지하실": {
        "description": "벽에는 수많은 이름이 적혀 있다. 그중 마지막 이름은 당신의 이름이다.",
        "items": ["일기장"],
        "doors": ["거실"]
    },
    "다락방": {
        "description": "창문이 바람도 없이 흔들린다. 구석에 낡은 상자가 놓여 있다.",
        "items": ["마지막 편지"],
        "doors": ["안방"]
    }
}

# -------------------------
# 공포 이벤트
# -------------------------

events = [
    ("등 뒤에서 발소리가 들린다...", 10),
    ("누군가 귓가에 속삭인다. '돌아가...'", 15),
    ("벽에 걸린 사진 속 사람이 웃고 있다.", 10),
    ("갑자기 손전등이 깜빡인다!", 5),
    ("복도 끝에 검은 형체가 서 있다!", 20)
]

def horror_event():
    if random.random() < 0.35:
        message, damage = random.choice(events)
        st.session_state.sanity -= damage
        st.session_state.message = message

    if st.session_state.sanity <= 0:
        st.session_state.sanity = 0
        st.session_state.ended = True

# -------------------------
# 아이템 수집
# -------------------------

def collect_item():
    room = st.session_state.location
    items = rooms[room]["items"]

    for item in items:
        if item not in st.session_state.inventory:
            st.session_state.inventory.append(item)
            st.session_state.message = f"🎒 {item} 획득!"

# -------------------------
# 이동
# -------------------------

def move_room(room):
    if room == "지하실" and "지하실 열쇠" not in st.session_state.inventory:
        st.session_state.message = "🔒 문이 잠겨 있다. 열쇠가 필요하다."
        return

    st.session_state.location = room
    st.session_state.turn += 1
    st.session_state.visited.append(room)
    st.session_state.battery = max(
        0, st.session_state.battery - 8
    )

    st.session_state.message = rooms[room]["description"]
    collect_item()
    horror_event()

# -------------------------
# 화면
# -------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #080808, #191111);
    color: #eeeeee;
}
h1, h2, h3 {
    color: #c62828 !important;
}
div.stButton > button {
    background-color: #390d0d;
    color: white;
    border: 1px solid #8b2525;
    border-radius: 8px;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #8b1717;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("👻 폐가 : 마지막 방문자")
st.caption("당신은 절대 들어가서는 안 될 집에 들어왔다.")

if not st.session_state.started:
    st.image(
        "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200",
        caption="오래전 버려진 집"
    )

    st.warning(
        "10년 전, 이 집에 살던 일가족이 흔적도 없이 사라졌다."
    )

    if st.button("🚪 흉가 탐방 시작"):
        init_game()
        st.rerun()

else:
    if st.session_state.ended:
        st.error("GAME OVER")

        st.title("당신은 흉가에서 사라졌다.")
        st.write("마지막으로 들린 목소리는 당신 자신의 목소리였다.")

        if st.button("🔄 다시 시작"):
            init_game()
            st.rerun()

    else:
        # 상태 표시
        st.subheader("📊 생존 상태")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("🧠 정신력", f"{st.session_state.sanity}%")
            st.progress(st.session_state.sanity / 100)

        with col2:
            st.metric("🔦 배터리", f"{st.session_state.battery}%")
            st.progress(st.session_state.battery / 100)

        st.divider()

        # 현재 위치
        st.subheader(f"📍 현재 위치 : {st.session_state.location}")

        st.write(rooms[st.session_state.location]["description"])

        st.warning(st.session_state.message)

        # 인벤토리
        st.subheader("🎒 소지품")
        if st.session_state.inventory:
            st.write(" / ".join(st.session_state.inventory))
        else:
            st.write("아직 획득한 아이템이 없습니다.")

        st.divider()

        # 탐험
        st.subheader("🚶 이동하기")

        available_rooms = rooms[st.session_state.location]["doors"]

        for room in available_rooms:
            if st.button(f"➡️ {room}으로 이동"):
                move_room(room)
                st.rerun()

        # 특별 행동
        st.subheader("🔍 행동하기")

        if st.button("👀 주변 자세히 살펴보기"):
            st.session_state.sanity -= 5
            st.session_state.turn += 1

            if random.random() < 0.5:
                st.session_state.message = "벽 뒤에서 누군가 당신을 지켜보고 있다."
            else:
                st.session_state.message = "바닥에서 오래된 발자국을 발견했다."

            if st.session_state.sanity <= 0:
                st.session_state.sanity = 0
                st.session_state.ended = True

            st.rerun()

        if st.button("🔦 손전등 배터리 절약"):
            st.session_state.battery = max(
                0, st.session_state.battery - 3
            )
            st.session_state.message = "손전등의 빛이 희미해진다."
            st.rerun()

        if st.button("🏃 현관으로 도망치기"):
            if st.session_state.location == "현관":
                st.success("당신은 간신히 집을 빠져나왔다!")
                st.session_state.ended = True
                st.session_state.message = "탈출 엔딩"
            else:
                st.session_state.sanity -= 10
                st.session_state.message = "문을 찾지 못했다. 무언가 다가온다."

                if st.session_state.sanity <= 0:
                    st.session_state.sanity = 0
                    st.session_state.ended = True

            st.rerun()

        st.divider()

        st.caption(
            f"탐험 횟수: {st.session_state.turn}회"
        )
