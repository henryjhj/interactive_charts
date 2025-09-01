import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("交互式函数 + 数据表")

# 选择函数
func_name = st.selectbox("选择函数", ["sin", "cos", "tan"])
period = st.slider("选择周期（T）", 1, 10, 2)

# 生成数据
x = np.linspace(-2*np.pi, 2*np.pi, 100)
if func_name == "sin":
    y = np.sin(2 * np.pi * x / period)
elif func_name == "cos":
    y = np.cos(2 * np.pi * x / period)
else:
    y = np.tan(2 * np.pi * x / period)

# 绘制图表
fig, ax = plt.subplots()
ax.plot(x, y, label=f"{func_name}(x)")
ax.legend()
ax.set_title(f"{func_name}(x), T={period}")
st.pyplot(fig)

# 显示文字
st.write("### 数据预览")
st.write("下面是部分 (x, y) 数据点：")

# 转换为 DataFrame
df = pd.DataFrame({
    "x": x,
    f"{func_name}(x)": y
})

# 显示 DataFrame（自动带交互功能：排序、搜索、滚动）
st.dataframe(df.head(10))   # 显示前 10 行

# 如果要静态表格（不可交互）
# st.table(df.head(10))