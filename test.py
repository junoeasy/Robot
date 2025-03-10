import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

# 📌 3D 플롯 생성
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# 📌 고정된 점 A (회전의 중심)
A_x, A_y, A_z = 0, 0, 0  # A는 고정

# 📌 이동할 두 점 B & C (초기 위치)
B_x, B_y, B_z = 0, 1, 0  # B의 초기 위치
C_x, C_y, C_z = 0, 1, 1  # C의 초기 위치
BC_length = 1  # 📌 BC 거리는 고정

# 📌 점과 선 초기화
A_point, = ax.plot([A_x], [A_y], [A_z], 'ro', markersize=8)  # 고정된 점 A
B_point, = ax.plot([B_x], [B_y], [B_z], 'bo', markersize=8)  # 이동하는 점 B
C_point, = ax.plot([C_x], [C_y], [C_z], 'go', markersize=8)  # 이동하는 점 C
line_AB, = ax.plot([A_x, B_x], [A_y, B_y], [A_z, B_z], 'k-', linewidth=2)  # A → B 연결선
line_BC, = ax.plot([B_x, C_x], [B_y, C_y], [B_z, C_z], 'k-', linewidth=2)  # B → C 연결선

# 📌 좌표 및 거리 표시
text_A = ax.text(A_x, A_y, A_z, f"A (0,0,0)", color='r')
text_B = ax.text(B_x, B_y, B_z, f"B (0,1,0)", color='b')
text_C = ax.text(C_x, C_y, C_z, f"C (0,1,1)", color='g')
text_AB = ax.text((A_x + B_x) / 2, (A_y + B_y) / 2, (A_z + B_z) / 2, f"AB: {np.linalg.norm([B_x - A_x, B_y - A_y, B_z - A_z]):.2f}", color='k')
text_BC = ax.text((B_x + C_x) / 2, (B_y + C_y) / 2, (B_z + C_z) / 2, f"BC: {BC_length:.2f}", color='k')

# 📌 축 범위 설정 (-1에서 1, 0.25 간격)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

ax.set_xticks(np.arange(-1, 1.25, 0.25))  # X축 0.25 단위로 설정
ax.set_yticks(np.arange(-1, 1.25, 0.25))  # Y축 0.25 단위로 설정
ax.set_zticks(np.arange(-1, 1.25, 0.25))  # Z축 0.25 단위로 설정

ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
ax.set_title("3D Points with Six Sliders (Pending Functionality)")

# 📌 슬라이더 추가 (XY 평면에서 B & C 회전)
ax_slider1 = plt.axes([0.2, 0.25, 0.65, 0.03])  
slider1 = Slider(ax_slider1, 'Rotate B & C (XY)', 0, 360, valinit=0, valstep=1)

# 📌 슬라이더 추가 (YZ 평면에서 C 회전, BC 길이 유지)
ax_slider2 = plt.axes([0.2, 0.20, 0.65, 0.03])  
slider2 = Slider(ax_slider2, 'Rotate C (YZ)', 0, 360, valinit=0, valstep=1)

# 📌 추가된 4개의 슬라이더 (기능 미정, 원하는 동작 추가 가능)
ax_slider3 = plt.axes([0.2, 0.15, 0.65, 0.03])  
slider3 = Slider(ax_slider3, 'Slider 3', 0, 360, valinit=0, valstep=1)

ax_slider4 = plt.axes([0.2, 0.10, 0.65, 0.03])  
slider4 = Slider(ax_slider4, 'Slider 4', 0, 360, valinit=0, valstep=1)

ax_slider5 = plt.axes([0.2, 0.05, 0.65, 0.03])  
slider5 = Slider(ax_slider5, 'Slider 5', 0, 360, valinit=0, valstep=1)

ax_slider6 = plt.axes([0.2, 0.01, 0.65, 0.03])  
slider6 = Slider(ax_slider6, 'Slider 6', 0, 360, valinit=0, valstep=1)

# 📌 슬라이더 업데이트 함수 (현재 slider1과 slider2만 작동, 나머지는 기능 미정)
def update(val):
    theta1 = np.radians(slider1.val)  # XY 평면 회전
    new_B_x = 0  
    new_B_y = np.cos(theta1)
    new_B_z = np.sin(theta1)

    new_C_x = 0  
    new_C_y = np.cos(theta1)
    new_C_z = 1 + np.sin(theta1)

    theta2 = np.radians(slider2.val)  # YZ 평면 회전 (BC 길이 유지)
    move_C_y = new_B_y + BC_length * np.cos(theta2)
    move_C_z = new_B_z + BC_length * np.sin(theta2)

    # 점 위치 업데이트
    B_point.set_data([new_B_x], [new_B_y])
    B_point.set_3d_properties([new_B_z])
    
    C_point.set_data([new_C_x], [move_C_y])
    C_point.set_3d_properties([move_C_z])

    # 선 업데이트
    line_AB.set_data([A_x, new_B_x], [A_y, new_B_y])
    line_AB.set_3d_properties([A_z, new_B_z])

    line_BC.set_data([new_B_x, new_C_x], [new_B_y, move_C_y])
    line_BC.set_3d_properties([new_B_z, move_C_z])

    fig.canvas.draw_idle()

# 📌 슬라이더 값이 변경될 때 update 함수 호출
slider1.on_changed(update)
slider2.on_changed(update)
slider3.on_changed(update)  
slider4.on_changed(update)  
slider5.on_changed(update)  
slider6.on_changed(update)  

# 📌 그래프 표시
plt.show()
