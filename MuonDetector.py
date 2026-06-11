import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# 0. 页面全局配置
# ==========================================
st.set_page_config(page_title="缪子探测器数据分析站", layout="wide")

st.markdown("<style>div[data-testid='stToolbar'] button[kind='header'] {display: none;}</style>", unsafe_allow_html=True)
st.title("🌌 宇宙线缪子物理实验与数据监测站")
st.markdown("基于双层塑料闪烁体与SiPM符合测量的真实物理数据分析平台。请在左侧调整参数，观察统计涨落与物理规律的变化。")

# ==========================================
# 1. 侧边栏：参数交互与文件上传
# ==========================================
st.sidebar.header("⚙️ 实验参数调节")
st.sidebar.markdown("模拟硬件调节与后期数据清洗：")

# 交互控件 1：ADC噪声阈值
adc_threshold = st.sidebar.slider("ADC 噪声阈值(过滤低能本底)", min_value=200, max_value=800, value=350, step=10)

# 交互控件 2：时间积分窗口
time_window_choice = st.sidebar.selectbox("时间积分窗口 (Δt)", ["10秒", "30秒", "60秒"])
time_window_map = {"10秒": 10, "30秒": 30, "60秒": 60}
time_window = time_window_map[time_window_choice]

st.sidebar.markdown("---")
# 交互控件 3：数据文件上传
uploaded_file = st.sidebar.file_uploader("📂 上传探测器数据(.TXT)", type=['txt'])

# ==========================================
# 2. 数据加载与聚合模块
# ==========================================
@st.cache_data
def load_data(file):
    if file is not None:
        # 读取你们的设备数据，跳过前7行参数说明
        df = pd.read_csv(file, sep=r'\s+', skiprows=7)
        # 剔除开机不稳定的 INF 数据
        df = df[df['Flu[s^-1]'] != 'INF']
        df['Time[s]'] = pd.to_numeric(df['Time[s]'])
        return df
    else:
        # 如果未上传文件，生成具有物理特征的演示数据（供老师体验）
        np.random.seed(42)
        time_seq = np.arange(0, 3600, 1) # 1小时虚拟数据
        counts = np.random.poisson(lam=0.8, size=len(time_seq))
        adc1_sim = np.random.lognormal(mean=6.0, sigma=0.3, size=len(time_seq))
        df_sim = pd.DataFrame({'Time[s]': time_seq, 'Count[1]': np.cumsum(counts), 'adc1': adc1_sim})
        return df_sim

df = load_data(uploaded_file)

# 动态计算：根据用户选择的「时间窗口」重组数据
df['Time_Group'] = (df['Time[s]'] // time_window) * time_window
df_grouped = df.groupby('Time_Group').agg({
    'Count[1]': 'last' # 获取该窗口末尾的累积计数
}).reset_index()
# 计算每个窗口内的增量计数 (Delta Count)
df_grouped['Delta_Count'] = df_grouped['Count[1]'].diff().fillna(df_grouped['Count[1]'].iloc[0])
df_grouped['Flux_Hz'] = df_grouped['Delta_Count'] / time_window

# ==========================================
# 3. 主界面：三大物理图表区
# ==========================================
# 第一部分：通量稳定性折线图（横向铺满）
st.subheader(f"📈 1. 缪子通量随时间的演化 (当前积分窗口: {time_window}s)")
fig1, ax1 = plt.subplots(figsize=(12, 3))
ax1.plot(df_grouped['Time_Group'], df_grouped['Flux_Hz'], marker='.', linestyle='-', color='#1f77b4', alpha=0.8)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Flux (Hz)')
ax1.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig1)

# 下方分为两列，展示两个高级物理图表
col1, col2 = st.columns(2)

# 第二部分：泊松分布拟合
with col1:
    st.subheader("📊 2. 放射性统计规律(泊松分布)")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    
    # 统计各个计数值的发生频次
    counts_freq = df_grouped['Delta_Count'].value_counts().sort_index()
    x_data = counts_freq.index.values.astype(float) # 强制转为浮点型防报错
    y_data = counts_freq.values
    
    try:
        # ?? MLE???????? lambda?? curve_fit ???????? lambda?30s/60s????
        lambda_opt = float(np.mean(df_grouped['Delta_Count']))
        N = int(np.sum(y_data))

        # ??????????????? 0??????????? k???????
        k_all = np.arange(0, int(np.max(x_data)) + 1)
        y_all = np.array([int(counts_freq.get(k, 0)) for k in k_all], dtype=float)

        ax2.bar(k_all, y_all, alpha=0.6, color='coral', label='Experiment Data', width=0.8, align='center')

        # ????????????????????? k??????????
        x_fit = np.arange(0, int(lambda_opt + 5*np.sqrt(lambda_opt)) + 1)
        y_fit = poisson.pmf(x_fit, lambda_opt) * N

        ax2.plot(x_fit, y_fit, 'r-', lw=2, label=f'Poisson (λ={lambda_opt:.2f})')
        ax2.set_xlabel(f'Muon Counts per {time_window}s')
        ax2.set_ylabel('Frequency')
        ax2.set_xlim(-0.5, max(int(np.max(x_fit)), int(np.max(k_all))) + 0.5)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    except Exception as e:
        ax2.text(0.5, 0.5, f"拟合异常: {str(e)}", ha='center', va='center', color='red')
        ax2.axis('off')
    st.pyplot(fig2)
# 第三部分：能量沉积谱（朗道分布长尾）
with col2:
    st.subheader("⚡ 3. 沉积能谱分布 (朗道样长尾)")
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    
    if 'adc1' in df.columns:
        all_adcs = pd.to_numeric(df['adc1'], errors='coerce').dropna().values
        # 核心逻辑：使用侧边栏的滑动条动态过滤数据
        valid_adcs = all_adcs[all_adcs > adc_threshold]
        
        ax3.hist(valid_adcs, bins=50, color='purple', alpha=0.7, density=True)
        ax3.set_xlabel('ADC Channel / Energy Deposition')
        ax3.set_ylabel('Probability Density')
        ax3.axvline(x=adc_threshold, color='red', linestyle='--', label=f'Threshold={adc_threshold}')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
    else:
        ax3.text(0.5, 0.5, "请上传包含 adc1 字段的数据", ha='center', va='center')
    st.pyplot(fig3)

# ==========================================
# 4. 教学总结区域
# ==========================================
st.markdown("---")
st.markdown(r"""
**📘 教学指导意见：**
* **本底与噪声**：尝试向**右**拖动 `ADC噪声阈值` 滑块（增大阈值）。低能本底（如环境伽马射线、电子噪声）被过滤后，缪子作为最小电离粒子（MIP）特有的朗道分布「长尾能谱」特征将更加清晰可见。
* **统计误差**：尝试改变 `时间积分窗口`。当窗口过小（如1秒）时，计数少，泊松分布的形状会非常离散且不对称；当窗口增大，平均期望 ($\\lambda$) 变大，泊松分布将逐渐向高斯分布（正态分布）演化，这是深刻理解中心极限定理的绝佳实验。
""")
