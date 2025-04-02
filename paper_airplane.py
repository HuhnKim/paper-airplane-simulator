import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import io
from matplotlib.animation import PillowWriter
import tempfile
import time

st.set_page_config(page_title="Paper Airplane Simulator", layout="centered")

# 인자 수준 정의
wing_options = ['Short', 'Medium', 'Long']
body_options = ['Short', 'Medium', 'Long']
shape_options = ['Delta', 'Standard', 'Arrow']
material_options = ['Recycled', 'Regular', 'Glossy']
humidity_options = ['Dry', 'Normal', 'Humid']

# 최적 조건 설정 (비행거리 증가 조건)
optimal_condition = {
    'WingLength': 'Long',
    'BodyLength': 'Medium',
    'Shape': 'Delta',
    'Material': 'Glossy',
    'Humidity': 'Normal'
}

# 거리 시뮬레이션 함수 (바람 효과 포함)
def simulate_distance(wing, body, shape, material, humidity):
    base_distance = 5
    if wing == optimal_condition['WingLength']:
        base_distance += 5
    if body == optimal_condition['BodyLength']:
        base_distance += 4
    if shape == optimal_condition['Shape']:
        base_distance += 5
    if material == optimal_condition['Material']:
        base_distance += 3
    if humidity == optimal_condition['Humidity']:
        base_distance += 2
    wind_effect = random.uniform(-2, 2)
    noise = np.random.normal(0, 1.5)
    return base_distance + wind_effect + noise

# 색상 및 마커 설정
wing_color = {'Short': 'blue', 'Medium': 'green', 'Long': 'red'}
body_size = {'Short': 5, 'Medium': 8, 'Long': 11}
shape_marker = {'Delta': '^', 'Standard': 's', 'Arrow': '>'}

# Streamlit UI
st.title("🛩️ Paper Airplane Flight Simulator")
st.markdown("""
선택한 조건에 따라 종이비행기의 비행을 시뮬레이션하고, 날아간 거리를 확인하세요. 

- **Wing Length**: 날개의 길이
- **Body Length**: 몸통 길이
- **Shape**: 기체 모양
- **Material**: 종이 재질
- **Humidity: 실내 공기의 습도
- 비행에는 무작위 **바람 효과**가 포함됩니다.
""")

wing = st.radio("날개 길이", wing_options, horizontal=True)
body = st.radio("몸통 길이", body_options, horizontal=True)
shape = st.radio("모양", shape_options, horizontal=True)
material = st.radio("재질", material_options, horizontal=True)
humidity = st.radio("습도", humidity_options, horizontal=True)

if st.button("비행 시작!"):
    distance = simulate_distance(wing, body, shape, material, humidity)

    st.success("비행기 이륙! 아래에서 비행 모습을 확인하세요.")

    # matplotlib 애니메이션 설정
    fig, ax = plt.subplots()
    ax.set_xlim(0, 20)
    ax.set_ylim(-1, 1)
    ax.set_title("Flight Animation")
    ax.set_xlabel("Distance (m)")
    ax.get_yaxis().set_visible(False)

    point, = ax.plot([], [], marker=shape_marker[shape], color=wing_color[wing], markersize=body_size[body]*1.5)

    def init():
        point.set_data([], [])
        return point,

    def animate(frame):
        d = (distance / 50) * frame
        x = [min(d, distance)]
        y = [np.sin(frame / 10) * 0.5]
        point.set_data(x, y)
        return point,

    ani = animation.FuncAnimation(fig, animate, frames=50, init_func=init, blit=True, interval=100, repeat=False)

    fig.tight_layout()

    # 임시 파일로 GIF 저장 후 읽기
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmpfile:
        writer = PillowWriter(fps=10)
        ani.save(filename=tmpfile.name, writer=writer)
        tmpfile.seek(0)
        gif_bytes = tmpfile.read()

    st.image(gif_bytes, caption=f"최종 비행 거리: {distance:.2f} m", use_container_width=True)

st.markdown("""
---
Made with ❤️ using Streamlit and Matplotlib
""")
