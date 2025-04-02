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
st.markdown("<h2 style='text-align: center;'>🛩️ Paper Airplane Flight Simulator</h2>", unsafe_allow_html=True)
st.markdown("""
선택한 조건에 따라 종이비행기의 비행을 시뮬레이션하고, 날아간 거리를 확인하세요. 
비행 시 무작위로 바람이 영향을 미칩니다.
""")

# wing = st.radio("날개 길이", wing_options, horizontal=True, key="wing")
# body = st.radio("몸통 길이", body_options, horizontal=True, key="body")
# shape = st.radio("기체 모양", shape_options, horizontal=True, key="shape")
# material = st.radio("종이 재질", material_options, horizontal=True, key="material")
# humidity = st.radio("습도", humidity_options, horizontal=True, key="humidity")

col1, col2 = st.columns([2, 9])
with col1:
    st.markdown("<div style='text-align:center'><strong>날개 길이</strong></div>", unsafe_allow_html=True)
with col2:
    wing = st.radio(" ", wing_options, horizontal=True, key="wing", label_visibility="collapsed")
col1, col2 = st.columns([2, 9])
with col1:
    st.markdown("<div style='text-align:center'><strong>몸통 길이</strong></div>", unsafe_allow_html=True)
with col2:
    body = st.radio(" ", body_options, horizontal=True, key="body", label_visibility="collapsed")
col1, col2 = st.columns([2, 9])
with col1:
    st.markdown("<div style='text-align:center'><strong>모양</strong></div>", unsafe_allow_html=True)
with col2:
    shape = st.radio(" ", shape_options, horizontal=True, key="shape", label_visibility="collapsed")
col1, col2 = st.columns([2, 9])
with col1:
    st.markdown("<div style='text-align:center'><strong>재질</strong></div>", unsafe_allow_html=True)
with col2:
    material = st.radio(" ", material_options, horizontal=True, key="material", label_visibility="collapsed")
col1, col2 = st.columns([2, 9])
with col1:
    st.markdown("<div style='text-align:center'><strong>습도</strong></div>", unsafe_allow_html=True)
with col2:
    humidity = st.radio(" ", humidity_options, horizontal=True, key="humidity", label_visibility="collapsed")

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
        writer = PillowWriter(fps=20)
        ani.save(filename=tmpfile.name, writer=writer)
        tmpfile.seek(0)
        gif_bytes = tmpfile.read()

    st.markdown(f"<h2 style='text-align: center; color: darkblue;'>✈️ 최종 비행 거리: {distance:.2f} m</h2>", unsafe_allow_html=True)
    st.image(gif_bytes, use_container_width=True)

st.markdown("""
---
Made with ❤️ using Streamlit and Matplotlib
""")
