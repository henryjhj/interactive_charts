import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("交互式函数可视化")

# 函数选择
func_name = st.selectbox(
    "选择函数",
    ["sin", "cos", "tan"]
)

# 周期调整
period = st.slider(
    "选择周期（T）",
    min_value=1, max_value=10, value=2, step=1
)

# 数据范围
x = np.linspace(-2*np.pi, 2*np.pi, 1000)

# 根据选择绘制函数
if func_name == "sin":
    y = np.sin(2 * np.pi * x / period)
elif func_name == "cos":
    y = np.cos(2 * np.pi * x / period)
else:  # tan
    y = np.tan(2 * np.pi * x / period)

# 绘制图像
fig, ax = plt.subplots()
ax.plot(x, y, label=f"{func_name}(x), T={period}")
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
ax.set_ylim(-5, 5)  # 限制 y 轴范围，避免 tan 爆掉
ax.legend()
ax.set_title(f"{func_name}(x) with period {period}")

# 显示图表
st.pyplot(fig)