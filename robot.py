import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


from matplotlib.widgets import Slider

# 📌 3D 플롯 생성
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')


# 📌 축 및 제목 설정
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
ax.set_title("Interactive 3D Point with Slider")

ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([0, 1])  # Z 범위 설정


# UR5 DH Parameters
theta_degrees = np.array([0, 0, 0, 0, 0, 0])  # Joint angles (initially set to 0 in degrees)
a = np.array([0, -0.425, -0.392, 0, 0, 0])  # Length of the common normal (a values)
d = np.array([0.089, 0, 0, 0.109, 0.095, 0.082])  # Offset along the z-axis (d values)
alpha = np.array([np.pi / 2, 0, 0, np.pi / 2, -np.pi / 2, 0])  # Link twist angles (alpha values)

x_arr=[]
y_arr=[0,0,0,0,0,0]
z_arr=[]
lastpoint=[0,0]
for i in range(len(a)):
    x_arr.append(lastpoint[0]+a[i])
    z_arr.append(lastpoint[1]+d[i])
    lastpoint=[lastpoint[0]+a[i],lastpoint[1]+d[i]]
print(x_arr)
print(z_arr)

# 📌 초기 점의 좌표 (X, Y 고정, Z는 슬라이더로 변경)
x_point, y_point = 0, 0  # 점의 X, Y 위치는 고정
initial_z = 0.5  # 초기 Z 값


# 📌 점을 그리기 (초기값)
point1, = ax.plot([x_arr[0]], [0.0], [initial_z], 'ro', markersize=8)  # 빨간색 점

# 📌 슬라이더 추가 (Z 값 조절)
ax_slider = plt.axes([0.2, 0.02, 0.65, 0.03])  # (left, bottom, width, height)
slider = Slider(ax_slider, 'Z Value', 0, 1, valinit=initial_z, valstep=0.01)  # 0.01 단위 조절

# 📌 슬라이더 업데이트 함수
def update(val):
    new_z = slider.val  # 슬라이더에서 새로운 Z 값 가져오기
    point.set_data([x_point], [y_point])  # X, Y 좌표는 그대로
    point.set_3d_properties([new_z])  # Z 좌표 업데이트
    fig.canvas.draw_idle()  # 그래프 업데이트

slider.on_changed(update)  # 슬라이더 값이 변경될 때 update 함수 호출

# 📌 그래프 표시
plt.show()
