#!/usr/bin/env python
# coding: utf-8

# ### 평균

# In[1]:

import math
#from scipy.special import gamma
from scipy import integrate as spi
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt

def Mean(x) :
    return float(sum(x)/len(x))


# ### 모분산

# In[2]:


def MVar(x) :
    return sum(map(lambda a:(a - Mean(x))**2, x))/len(x)


# ### 표본분산

# In[3]:


def Var(x) :
    return sum(map(lambda a:(a - Mean(x))**2, x))/(len(x) - 1)


# ### 모표준편차

# In[5]:


def MStd(x) :
    return math.sqrt(MVar(x))


# ### 표본표준편차

# In[6]:


def Std(x) :
    return math.sqrt(Var(x))


# ### 최빈값

# In[7]:


def Mode_dup(x):
    xx = x
    if type(x) != list:
        xx = x.to_list()
    counts = map(lambda elem: (elem, xx.count(elem)), xx)
    return dict(counts)



def Mode(x):
    xx = x
    if type(x) != list:
        xx = x.to_list()
    mode_dict = Mode_dup(xx)
    values = list(mode_dict.values())
    keys = list(mode_dict.keys())
    M = max(values)
    C = values.count(M)
    if M * C == len(xx):
        m = '최빈값은 없다.'
    else:
        mode_list = list(map(lambda idx: keys[idx], filter(lambda idx: values[idx] == M, range(len(values)))))
        m = mode_list
    return m


# ### 중앙값

# In[8]:

def Median(x):
    xx = list(x) if not isinstance(x, list) else x
    xx.sort()
    mid = len(xx) / 2
    return (xx[math.ceil(mid) - 1] + xx[math.floor(mid)]) / 2


# ### 사분위수

# In[9]:


def Q1(x):
    xx = list(x) if not isinstance(x, list) else x
    xx.sort()
    M = (len(xx) + 1) * 0.25
    return float(xx[math.floor(M) - 1] + (xx[math.floor(M)] - xx[math.floor(M) - 1]) * (M - int(M)))

def Q2(x):
    xx = list(x) if not isinstance(x, list) else x
    return Median(xx)


def Q3(x):
    xx = list(x) if not isinstance(x, list) else x
    xx.sort()
    M = (len(xx) + 1) * 0.75
    return float(xx[math.floor(M) - 1] + (xx[math.floor(M)] - xx[math.floor(M) - 1]) * (M - int(M)))

def Q4(x):
    xx = list(x) if not isinstance(x, list) else x
    return max(xx)


# ### 백분위수

# In[10]:


def P_per(x, p):
    # 리스트 변환 및 정렬
    xx = list(x) if not isinstance(x, list) else x
    xx.sort()
    
    # 백분위수 계산
    M = (len(xx) + 1) * (p * 0.01)
    
    # 백분위수 값 반환
    return float(xx[math.floor(M) - 1] + (xx[math.floor(M)] - xx[math.floor(M) - 1]) * (M - math.floor(M)))

# ---
# ---

# ### 모집단공분산

# In[11]:


def Cal_covariance(x, y):
    x_mean = Mean(x)
    y_mean = Mean(y)
    n = len(x)
    cov_elements = map(lambda i: (x[i] - x_mean) * (y[i] - y_mean), range(n))
    cov = sum(cov_elements) / n
    return cov


# ### 표본공분산

# In[12]:


def Cal_sample_covariance(x, y):
    x_mean = Mean(x)
    y_mean = Mean(y)
    n = len(x)
    cov_elements = map(lambda i: (x[i] - x_mean) * (y[i] - y_mean), range(n))
    cov = sum(cov_elements) / (n - 1)
    return cov


# ### 첨도

# In[13]:


#확률 분포의 뾰족한 정도를 측정하는 통계량 / 일반적으로 정규 분포의 첨도는 0, 양수인 경우: 뾰족한 분포, 음수인 경우: 평탄한 분포
def kurtosis(x):
    mean = Mean(x)
    mvar = MVar(x)
    kurtosis_values = map(lambda a: (a - mean) ** 4, x)
    kurtosis_result = sum(kurtosis_values) / (len(x) * (mvar ** 2)) - 3
    return kurtosis_result


# ### 왜도

# In[14]:


#확률 분포의 비대칭성을 측정하는 통계량 / 0에 가까울수록: 분포 대칭, 양수인 경우: 오른쪽에 치우쳐져 있음, 음수인 경우: 왼쪽에 치우쳐져 있음
def skewness(x):
    mean = Mean(x)
    std = MStd(x)
    skewness_values = map(lambda a: (a - mean) ** 3, x)
    skewness_result = sum(skewness_values) / (len(x) * (std ** 3))
    return skewness_result


# In[ ]:





# ## 확률

# ### 베이즈 정리(두 사건)

# In[15]:


# prior_A: A 사건의 사전 확률
# prior_A_2: A_2 사건의 사전 확률
# B_A: B 사건이 일어났을 때의 A 사건의 우도
# B_A_2: B 사건이 일어났을 때의 A_2 사건의 우도
def bayes_theorem(prior_A, prior_A_2, B_A, B_A_2): 
    # A 사건의 사후확률
    posterior_A = (prior_A * B_A) / (prior_A * B_A + prior_A_2 * B_A_2)
    # A_2 사건의 사후확률
    posterior_A_2 = 1 - posterior_A
    return posterior_A, posterior_A_2


# ### 베이즈 정리(일반화)

# In[16]:


# priors: 각 사건의 사전 확률을 담은 리스트
# likelihoods: 각 사건이 일어났을 때의 조건부 확률(우도)을 담은 리스트
def generalized_bayes_theorem(x, y):
    numerator = 1
    denominator = sum(map(lambda prior, likelihood: prior * likelihood, x, y))
    # 각 사건의 사후확률 계산
    posteriors = list(map(lambda prior, likelihood: prior * likelihood / denominator, x, y))
    for idx, posterior in enumerate(posteriors):
        print(f"사건 {idx+1}의 사후확률:", posterior)
    return posteriors


# ### 이산형 확률변수

# #### 이산형 확률변수의 확률질량함수

# In[17]:


# 'x': 이산형 확률변수, 'y': 해당 x값의 도수
def dis_pmf(x, y):
    total_sum = sum(y)
    pmf_dict = dict(map(lambda a_b: (a_b[0], a_b[1] / total_sum), zip(x, y)))
    return pmf_dict


# #### 이산형 확률변수의 누적확률분포함수

# In[18]:


# #### 이산형 확률변수의 기댓값
# 속도 수정
# 'pmf': 이산형 확률변수의 확률질량함수, 'x': 누적확률분포함수를 계산할 값
def dis_cpdf(pmf, x):
    return float(sum(map(lambda item: item[1] if item[0] <= x else 0, pmf.items())))



# In[19]:


# 'x': 이산형 확률변수, 'y': 이산형 확률변수의 확률질량함수
def dis_expected_value(x, y):
    ev = sum(map(lambda value, probability: value * probability, x, y))
    return ev

# 'x': 이산형 확률변수, 'y': 해당 x값의 도수
def dis_expected_value_frequency(x, y):
    total_sum = sum(map(lambda value, frequency: value * frequency, x, y))
    total_count = sum(y)
    mean = total_sum / total_count
    return mean


# #### 이산형 확률변수의 분산

# In[20]:


# 'x': 이산형 확률변수, 'y': 이산형 확률변수의 확률질량함수
def dis_variance(x, y):
    return sum(prob * (value - dis_expected_value(x, y)) ** 2 for value, prob in zip(x, y))

# 'x': 이산형 확률변수, 'y': 해당 x값의 도수
def dis_variance_frequency(x, y):
    total_sum = 0
    total_count = 0
    for value, frequency in zip(x, y):
        total_sum += frequency * (value - dis_expected_value_frequency(x, y)) ** 2
        total_count += frequency
    return total_sum / total_count


# #### 이산형 확률변수의 표준편차

# In[21]:


# 'x': 이산형 확률변수, 'y': 이산형 확률변수의 확률질량함수
def dis_standard_deviation(x,y):
    return math.sqrt(dis_variance(x,y))

# 'x': 이산형 확률변수, 'y': 해당 x값의 도수
def dis_standard_deviation_frequency(x, y):
    return math.sqrt(dis_variance_frequency(x, y))


# ### 이항분포

# #### 이항계수

# In[22]:


# 'n': 전체 수, 'k': 특정 수
def bi_coefficient(n, k):
    if k == 0 or k == n:
        return 1
    return bi_coefficient(n - 1, k - 1) + bi_coefficient(n - 1, k)


# #### 이항분포의 확률질량함수

# In[23]:


# 'n': 전체 수, 'p': 확률, 'k': 특정 수
def bi_pmf(n, p, k):
    return bi_coefficient(n, k) * (p ** k) * ((1 - p) ** (n - k))


# #### 이항확률분포의 평균

# In[24]:


# 'n':전체 수, 'p': 확률
def bi_mean(n, p):
    return n * p


# #### 이항확률분포의 분산

# In[25]:


# 'n':전체 수, 'p': 확률
def bi_variance(n, p):
    return n * p * (1 - p)


# ### 포아송분포

# #### 포아송분포의 확률질량함수

# In[26]:


# 'lambd': 평균 발생 횟수, 'k': 발생 횟수, 관찰수 
def po_pmf(lambd, k):
    return float((math.exp(-lambd) * (lambd ** k)) / math.factorial(k))


# #### 이항분포의 포아송분포 근사 후 평균

# In[27]:


# 'lambd': 평균 발생 횟수, 'k': 발생 횟수, 관찰수 , 'n': 전체 수
def po_bi_mean(lambd, k, n):
    return n * po_pmf(lambd, k)


# #### 이항분포의 포아송분포 근사 후 분산

# In[28]:


# 'lambd': 평균 발생 횟수, 'k': 발생 횟수, 관찰수 , 'n': 전체 수
def po_bi_variance(lambd, k, n):
    return n * po_pmf(lambd, k) * (1-po_pmf(lambd, k))


# ### 연속형 확률변수

# #### 연속형 확률변수의 누적분포함수

# In[29]:



x = sp.Symbol('x') #변수 지정 必
# 'f': 확률변수의 확률밀도함수(x변수로 구성된 함수), 'l': lower_bound, 'u': upper_bound, -sp.oo=-oo, sp.oo=oo로 표기
def con_cdf(f,l,u):
    cdf = sp.integrate(f, (x,l,u))
    return cdf.subs(x, u)


# #### 연속형 확률변수의 평균

# In[30]:


# 'f': 변수 x로만 이루어져있는 function, 'l': lower_bound, 'u': upper_bound, 'n': num_intervals 
def con_mean(f, l, u):
    return float(con_cdf(x*f, l, u))


# #### 연속형 확률변수의 분산

# In[31]:


# 'f': 변수 x로만 이루어져있는 function, 'l': lower_bound, 'u': upper_bound, 'n': num_intervals 
def con_variance(f, l, u):
    return float(con_cdf((x-con_mean(f,l,u))**2*f, l, u))


# ### 균일분포

# #### 균일분포의 누적분포함수

# In[32]:


# 'x': 확률변수 값, 'a': 균일분포 구간의 하한, 'b': 균일분포 구간의 상한
def uni_cdf(x, a, b):
    if x < a:
        return 0
    elif x >= b:
        return 1
    else:
        return (x - a) / (b - a)


# #### 균일분포의 평균

# In[33]:


# 'a': 균일분포 구간의 하한, 'b': 균일분포 구간의 상한
def uni_mean(a, b):
    return float((a + b) / 2)


# #### 균일분포의 분산

# In[34]:


# 'a': 균일분포 구간의 하한, 'b': 균일분포 구간의 상한
def uni_variance(a, b):
    return float(((b - a) ** 2) / 12)


# ### 정규분포

# #### 정규분포의 확률밀도함수

# In[35]:


# 'x': 확률변수 값, 'm': 평균, 's': 표준편차
def nor_pdf(x, m, s):
    return float((1 / (math.sqrt(2 * math.pi) * s)) * math.exp(-((x - m) ** 2) / (2 * s ** 2)))


# #### 표준정규분포의 확률밀도함수

# In[36]:


# 'x': 확률변수 값
def sta_nor_pdf(x):
    return float((1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * x ** 2))


# #### 표준정규분포의 누적분포함수

# In[37]:


#'x': 누적분포함수 값을 계산할 확률변수 값 (-oo<=a<=x)
def sta_nor_cdf(x):
    return float((1 + math.erf(x / math.sqrt(2))) / 2)


# In[38]:


# a에서 b까지의 넓이를 구해서 처리 작업 추가 (a, b)-> sta_nor_cdf(b)와 sta_nor_cdf(a)의 차
# 연속함수 작업에 동일하게 고려하기


# In[39]:


def sta_nor_cdf_ab(a, b):
    return sta_nor_cdf(b) - sta_nor_cdf(a)


# #### 이항분포의 정규근사

# In[40]:


#정규분포는 이항분포의 확률에 대한 근사 계산을 제공


# In[41]:


# 'n': 전체 수, 'p': 확률, 'x': 비교하고자 하는 표본 수 
def nor_bi_ap(n, p, x):
    in_x = (x - n * p) / math.sqrt(n * p * (1 - p))
    return sta_nor_cdf(in_x)


# ### 지수분포

# #### 지수분포의 확률밀도함수

# In[42]:


# 'lambd': 비율 매개변수(양수), 'x': 확률변수 값
def exp_pdf(lambd, x):
    if x < 0:
        return 0
    return lambd * math.exp(-lambd * x)


# #### 지수분포의 누적분포함수

# In[43]:


# 'lambd': 비율 매개변수(양수), 'x': 확률변수 값, P(a<=X)=exp(-lambd*a), P(0<=X<=b)=1-exp(-lambd*b) [설명추가 必]
def exp_cdf(lambd, x):
    if x < 0:
        return 0
    return 1 - math.exp(-lambd * x)


# In[ ]:


#** a와 b사이의 넓이


# In[ ]:





# #### 지수분포의 평균

# In[44]:


# 'lambd': 비율 매개변수(양수)
def exp_mean(lambd):
    return 1 / lambd


# #### 지수분포의 분산

# In[45]:


# 'lambd': 비율 매개변수(양수)
def exp_variance(lambd):
    return 1 / (lambd ** 2)


# ## 표본추출과 표집분포

# ### 단순확률추출

# #### (비복원추출 - 유한모집단) 표본평균의 기댓값

# In[46]:


# 'm': 모집단의 평균
def sim_expected_value(m):
    return m


# #### (비복원추출 - 유한모집단) 표본평균의 분산 

# In[47]:


# 'N': 모집단의 크기, 'n': 표본 수, 'v': 모집단의 분산
def sim_variance(N, n, v):
    return float(((N-n)/(N-1)) * (v/n))


# #### (비복원추출 - 유한모집단) 표본평균의 표준오차 

# In[48]:


# 'N': 모집단의 크기, 'n': 표본 수, 'v': 모집단의 분산
def sim_std_err(N, n, v):
    return math.sqrt(sim_variance(N, n, v))


# #### (복원추출 - 무한모집단) 표본평균의 기댓값

# In[49]:


# 'm': 모집단의 평균
def sim_re_expected_value(m):
    return m


# #### (복원추출 - 무한모집단) 표본평균의 분산

# In[50]:


# 'n': 표본 수, 'v': 모집단의 분산
def sim_re_variance(n, v):
    return float(v/n)


# #### (복원추출 - 무한모집단) 표본평균의 표준오차

# In[51]:


def sim_re_std_err(n, v):
    return math.sqrt(sim_re_variance(n, v))


# ### 비율의 표집분포

# In[52]:


# 모집단이 이항분포이면 표본비율은 표본크기가 충분히 클 때 대수의 법칙과 중심극한정리를 적용할 수 있다. 조건: n*p>=5, n*(1-p)>=5


# #### 표본비율의 평균

# In[53]:


# 'n':전체 수, 'p': 확률
def sam_pro_mean(n, p):
    return p


# In[54]:


# 경우 추가- 'x': 표본평균 리스트, 'p': 표본평균에 해당하는 확률
def sam_pro_mean_list(x, p):
    exp = sum(map(lambda xi, pi: xi * pi, x, p))
    return exp


# #### 표본비율의 분산

# In[55]:


# 'n':전체 수, 'p': 확률
def sam_pro_variance(n, p):
    return (p*(1-p))/n


# In[56]:


# 경우 추가- 'x': 표본평균 리스트, 'p': 표본평균에 해당하는 확률
def sam_pro_variance_list(x, p):
    exp = sum(map(lambda xi, pi: xi * pi, x, p))
    exp2 = sum(map(lambda xi, pi: (xi ** 2) * pi, x, p))
    return exp2 - exp ** 2


# #### 표본비율의 표준오차

# In[57]:


# 'n':전체 수, 'p': 확률
def sam_pro_std_err(n, p):
    return math.sqrt(sam_pro_variance(n, p))


# In[58]:


# 경우 추가- 'x': 표본평균 리스트, 'p': 표본평균에 해당하는 확률
def sam_pro_std_err_list(x, p):
    return math.sqrt(sam_pro_variance_list(x, p))


# ## 추정

# ### 점추정

# #### 표본에서 모평균 추정(비편향 추정량)

# In[59]:


# 'x': 표본 데이터
def est_mean(x):
    return Mean(x)


# #### 표본에서 모표준편차 추정

# In[60]:


# 'x': 표본 데이터
def est_std(x):
    return MStd(x)


# #### 비편향성 여부 판단

# In[61]:


# 'x': 실제 모평균, 'y': 추정된 모평균
def check_unbiasedness(x, y):
    if x - y == 0 :
        print("추정량은 비편향 추정량입니다.")
    else:
        print("추정량은 편향 추정량입니다.")
    return x - y


# #### 일치성 여부 판단

# In[62]:


import random
# 'x': 실제 모평균, size': 표본 크기 (리스트 형태-1개 이상 가능), 'num': 시도 횟수(에제에서는 무한의 경우)
def check_consistency(x, size, num):
    consistent_estimators = list(map(lambda n: Mean(list(map(lambda _: est_mean([random.uniform(0, 1) for _ in range(n)]), range(num)))), size))
    return consistent_estimators


# In[ ]:





# In[ ]:





# ### 구간추정

# #### 모평균에 대한 구간추정

# ##### 모표준편차를 아는 경우

# In[63]:



# In[64]:


# 's': 모표준편차, x': 표본 데이터, 'a': 유의수준(alpha) 
def con_interval_z(s, x, a):
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    target_cell = df[df.eq(0.5-a/2).any(1)]
    row = target_cell.index.tolist()[0]
    column = target_cell.columns[target_cell.eq(0.5-a/2).any()][0]
    cr = float(row)+float(column)
    return (float(Mean(x) - cr*s/math.sqrt(len(x))), float(Mean(x) + cr*s/math.sqrt(len(x))))


# ##### 모표준편차를 모를 경우

# In[65]:


# 'x': 표본 데이터, 'a': 유의수준(alpha)
def con_interval_t(x, a):    
    df = pd.read_csv('./t분포표.csv', encoding='euc-kr', index_col=0) 
    cr = df["%g" %(a/2)][int(len(x) - 1)]
    return (float(Mean(x)-cr*(Std(x)/math.sqrt(len(x)))), float(Mean(x)+cr*(Std(x)/math.sqrt(len(x)))))


# #### 모비율에 대한 구간추정

# In[66]:


# 속도 수정
# 'n': 표본 수, 'x': 발생 횟수, 관찰 수, 'a': 유의수준(alpha) 
def con_interval_p(n, x, a):
    p = x / n
    if n * p >= 5 and n * (1 - p) >= 5:
        df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
        target_cell = df[df.eq(0.5 - a/2).any(1)]

        if target_cell.empty:
            # 가장 가까운 표준 정규 분포 값 찾기
            differences = abs(df.values.flatten() - (0.5 - a/2))
            min_difference = differences.min()
            nearest_values = df.values.flatten()[differences == min_difference]

            # 가장 가까운 값들로 ratio 갱신
            cr_list = list(map(lambda x: float(df[df.eq(x).any(1)].index[0]) + float(df.columns[df.eq(x).any()][0]), nearest_values))
            cr = round(Mean(cr_list), 3)

        else:
            row = target_cell.index.tolist()[0]
            column = target_cell.columns[target_cell.eq(0.5 - a/2).any()][0]
            cr = float(row) + float(column)
            
        return (float(p - cr * math.sqrt(p * (1 - p) / n)), float(p + cr * math.sqrt(p * (1 - p) / n)))
    
    else:
        return "경고: n * p와 n * (1 - p)가 5 이상이어야 합니다."


# In[ ]:





# ### 표준정규분포표에서 없는 값 근사하여 cr 즉 기각역 찾기

# #### 양측

# In[67]:


# 속도 수정
def two_tailed_pred_interval_p(a):
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    target_cell = df[df.eq(0.5 - a/2).any(1)]
    
    if target_cell.empty:
        # 가장 가까운 표준 정규 분포 값 찾기
        differences = abs(df.values.flatten() - (0.5 - a/2))
        min_difference = differences.min()
        nearest_values = df.values.flatten()[differences == min_difference]

        # 가장 가까운 값들로 ratio 갱신
        cr_list = list(map(lambda x: float(df[df.eq(x).any(1)].index[0]) + float(df.columns[df.eq(x).any()][0]), nearest_values))
        cr = round(Mean(cr_list), 3)
        
    else:
        row = target_cell.index.tolist()[0]
        column = target_cell.columns[target_cell.eq(0.5 - a/2).any()][0]
        cr = float(row) + float(column)

    return cr


# #### 단측

# In[68]:


# 속도 수정
def one_tailed_pred_interval_p(a):
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    target_cell =  df[df.eq(0.5 - a).any(1)]
    
    if target_cell.empty:
        # 가장 가까운 표준 정규 분포 값 찾기
        differences = abs(df.values.flatten() - (0.5 - a))
        min_difference = differences.min()
        nearest_values = df.values.flatten()[differences == min_difference]

        # 가장 가까운 값들로 ratio 갱신
        cr_list = list(map(lambda x: float(df[df.eq(x).any(1)].index[0]) + float(df.columns[df.eq(x).any()][0]), nearest_values))
        cr = round(Mean(cr_list), 3)
        
    else:
        row = target_cell.index.tolist()[0]
        column = target_cell.columns[target_cell.eq(0.5 - a).any()][0]
        cr = float(row) + float(column)

    return cr


# ---
# ---

# ## 모평균에 대한 검정

# ### z-검정(모표준편차를 알 때,  모집단 1개)
# - Z검정은 p값과 기각역을 함수로 한꺼번에 구한다

# In[69]:





# #### 양측 z검정

# In[70]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모평균이 'm'인지 확인, 모표준편차 's'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 1개, 양측검정 [Z1_Twosided 축약 : Z1_Ts]

def Z1_Ts(a,x,m,s) :     
    
    Z = round((Mean(x) - m)/(s/math.sqrt(len(x))),17)
    print("1.검정통계량 : %g" %Z)
    
    y, z = sp.symbols('y z') 
    f = 1 / (math.sqrt(2 * math.pi)) * sp.exp(-z**2 / 2)
    I = sp.integrate(f,(z,0,y))
    eqn = sp.Eq(I, 0.5 - a/2)
    cr = round(sp.solve( eqn, y )[0],3)
    print("\n2.임계값 : {0}, {1}".format(-cr,cr))
    print("\n3.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))
    
    I2 = (0.5 - sp.Integral(f,(z,0,abs(Z))))*2             
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
    
    if cr < abs(Z) :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 z검정(표에서 기각역 찾기)

# In[71]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모평균이 'm'인지 확인, 모표준편차 's'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 1개, 양측검정 [Z1_Twosided 축약 : Z1_Ts]

def Z1_Tscr(a,x,m,s) :
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    Z = round((Mean(x) - m)/(s/math.sqrt(len(x))),17)
    print("1.검정통계량 : %g" %Z)
    
    z = sp.symbols('z') 
    f = 1 / (math.sqrt(2 * math.pi)) * sp.exp(-z**2 / 2)
    cr = two_tailed_pred_interval_p(a)
    print("\n2.임계값 : {0}, {1}".format(-cr,cr))
    print("\n3.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))
    
    I2 = (0.5 - sp.Integral(f,(z,0,abs(Z))))*2             
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
    
    if cr < abs(Z) :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 z검정(위꼬리 검정)

# In[72]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모평균이 'm'보다 큰지 확인, 모표준편차 's'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 1개, 위꼬리검정 [Z1_Upsided 축약 : Z1_Up]

def Z1_Up(a,x,m,s) :            
    
    Z = round((Mean(x) - m)/(s/math.sqrt(len(x))),17)
    print("1.검정통계량 : %g" %Z)

    y, z = sp.symbols('y z') 
    f = 1/(math.sqrt(2*math.pi))*sp.exp(-(z**2)/2)
    I = sp.integrate(f,(z,0,y))
    eqn = sp.Eq(I, 0.5 - a)
    cr = round(sp.solve( eqn, y )[0],3)
    print("\n2.임계값 : {0}".format(cr))
    print("\n3.기각역 : ({0}, oo)".format(cr)) 
    
    if Z >= 0 :
        I2 = 0.5 - sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 + sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
        
    if cr < Z :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 z검정(위꼬리 검정) (표에서 기각역 찾기)

# In[73]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모평균이 'm'보다 큰지 확인, 모표준편차 's'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 1개, 위꼬리검정 [Z1_Upsided 축약 : Z1_Up]

def Z1_Upcr(a,x,m,s) :            
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    Z = round((Mean(x) - m)/(s/math.sqrt(len(x))),17)
    print("1.검정통계량 : %g" %Z)

    z = sp.symbols('z') 
    f = 1/math.sqrt(2*math.pi)*math.exp(-(z^2)/2)
    
    cr = one_tailed_pred_interval_p(a)
    print("\n2.임계값 : {0}".format(cr))
    print("\n3.기각역 : ({0}, oo)".format(cr)) 
    
    if Z >= 0 :
        I2 = 0.5 - sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 + sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
        
    if cr < Z :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 z검정(아래꼬리 검정)

# In[74]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모평균이 'm'보다 작은지 확인, 모표준편차 's'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 1개, 아래꼬리검정 [Z1_Undersided 축약 : Z1_Un]

def Z1_Un(a,x,m,s) :        
    
    Z = round((Mean(x) - m)/(s/math.sqrt(len(x))),17)
    print("1.검정통계량 : %g" %Z)
    
    y, z = sp.symbols('y z') 
    f = 1/math.sqrt(2*math.pi)*sp.exp(-(z**2)/2)
    I = sp.integrate(f,(z,0,y))
    eqn = sp.Eq(I, 0.5 - a)
    cr = round(sp.solve( eqn, y )[0],3)
    print("\n2.임계값 : {0}".format(-cr))
    print("\n3.기각역 : (-oo, {0})".format(-cr))
    
    if Z >= 0 :
        I2 = 0.5 + sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 - sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2)
    print("\n5.유의수준 : %g" %a)
    
    if Z < -cr :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 z검정(아래꼬리 검정) (표에서 기각역 찾기)

# In[75]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모평균이 'm'보다 작은지 확인, 모표준편차 's'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 1개, 아래꼬리검정 [Z1_Undersided 축약 : Z1_Un]

def Z1_Uncr(a,x,m,s) :        
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    Z = round((Mean(x) - m)/(s/math.sqrt(len(x))),17)
    print("1.검정통계량 : %g" %Z)
    
    z = sp.symbols('z') 
    f = 1/math.sqrt(2*math.pi)*sp.exp(-(z**2)/2)
    cr = one_tailed_pred_interval_p(a)
    print("\n2.임계값 : {0}".format(-cr))
    print("\n3.기각역 : (-oo, {0})".format(-cr))
    
    if Z >= 0 :
        I2 = 0.5 + sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 - sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2)
    print("\n5.유의수준 : %g" %a)
    
    if Z < -cr :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ### z-검정(두 모표준편차를 알 때,  모집단 2개)

# #### 양측 z2검정

# In[76]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 두 모평균이 같은지 확인, 두 모표준편차 'xs, ys'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 2개, 양측검정 [Z2_Twosided 축약 : Z2_Ts]

def Z2_Ts(a, x, y, xs, ys) :       

    Z = round((Mean(x) - Mean(y)) / (math.sqrt(((xs**2)/len(x)) + ((ys**2)/len(y)))),17)
    print("1.검정통계량 : %g" %Z)  
    
    w, z = sp.symbols('w z') 
    f = 1/math.sqrt(2*math.pi)*sp.exp(-(z**2)/2)
    I = sp.integrate(f,(z,0,w))
    eqn = sp.Eq(I, 0.5 - a/2)
    cr = round(sp.solve( eqn, w )[0],3)
    print("\n2.임계값 : {0}, {1}".format(-cr, cr))
    print("\n3.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr, cr))
    
    I2 = (0.5 - sp.Integral(f,(z,0,abs(Z))))*2
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
    
    if cr < abs(Z) :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans

# #### 양측 z2검정(표에서 기각역 찾기)

# In[77]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 두 모평균이 같은지 확인, 두 모표준편차 'xs, ys'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 2개, 양측검정 [Z2_Twosided 축약 : Z2_Ts]

def Z2_Tscr(a, x, y, xs, ys) :       
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    Z = round((Mean(x) - Mean(y)) / (math.sqrt(((xs**2)/len(x)) + ((ys**2)/len(y)))),17)
    print("1.검정통계량 : %g" %Z)  
    
    z = sp.symbols('z') 
    f = 1/math.sqrt(2*math.pi)*sp.exp(-(z**2)/2)
    cr = two_tailed_pred_interval_p(a)
    print("\n2.임계값 : {0}, {1}".format(-cr, cr))
    print("\n3.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr, cr))
    
    I2 = (0.5 - sp.Integral(f,(z,0,abs(Z))))*2
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
    
    if cr < abs(Z) :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 z2검정(위꼬리 검정)

# In[78]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차 'xs, ys'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 2개, 위꼬리검정 [Z2_Upsided 축약 : Z2_Up]

def Z2_Up(a,x,y,xs,ys) :             
    
    Z = round((Mean(x) - Mean(y)) / (math.sqrt(((xs**2)/len(x)) + ((ys**2)/len(y)))),17)
    print("1.검정통계량 : %g" %Z)
    
    w, z = sp.symbols('w z') 
    f = 1/math.sqrt(2*math.pi)*sp.exp(-(z**2)/2)
    I = sp.integrate(f,(z,0,w)) 
    eqn = sp.Eq(I, 0.5 - a)
    cr = round(sp.solve( eqn, w )[0], 3)
    print("\n2.임계값 : {0}".format(cr))
    print("\n3.기각역 : ({0}, oo)".format(cr))
    
    if Z >= 0 :
        I2 = 0.5 - sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 + sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
   
    if cr < Z :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 z2검정(위꼬리 검정) (표에서 기각역 찾기)

# In[79]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차 'xs, ys'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 2개, 위꼬리검정 [Z2_Upsided 축약 : Z2_Up]

def Z2_Upcr(a,x,y,xs,ys) :                
    Z = round((Mean(x) - Mean(y)) / (math.sqrt(((xs**2)/len(x)) + ((ys**2)/len(y)))),17)
    print("1.검정통계량 : %g" %Z)
    
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    z = sp.symbols('z') 
    f = 1/math.sqrt(2*math.pi)*sp.exp(-(z**2)/2)
    cr = one_tailed_pred_interval_p(a)
    print("\n2.임계값 : {0}".format(cr))
    print("\n3.기각역 : ({0}, oo)".format(cr))
    
    if Z >= 0 :
        I2 = 0.5 - sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 + sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
   
    if cr < Z :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 z2검정(아래꼬리 검정)

# In[80]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차 'xs, ys'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 2개, 아래꼬리검정 [Z2_Undersided 축약 : Z2_Un]

def Z2_Un(a,x,y,xs,ys) :          
        
    Z = round((Mean(x) - Mean(y))/(math.sqrt(((xs**2)/len(x)) + ((ys**2)/len(y)))),17)
    print("1.검정통계량 : %g" %Z)
    
    w, z = sp.symbols('w z') 
    f = 1/math.sqrt(2*math.pi)*sp.exp(-(z**2)/2)
    I = sp.integrate(f,(z,0,w))
    eqn = sp.Eq(I, 0.5 - a)
    cr = round(sp.solve( eqn, w)[0],3)
    print("\n2.임계값 : {0}".format(-cr))
    print("\n3.기각역 : (-oo, {0})".format(-cr))
    
    if Z >= 0 :
        I2 = 0.5 + sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 - sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2)
    print("\n5.유의수준 : %g" %a)
    
    if Z < -cr :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 z2검정(아래꼬리 검정) (표에서 기각역 찾기)

# In[81]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차 'xs, ys'를 아는 경우
# 모표준편차를 아는 경우이므로, z검정을 사용, 모집단 2개, 아래꼬리검정 [Z2_Undersided 축약 : Z2_Un]

def Z2_Uncr(a,x,y,xs,ys) :          
        
    Z = round((Mean(x) - Mean(y))/(math.sqrt(((xs**2)/len(x)) + ((ys**2)/len(y)))),17)
    print("1.검정통계량 : %g" %Z)
    
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    z = sp.symbols('z') 
    f = 1/math.sqrt(2*math.pi)*sp.exp(-(z**2)/2)
    cr = one_tailed_pred_interval_p(a)

    print("\n2.임계값 : {0}".format(-cr))
    print("\n3.기각역 : (-oo, {0})".format(-cr))
    
    if Z >= 0 :
        I2 = 0.5 + sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 - sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2)
    print("\n5.유의수준 : %g" %a)
    
    if Z < -cr :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ### t-검정(모표준편차를 모를 때,  모집단 1개)
# - t검정은 [함수로 p값 구하는 모듈 / 표로 기각역 구하는 모듈] 두 가지로 구분
# - 합쳐놓은 것 추가

# In[82]:




# #### 양측 t검정 (표 : 기각역)

# In[83]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 모평균이 'm'인지 확인, 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 1개, 양측 기각역 검정 
# T1_Twosided_criticalregion 축약 : T1_Tscr

def T1_Tscr(a,x,m) :
    
    df = pd.read_csv('./t분포표.csv', encoding='euc-kr', index_col=0) 

    T1 = round(Mean(x) - m) / (Std(x)/math.sqrt(len(x)))
    print("1.검정통계량: %g" %T1)              
    print("\n2.자유도 :", len(x) - 1)
    
    cr = df["%g" %(a/2)][int(len(x) - 1)]
    print("\n3.임계값 : {0}, {1}".format(-cr,cr))
    print("\n4.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))
    
    if cr < abs(T1) :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 t검정 (함수 : p값)

# In[84]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 모평균이 'm'인지 확인, 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 1개, 양측 p값 검정 
# T1_Twosided_probabilityvalue 축약 : T1_Tsp

def T1_Tsp(a,x,m) :
    
    t = round((Mean(x) - m) / (Std(x)/math.sqrt(len(x))),17)     
    print("1.검정통계량 : %g" %t)
    
    v = len(x) - 1                  
    print("\n2.자유도 :",v)
    
    z = sp.symbols('z')
    f = (math.gamma((v+1)/2)/(math.sqrt(v*math.pi)*math.gamma(v/2)))*((1+(z**2)/v)**(-(v+1)/2))     
    I = 0.5 - sp.Integral(f,(z,0,abs(t)))           
    print("\n3.p값 : %g" %(I*2))
    print("\n4.유의수준 : %g" %a)
    
    if I < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 t검정 (모든 정보 다 나오게)

# In[85]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 모평균이 'm'인지 확인, 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 1개, 양측검정 
# T1_Twosided 축약 : T1_Ts

def T1_Ts(a,x,m) :
    
    df = pd.read_csv('./t분포표.csv', encoding='euc-kr', index_col=0) 

    t = round((Mean(x) - m) / (Std(x)/math.sqrt(len(x))),17)     
    print("1.검정통계량 : %g" %t)
    
    v = len(x) - 1                  
    print("\n2.자유도 :",v)
    
    cr = df["%g" %(a/2)][int(v)]
    print("\n3.임계값 : {0}, {1}".format(-cr,cr))
    print("\n4.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))
    
    z = sp.symbols('z')
    f = (math.gamma((v+1)/2)/(math.sqrt(v*math.pi)*math.gamma(v/2)))*((1+(z**2)/v)**(-(v+1)/2))     
    I = 0.5 - sp.Integral(f,(z,0,abs(t)))           
    print("\n5.p값 : %g" %(I*2))
    print("\n6.유의수준 : %g" %a)
    
    if I < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t검정 (위꼬리 검정) (표 : 기각역)

# In[86]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 모평균이 'm'보다 큰지 확인, 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 1개, 위꼬리 기각역 검정 
# T1_Upsided_criticalregion 축약 : T1_Upcr

def T1_Upcr(a,x,m) :             

    df = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)

    T1 = (Mean(x) - m) / (Std(x)/math.sqrt(len(x)))
    print("1.검정통계량 : %g" %T1)                 
    print("\n2.자유도 :", len(x) - 1)
    
    cr = df["%g" %a][int(len(x) - 1)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    if cr < T1 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t검정 (위꼬리 검정) (함수 : p값)

# In[87]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 모평균이 'm'보다 큰지 확인, 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 1개, 위꼬리 p값 검정 
# T1_Upsided_probabilityvalue 축약 : T1_Upp

def T1_Upp(a,x,m) :
    
    t = round((Mean(x) - m) / (Std(x)/math.sqrt(len(x))),17)     
    print("1.검정통계량 : %g" %t)

    v = len(x) - 1                  
    print("\n2.자유도 :",v)
    
    z = sp.symbols('z')
    f = (math.gamma((v+1)/2)/(math.sqrt(v*math.pi)*math.gamma(v/2)))*((1+(z**2)/v)**(-(v+1)/2))
    
    if t >= 0 :
        TI = 0.5 - sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 + sp.Integral(f,(z,0,abs(t)))
    print("\n3.p값 : %g" %TI)
    print("\n4.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t검정 (위꼬리 검정) (모든 정보 다 나오게)

# In[88]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 모평균이 'm'보다 큰지 확인, 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 1개, 위꼬리검정 
# T1_Upsided 축약 : T1_Up

def T1_Up(a,x,m) :             

    df = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)

    t = round((Mean(x) - m) / (Std(x)/math.sqrt(len(x))),17)     
    print("1.검정통계량 : %g" %t)

    v = len(x) - 1                  
    print("\n2.자유도 :",v)
    
    cr = df["%g" %a][int(v)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    z = sp.symbols('z')
    f = (math.gamma((v+1)/2)/(math.sqrt(v*math.pi)*math.gamma(v/2)))*((1+(z**2)/v)**(-(v+1)/2))
    if t >= 0 :
        TI = 0.5 - sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 + sp.Integral(f,(z,0,abs(t)))
    print("\n5.p값 : %g" %TI)
    print("\n6.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t검정(아래꼬리 검정) (표 : 기각역)

# In[89]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 모평균이 'm'보다 작은지 확인, 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 1개, 아래꼬리 기각역 검정 
# T1_Undersided_criticalregion 축약 : T1_Uncr

def T1_Uncr(a,x,m) :          
    
    df = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)        
    
    T1 = (Mean(x) - m) / (Std(x)/math.sqrt(len(x)))
    print("1.검정통계량 : %g" %T1)              
    print("\n2.자유도 :", len(x) - 1)
    
    cr = df["%g" %a][int(len(x) - 1)]
    print("\n3.임계값 : {0}".format(-cr))
    print("\n4.기각역 : (-oo, {0})".format(-cr))
    
    if T1 < -cr :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t검정 (아래꼬리 검정) (함수 : p값)

# In[90]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 모평균이 'm'보다 큰지 확인, 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 1개, 아래꼬리 p값 검정 
# T1_Undersided_probabilityvalue 축약 : T1_Unp

def T1_Unp(a,x,m) :
    
    t = round((Mean(x) - m) / (Std(x)/math.sqrt(len(x))),17)    
    print("1.검정통계량 : %g" %t)

    v = len(x) - 1                  
    print("\n2.자유도 :",v)
    
    z = sp.symbols('z')
    f = (math.gamma((v+1)/2)/(math.sqrt(v*math.pi)*math.gamma(v/2)))*((1+(z**2)/v)**(-(v+1)/2))
    if t >= 0 :
        TI = 0.5 + sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 - sp.Integral(f,(z,0,abs(t)))
    print("\n3.p값 : %f" %TI)
    print("\n4.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t검정 (아래꼬리 검정) (모든 정보 다 나오게)

# In[91]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 모평균이 'm'보다 작은지 확인, 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 1개, 아래꼬리검정 
# T1_Undersided 축약 : T1_Un

def T1_Un(a,x,m) :             

    df = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)

    t = round((Mean(x) - m) / (Std(x)/math.sqrt(len(x))),17)     
    print("1.검정통계량 : %g" %t)

    v = len(x) - 1                  
    print("\n2.자유도 :",v)
    
    cr = df["%g" %a][int(v)]
    print("\n3.임계값 : {0}".format(-cr))
    print("\n4.기각역 : (-oo, {0})".format(-cr))
    
    z = sp.symbols('z')
    f = (math.gamma((v+1)/2)/(math.sqrt(v*math.pi)*math.gamma(v/2)))*((1+(z**2)/v)**(-(v+1)/2))
    if t >= 0 :
        TI = 0.5 + sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 - sp.Integral(f,(z,0,abs(t)))
    print("\n5.p값 : %g" %TI)
    print("\n6.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ### t-검정(모표준편차를 모를 때, 모집단 2개, 합동분산)
# - (t검정통계량)^2 = (F검정통계량) : 등분산임을 확인할 수 있음
# - 다르면, 이분산으로 검정해야 함

# #### 양측 t2검정 (등분산, 표)

# In[92]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 두 모평균이 같은지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르므로, t검정을 사용, 모집단 2개, 등분산 양측 기각역 검정 
# T2_Twosided_criticalregion_Equivariance 축약 : T2_TscrEqv

def T2_TscrEqv(a,x,y) :       

    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
   
    df = len(x) + len(y) - 2      
    psv = ((len(x) - 1)*Std(x)**2 + (len(y) - 1)*Std(y)**2)/df    
    T2 = (Mean(x) - Mean(y))/math.sqrt(psv*(1/len(x) + 1/len(y)))
    print("1.검정통계량: %g" %T2)
    print("\n2.자유도:", df)
    print("\n3.합동표본분산(합동추정치) : %g" %psv)
                                        
    cr = df1["%g" %(a/2)][int(df)]
    print("\n4.임계값 : {0}, {1}".format(-cr,cr))
    print("\n5.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))

    if cr < abs(T2):
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 t2검정 (등분산, p-value)

# In[93]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 두 모평균이 같은지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르므로, t검정을 사용, 모집단 2개, 등분산 양측 p값 검정 
# T2_Twosided_probabilityvalue_Equivariance 축약 : T2_TspEqv

def T2_TspEqv(a,x,y) :
    
    df = len(x) + len(y) - 2                  
    psv = ((len(x) - 1)*Std(x)**2 + (len(y) - 1)*Std(y)**2)/df            
    t = round((Mean(x) - Mean(y))/math.sqrt(((1/len(x)) + (1/len(y)))*psv),17)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    print("\n3.합동표본분산(합동추정치) : %g" %psv)
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    I = 0.5 - sp.Integral(f,(z,0,abs(t)))          
    print("\n4.p값 : %g" %(I*2))
    print("\n5.유의수준 : %g" %a)
    
    if I < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 t2검정 (등분산)

# In[94]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 두 모평균이 같은지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르므로, t검정을 사용, 모집단 2개, 등분산 양측검정 
# T2_Twosided_Equivariance 축약 : T2_TsEqv

def T2_TsEqv(a,x,y) :
     
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
     
    df = len(x) + len(y) - 2                  
    psv = ((len(x) - 1)*Std(x)**2 + (len(y) - 1)*Std(y)**2)/df            
    t = round((Mean(x) - Mean(y))/math.sqrt(((1/len(x)) + (1/len(y)))*psv),17)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    print("\n3.합동표본분산(합동추정치) : %g" %psv)
                                      
    cr = df1["%g" %(a/2)][int(df)]
    print("\n4.임계값 : {0}, {1}".format(-cr,cr))
    print("\n5.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    I = 0.5 - sp.Integral(f,(z,0,abs(t)))          
    print("\n6.p값 : %g" %(I*2))
    print("\n7.유의수준 : %g" %a)
    
    if I < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t2검정(위꼬리 검정) (등분산, 표)

# In[95]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 등분산 위꼬리검정 
# T2_Upsided_Equivariance 축약 : T2_UpEqv

def T2_UpcrEqv(a,x,y) :
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    df = len(x) + len(y) - 2                  
    psv = ((len(x) - 1)*Std(x)**2 + (len(y) - 1)*Std(y)**2)/df            
    t = (Mean(x) - Mean(y))/math.sqrt(((1/len(x)) + (1/len(y)))*psv)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    print("\n3.합동표본분산(합동추정치) : %g" %psv) 
    
    cr = df1["%g" %a][int(df)]
    print("\n4.임계값 : {0}".format(cr))
    print("\n5.기각역 : ({0}, oo)".format(cr))
    
    if cr < t :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ####  단측 t2검정(위꼬리 검정) (등분산, 함수)

# In[96]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 등분산 위꼬리 p값 검정 
# T2_Upsided_probabilityvalue_Equivariance 축약 : T2_UppEqv

def T2_UppEqv(a,x,y) :
    
    df = len(x) + len(y) - 2                  
    psv = ((len(x) - 1)*Std(x)**2 + (len(y) - 1)*Std(y)**2)/df            
    t = round((Mean(x) - Mean(y))/math.sqrt(((1/len(x)) + (1/len(y)))*psv),17)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    print("\n3.합동표본분산(합동추정치) : %g" %psv)
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    if t >= 0 :
        TI = 0.5 - sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 + sp.Integral(f,(z,0,abs(t)))           
    print("\n4.p값 : %g" %TI)
    print("\n5.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ####  단측 t2검정(위꼬리 검정) (등분산)

# In[97]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 등분산 위꼬리검정 
# T2_Upsided_Equivariance 축약 : T2_UpEqv

def T2_UpEqv(a,x,y) :
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    df = len(x) + len(y) - 2                  
    psv = ((len(x) - 1)*Std(x)**2 + (len(y) - 1)*Std(y)**2)/df            
    t = round((Mean(x) - Mean(y))/math.sqrt(((1/len(x)) + (1/len(y)))*psv),17)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    print("\n3.합동표본분산(합동추정치) : %g" %psv)
    
    cr = df1["%g" %a][int(df)]
    print("\n4.임계값 : {0}".format(cr))
    print("\n5.기각역 : ({0}, oo)".format(cr))
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    if t >= 0 :
        TI = 0.5 - sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 + sp.Integral(f,(z,0,abs(t)))           
    print("\n6.p값 : %g" %TI)
    print("\n7.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t2검정(아래꼬리 검정) (등분산, 표)

# In[98]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 작은지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 등분산 아래꼬리 기각역 검정 
# T2_Undersided_criticalregion_Equivariance 축약 : T2_UncrEqv

def T2_UncrEqv(a,x,y) :
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    df = len(x) + len(y) - 2                  
    psv = ((len(x) - 1)*Std(x)**2 + (len(y) - 1)*Std(y)**2)/df            
    t = (Mean(x) - Mean(y))/math.sqrt(((1/len(x)) + (1/len(y)))*psv)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    print("\n3.합동표본분산(합동추정치) : %g" %psv) 
    
    cr = df1["%g" %a][int(df)]
    print("\n4.임계값 : {0}".format(-cr))
    print("\n5.기각역 : (-oo, {0})".format(-cr))
    
    if t < -cr :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t2검정(아래꼬리 검정) (등분산, 함수)

# In[99]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 작은지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 등분산 아래꼬리 p값 검정 
# T2_Undersided_probabilityvalue_Equivariance 축약 : T2_UnpEqv

def T2_UnpEqv(a,x,y) :
    
    df = len(x) + len(y) - 2                 
    psv = ((len(x)-1)*Var(x) + (len(y)-1)*Var(y))/df            
    t = round((Mean(x) - Mean(y))/math.sqrt(((1/len(x)) + (1/len(y)))*psv),17)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    print("\n3.합동표본분산 : %g" %psv)

    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    if t >= 0 :
        TI = 0.5 + sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 - sp.Integral(f,(z,0,abs(t)))           
    print("\n4.p값 : %g" %TI)
    print("\n5.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t2검정(아래꼬리 검정) (등분산)

# In[100]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 작은지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 등분산 아래꼬리검정 
# T2_Undersided_Equivariance 축약 : T2_UnEqv

def T2_UnEqv(a,x,y) :
        
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    df = len(x) + len(y) - 2                 
    psv = ((len(x)-1)*Var(x) + (len(y)-1)*Var(y))/df            
    t = round((Mean(x) - Mean(y))/math.sqrt(((1/len(x)) + (1/len(y)))*psv),17)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    print("\n3.합동표본분산 : %g" %psv)

    cr = df1["%g" %a][int(df)]
    print("\n4.임계값 : {0}".format(-cr))
    print("\n5.기각역 : (-oo, {0})".format(-cr))
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    if t >= 0 :
        TI = 0.5 + sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 - sp.Integral(f,(z,0,abs(t)))           
    print("\n6.p값 : %g" %TI)
    print("\n7.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ### t-검정(모표준편차를 모를 때, 모집단 2개, 이분산)

# #### 양측 t2 검정 (표 : 기각역)

# In[101]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 두 모평균이 같은지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르므로, t검정을 사용, 모집단 2개, 이분산 양측 기각역 검정 
# T2_Twosided_criticalregion 축약 : T2_Tscr

def T2_Tscr(a,x,y) :
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    df = round((Std(x)**2/len(x) + Std(y)**2/len(y))**2/((Std(x)**2/len(x))**2/(len(x) - 1) + (Std(y)**2/len(y))**2/(len(y) - 1)))
    T2 = (Mean(x) - Mean(y))/math.sqrt(Std(x)**2/len(x) + Std(y)**2/len(y))
    print("1.검정통계량: %g" %T2)
    print("\n2.자유도:", df)
    
    cr = df1["%g" %(a/2)][int(df)]
    print("\n3.임계값 : {0}, {1}".format(-cr,cr))
    print("\n4.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))
    
    if cr < abs(T2):
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 t2검정 (함수 : p값)

# In[102]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 두 모평균이 같은지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르므로, t검정을 사용, 모집단 2개, 이분산 양측 p값 검정 
# T2_Twosided_probabilityvalue 축약 : T2_Tsp

def T2_Tsp(a,x,y) :
    df = round((Std(x)**2/len(x) + Std(y)**2/len(y))**2/((Std(x)**2/len(x))**2/(len(x) - 1) + (Std(y)**2/len(y))**2/(len(y) - 1)))   
    t = round((Mean(x) - Mean(y))/math.sqrt(Std(x)**2/len(x) + Std(y)**2/len(y)),17)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    I = 0.5 - sp.Integral(f,(z,0,abs(t)))
    print("\n3.p값 : %f" %(I*2))
    print("\n4.유의수준 : %g" %a)
    
    if I < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 t2검정

# In[103]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 두 모평균이 같은지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르므로, t검정을 사용, 모집단 2개, 이분산 양측검정 
# T2_Twosided 축약 : T2_Ts

def T2_Ts(a,x,y) :
     
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    df = round((Std(x)**2/len(x) + Std(y)**2/len(y))**2/((Std(x)**2/len(x))**2/(len(x) - 1) + (Std(y)**2/len(y))**2/(len(y) - 1)))      
    t = round((Mean(x) - Mean(y))/math.sqrt(Std(x)**2/len(x) + Std(y)**2/len(y)),17)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    
    cr = df1["%g" %(a/2)][int(df)]
    print("\n3.임계값 : {0}, {1}".format(-cr,cr))
    print("\n4.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    I = 0.5 - sp.Integral(f,(z,0,abs(t)))
    print("\n5.p값 : %f" %(I*2))
    print("\n6.유의수준 : %g" %a)
    
    if I < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t2검정(위꼬리 검정) (표)

# In[104]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 이분산 위꼬리 기각역 검정 
# T2_Upsided_criticalregion 축약 : T2_Upcr

def T2_Upcr(a,x,y) :
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    df = round((Std(x)**2/len(x) + Std(y)**2/len(y))**2/((Std(x)**2/len(x))**2/(len(x) - 1) + (Std(y)**2/len(y))**2/(len(y) - 1)))    
    T2 = (Mean(x) - Mean(y))/math.sqrt(Std(x)**2/len(x) + Std(y)**2/len(y))
    print("1.검정통계량 : %g" %T2)
    print("\n2.자유도 :", df)
    
    cr = df1["%g" %a][int(df)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    if cr < T2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t2검정(위꼬리 검정) (함수)

# In[105]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 이분산 위꼬리 p값 검정 
# T2_Upsided_probabilityvalue 축약 : T2_Upp

def T2_Upp(a,x,y) :
     
    df = round((Std(x)**2/len(x) + Std(y)**2/len(y))**2/((Std(x)**2/len(x))**2/(len(x) - 1) + (Std(y)**2/len(y))**2/(len(y) - 1)))    
    t = round((Mean(x) - Mean(y))/math.sqrt(Std(x)**2/len(x) + Std(y)**2/len(y)),17)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    if t >= 0 :
        TI = 0.5 - sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 + sp.Integral(f,(z,0,abs(t)))         
    print("\n3.p값 : %f" %TI)
    print("\n4.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t2검정(위꼬리 검정)

# In[106]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 이분산 위꼬리검정 
# T2_Upsided 축약 : T2_Up

def T2_Up(a,x,y) :
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
     
    df = round((Std(x)**2/len(x) + Std(y)**2/len(y))**2/((Std(x)**2/len(x))**2/(len(x) - 1) + (Std(y)**2/len(y))**2/(len(y) - 1))) 
    t = round((Mean(x) - Mean(y))/math.sqrt(Std(x)**2/len(x) + Std(y)**2/len(y)),17)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    
    cr = df1["%g" %a][int(df)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    if t >= 0 :
        TI = 0.5 - sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 + sp.Integral(f,(z,0,abs(t)))         
    print("\n5.p값 : %f" %TI)
    print("\n6.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t2검정(아래꼬리 검정) (표)

# In[107]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 작은지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 이분산 아래꼬리 기각역 검정 
# T2_Undersided_criticalregion 축약 : T2_Uncr

def T2_Uncr(a,x,y) :
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    df = round((Std(x)**2/len(x) + Std(y)**2/len(y))**2/((Std(x)**2/len(x))**2/(len(x) - 1) + (Std(y)**2/len(y))**2/(len(y) - 1))) 
    t = round((Mean(x) - Mean(y))/math.sqrt(Std(x)**2/len(x) + Std(y)**2/len(y)),17) 
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :",df)
    
    cr = df1["%g" %a][int(df)]
    print("\n3.임계값 : {0}".format(-cr))
    print("\n4.기각역 : (-oo, {0})".format(-cr))
    
    if t < -cr :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t2검정(아래꼬리 검정) (함수)

# In[108]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 이분산 아래꼬리 p값 검정 
# T2_Undersided_probabilityvalue 축약 : T2_Unp

def T2_Unp(a,x,y) :
    
    df = round((Std(x)**2/len(x) + Std(y)**2/len(y))**2/((Std(x)**2/len(x))**2/(len(x) - 1) + (Std(y)**2/len(y))**2/(len(y) - 1))) 
    t = round((Mean(x) - Mean(y))/math.sqrt(Std(x)**2/len(x) + Std(y)**2/len(y)),17)  
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z^2)/df)^(-(df + 1)/2))  
    if t >= 0 :
        TI = 0.5 + sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 - sp.Integral(f,(z,0,abs(t)))          
    print("\n3.p값 : %f" %TI)
    print("\n4.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 t2검정(아래꼬리 검정)

# In[109]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모평균이 y의 모평균보다 큰지 확인, 두 모표준편차를 모르는 경우
# 모표준편차를 모르는 경우이므로, t검정을 사용, 모집단 2개, 이분산 아래꼬리검정 
# T2_Undersided 축약 : T2_Un

def T2_Un(a,x,y) :
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    df = round((Std(x)**2/len(x) + Std(y)**2/len(y))**2 / ((Std(x)**2/len(x))**2 / (len(x) - 1) + (Std(y)**2/len(y))**2 / (len(y) - 1)))      
    t = round((Mean(x) - Mean(y))/math.sqrt(Std(x)**2/len(x) + Std(y)**2/len(y)),17)     
    print("1.검정통계량 : %g" %t)
    print("\n2.자유도 :", df)
     
    cr = df1["%g" %a][int(df)]
    print("\n3.임계값 : {0}".format(-cr))
    print("\n4.기각역 : (-oo, {0})".format(-cr))
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    if t >= 0 :
        TI = 0.5 + sp.Integral(f,(z,0,t))
    else : 
        TI = 0.5 - sp.Integral(f,(z,0,abs(t)))          
    print("\n5.p값 : %f" %TI)
    print("\n6.유의수준 : %g" %a)
    
    if TI < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ### 짝관측 (표본이 독립이 아닌 경우, 모집단 2개, 평균 비교)

# #### 양쪽꼬리검정 (기각역)

# In[110]:


# 유의수준 'a' 로 두 자료 'x1, x2'의 새로운 단일변수 xd에 대한 모평균 0인지 확인, 두 자료가 독립적이지 않은 경우
# 짝관측은 t검정을 사용, 독립적이지 않은 모집단 2개, 양측 기각역 검정 
# Paired_Twosided_criticalregion 축약 : Paired_Tscr

def Paired_Tscr(a,x1,x2) :  
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    d = list(map(lambda x1, x2 : x1 - x2 , x1, x2))
    T = Mean(d) / (Std(d)/math.sqrt(len(d)))
    print("1.검정통계량 : %g" %T)     
    print("\n2.자유도 :", len(d) - 1)
    
    cr = df1["%g" %(a/2)][int(len(d) - 1)]
    print("\n3.임계값 : {0}, {1}".format(-cr,cr))
    print("\n4.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))
    
    if cr < abs(T) :         
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 짝양쪽꼬리검정 (p값)

# In[111]:


# 유의수준 'a' 로 두 자료 'x1, x2'의 새로운 단일변수 xd에 대한 모평균 0인지 확인, 두 자료가 독립적이지 않은 경우
# 짝관측은 t검정을 사용, 독립적이지 않은 모집단 2개, 양측 p값 검정 
# Paired_Twosided_probabilityvalue 축약 : Paired_Tsp

def Paired_Tsp(a,x1,x2) :  
    
    d = list(map(lambda x1, x2 : x1 - x2 , x1, x2))
    df = len(d) - 1
    t = round(Mean(d) / (Std(d)/math.sqrt(len(d))),17)
    print("1.검정통계량 : %g" %t)     
    print("\n2.자유도 :", df)
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    I = 0.5 - sp.Integral(f,(z,0,abs(t)))
    print("\n3.p값 : %f" %(I*2))
    print("\n4.유의수준 : %g" %a)
    
    if I < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 짝양쪽꼬리검정

# In[112]:


# 유의수준 'a' 로 두 자료 'x1, x2'의 새로운 단일변수 xd에 대한 모평균 0인지 확인, 두 자료가 독립적이지 않은 경우
# 짝관측은 t검정을 사용, 독립적이지 않은 모집단 2개, 양측검정 
# Paired_Twosided 축약 : Paired_Ts

def Paired_Ts(a,x1,x2) :  
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    d = list(map(lambda x1, x2 : x1 - x2 , x1, x2))
    df = len(d) - 1
    t = round(Mean(d) / (Std(d)/math.sqrt(len(d))),17)
    print("1.검정통계량 : %g" %t)     
    print("\n2.자유도 :", df)
    
    cr = df1["%g" %(a/2)][int(df)]
    print("\n3.임계값 : {0}, {1}".format(-cr,cr))
    print("\n4.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))  
    I = 0.5 - sp.Integral(f,(z,0,abs(t)))
    print("\n5.p값 : %f" %(I*2))
    print("\n6.유의수준 : %g" %a)
    
    if I < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 왼쪽꼬리검정 (기각역)

# In[113]:


# 유의수준 'a' 로 두 자료 'x1, x2'의 새로운 단일변수 xd에 대한 모평균 0인지 확인, 두 자료가 독립적이지 않은 경우
# 짝관측은 t검정을 사용, 독립적이지 않은 모집단 2개, 좌측 기각역 검정 
# Paired_Leftsided_criticalregion 축약 : Paired_Lcr

def Paired_Lcr(a,x1,x2) : 
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    d = list(map(lambda x1, x2 : x1 - x2 , x1, x2))
    T = Mean(d) / (Std(d)/math.sqrt(len(d)))
    print("1.검정통계량 : %g" %T)     
    print("\n2.자유도 :", len(d) - 1)
    
    cr = df1["%g" %a][int(len(d) - 1)]
    print("\n3.임계값 : {0}".format(-cr))
    print("\n4.기각역 : (-oo, {0})".format(-cr))
    
    if T < -cr :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 짝왼쪽꼬리검정 (p값)

# In[114]:


# 유의수준 'a' 로 두 자료 'x1, x2'의 새로운 단일변수 xd에 대한 모평균 0인지 확인, 두 자료가 독립적이지 않은 경우
# 짝관측은 t검정을 사용, 독립적이지 않은 모집단 2개, 좌측 p값 검정 
# Paired_Leftsided_probabilityvalue 축약 : Paired_Lp

def Paired_Lp(a,x1,x2) :  
    
    d = list(map(lambda x1, x2 : x1 - x2 , x1, x2))
    df = len(d) - 1
    t = round(Mean(d) / (Std(d)/math.sqrt(len(d))),17)
    print("1.검정통계량 : %g" %t)     
    print("\n2.자유도 :", df)
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))
    if t >= 0 :
        I = 0.5 + sp.Integral(f,(z,0,t))
    else : 
        I = 0.5 - sp.Integral(f,(z,0,abs(t)))          
    print("\n3.p값 : %f" %I)
    print("\n4.유의수준 : %g" %a)
    
    if I < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 짝왼쪽꼬리검정

# In[115]:


# 유의수준 'a' 로 두 자료 'x1, x2'의 새로운 단일변수 xd에 대한 모평균 0인지 확인, 두 자료가 독립적이지 않은 경우
# 짝관측은 t검정을 사용, 독립적이지 않은 모집단 2개, 좌측검정 
# Paired_Leftsided 축약 : Paired_L

def Paired_L(a,x1,x2) :  
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    d = list(map(lambda x1, x2 : x1 - x2 , x1, x2))
    df = len(d) - 1
    t = round(Mean(d) / (Std(d)/math.sqrt(len(d))),17)
    print("1.검정통계량 : %g" %t)     
    print("\n2.자유도 :", df)
    
    cr = df1["%g" %a][int(df)]
    print("\n3.임계값 : {0}".format(-cr))
    print("\n4.기각역 : (-oo, {0})".format(-cr))
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))
    if t >= 0 :
        I = 0.5 + sp.Integral(f,(z,0,t))
    else : 
        I = 0.5 - sp.Integral(f,(z,0,abs(t)))          
    print("\n5.p값 : %f" %I)
    print("\n6.유의수준 : %g" %a)
    
    if I < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 오른쪽꼬리검정

# In[116]:


# 유의수준 'a' 로 두 자료 'x1, x2'의 새로운 단일변수 xd에 대한 모평균 0인지 확인, 두 자료가 독립적이지 않은 경우
# 짝관측은 t검정을 사용, 독립적이지 않은 모집단 2개, 우측 기각역 검정 
# Paired_Rightsided_criticalregion 축약 : Paired_Rcr

def Paired_Rcr(a,x1,x2) : 

    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    d = list(map(lambda x1, x2 : x1 - x2 , x1, x2))
    T = Mean(d) / (Std(d)/math.sqrt(len(d)))
    print("1.검정통계량 : %g" %T)   
    print("\n2.자유도 :", len(d) - 1)
    
    cr = df1["%g" %a][int(len(d) - 1)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    if cr < T :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 짝오른쪽꼬리검정 (p값)

# In[117]:


# 유의수준 'a' 로 두 자료 'x1, x2'의 새로운 단일변수 xd에 대한 모평균 0인지 확인, 두 자료가 독립적이지 않은 경우
# 짝관측은 t검정을 사용, 독립적이지 않은 모집단 2개, 우측 p값 검정 
# Paired_Rightsided_probabilityvalue 축약 : Paired_Rp

def Paired_Rp(a,x1,x2) :  
    
    d = list(map(lambda x1, x2 : x1 - x2 , x1, x2))
    df = len(d) - 1
    t = round(Mean(d) / (Std(d)/math.sqrt(len(d))),17)
    print("1.검정통계량 : %g" %t)     
    print("\n2.자유도 :", df)
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))
    if t >= 0 :
        I = 0.5 - sp.Integral(f,(z,0,t))
    else : 
        I = 0.5 + sp.Integral(f,(z,0,abs(t)))          
    print("\n3.p값 : %f" %I)
    print("\n4.유의수준 : %g" %a)
    
    if I < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 짝오른쪽꼬리검정

# In[118]:


# 유의수준 'a' 로 두 자료 'x1, x2'의 새로운 단일변수 xd에 대한 모평균 0인지 확인, 두 자료가 독립적이지 않은 경우
# 짝관측은 t검정을 사용, 독립적이지 않은 모집단 2개, 우측검정 
# Paired_Rightsided 축약 : Paired_R

def Paired_R(a,x1,x2) :  
    
    df1 = pd.read_csv('./t분포표.csv',encoding='euc-kr',index_col=0)
    
    d = list(map(lambda x1, x2 : x1 - x2 , x1, x2))
    df = len(d) - 1
    t = round(Mean(d) / (Std(d)/math.sqrt(len(d))),17)
    print("1.검정통계량 : %g" %t)     
    print("\n2.자유도 :", df)
     
    cr = df1["%g" %a][int(df)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    z = sp.symbols('z')
    f = (math.gamma((df + 1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))
    if t >= 0 :
        I = 0.5 - sp.Integral(f,(z,0,t))
    else : 
        I = 0.5 + sp.Integral(f,(z,0,abs(t)))          
    print("\n5.p값 : %f" %I)
    print("\n6.유의수준 : %g" %a)
    
    if I < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ---
# ---

# ### 모비율 p에 대한 검정(비정규분포 모집단, 대표본근사, 모집단 1개)

# - 대표본근사를 통한 Z검정
# - 모비율에 대한 가설검정은 표본비율 p와 가설의 비율(모비율) p0 사이에 얼마나 차이가 있느냐에 따름.
# - 표본의 크기가 충분히 클 때, 즉 np0>=5와 n(1-p0)>=5를 만족할 때 p의 근사 분포를 다룸.

# #### 양측 모비율검정 (함수 : p값과 유의수준)

# In[119]:


# 모집단 1개, 표본비율 'x/n'와 가설비율(모비율) 'p0' 사이에 차이가 있는지 없는지 확인 (양측검정)
# 'a': 유의수준, 'n': 전체 대상 수, 'x': 해당 대상 수, 'p0': 가설비율
def P1_Ts(a,n,x,p0):
    p = x/n
    if n * p0 >=5 and n * (1-p0) >=5:
        Z = round((p - p0) / math.sqrt(p0*(1 - p0)/n),17)
        print("1.검정통계량 : %g" %Z)
        
        y, z = sp.symbols('y z') 
        f = 1 / sp.sqrt(2 * sp.pi) * sp.exp(-(z ** 2) / 2)
        I = sp.integrate(f,(z,0,y))
        eqn = sp.Eq(I, 0.5 - a/2)
        cr = round(sp.solve( eqn, y )[0],3)
        print("\n2.임계값 : {0}, {1}".format(-cr,cr))
        print("\n3.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))

        I2 = (0.5 - sp.Integral(f,(z,0,abs(Z))))*2             
        print("\n4.p값 : %g" %I2) 
        print("\n5.유의수준 : %g" %a)

        if cr < abs(Z) :
            ans = "[결과] : 귀무가설을 기각한다."
        else :
            ans = "[결과] : 귀무가설을 기각하지 못한다."

    else:
        ans = "대표본 근사의 조건을 만족하지 못하는 경우이다."
    
    return ans


# #### 양측 모비율검정 (표: 검정통계량과 기각역)

# In[120]:


# 모집단 1개, 표본비율 'x/n'와 가설비율(모비율) 'p0' 사이에 차이가 있는지 없는지 확인 (양측검정)
# 'a': 유의수준, 'n': 전체 대상 수, 'x': 해당 대상 수, 'p0': 가설비율
def P1_Tscr(a,n,x,p0):
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    
    p = x/n
    if n * p0 >=5 and n * (1-p0) >=5:
        Z = round((p - p0) / math.sqrt(p0*(1 - p0)/n),17)
        print("1.검정통계량 : %g" %Z)
        
        z = sp.symbols('z') 
        f = 1 / sp.sqrt(2 * sp.pi) * sp.exp(-(z ** 2) / 2)
        cr = two_tailed_pred_interval_p(a)
        print("\n2.임계값 : {0}, {1}".format(-cr,cr))
        print("\n3.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))

        I2 = (0.5 - sp.Integral(f,(z,0,abs(Z))))*2             
        print("\n4.p값 : %g" %I2) 
        print("\n5.유의수준 : %g" %a)

        if cr < abs(Z) :
            ans = "[결과] : 귀무가설을 기각한다."
        else :
            ans = "[결과] : 귀무가설을 기각하지 못한다."

    else:
        ans = "대표본 근사의 조건을 만족하지 못하는 경우이다."
    
    return ans


# #### 단측 모비율검정 (위 꼬리 단측검정, 함수 : p값과 유의수준)

# In[121]:


# 모집단 1개, 표본비율 'x/n'이 가설비율(모비율) 'p0'보다 큰지 확인 (위 꼬리 단측검정)
# 'a': 유의수준, 'n': 전체 대상 수, 'x': 해당 대상 수, 'p0': 가설비율
def P1_Up(a,n,x,p0):
    p = x/n
    if n * p0 >=5 and n * (1-p0) >=5:
        Z = round((p - p0) / math.sqrt(p0*(1 - p0)/n),17)
        print("1.검정통계량 : %g" %Z)
        
        y, z = sp.symbols('y z') 
        f = 1/sp.sqrt(2*sp.pi)*sp.exp(-(z**2)/2)
        I = sp.integrate(f,(z,0,y))
        eqn = sp.Eq(I, 0.5 - a)
        cr = round(sp.solve( eqn, y )[0],3)
        print("\n2.임계값 : {0}".format(cr))
        print("\n3.기각역 : ({0}, oo)".format(cr)) 

        if Z >= 0 :
            I2 = 0.5 - sp.Integral(f,(z,0,Z))
        else :
            I2 = 0.5 + sp.Integral(f,(z,0,abs(Z)))
        print("\n4.p값 : %g" %I2) 
        print("\n5.유의수준 : %g" %a)

        if cr < Z :
            ans = "[결과] : 귀무가설을 기각한다."
        else :
            ans = "[결과] : 귀무가설을 기각하지 못한다."

    else:
        ans = "대표본 근사의 조건을 만족하지 못하는 경우이다."
    
    return ans


# #### 단측 모비율검정 (위 꼬리 단측검정, 표 : 검정통계량과 기각역)

# In[122]:


# 모집단 1개, 표본비율 'x/n'이 가설비율(모비율) 'p0'보다 큰지 확인 (위 꼬리 단측검정)
# 'a': 유의수준, 'n': 전체 대상 수, 'x': 해당 대상 수, 'p0': 가설비율
def P1_Upcr(a,n,x,p0):
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    p = x/n
    if n * p0 >=5 and n * (1-p0) >=5:
        Z = round((p - p0) / math.sqrt(p0*(1 - p0)/n),17)
        print("1.검정통계량 : %g" %Z)
        
        z = sp.symbols('z') 
        f = 1/sp.sqrt(2*sp.pi)*sp.exp(-(z**2)/2)
        cr = one_tailed_pred_interval_p(a)
        print("\n2.임계값 : {0}".format(cr))
        print("\n3.기각역 : ({0}, oo)".format(cr)) 

        if Z >= 0 :
            I2 = 0.5 - sp.Integral(f,(z,0,Z))
        else :
            I2 = 0.5 + sp.Integral(f,(z,0,abs(Z)))
        print("\n4.p값 : %g" %I2) 
        print("\n5.유의수준 : %g" %a)

        if cr < Z :
            ans = "[결과] : 귀무가설을 기각한다."
        else :
            ans = "[결과] : 귀무가설을 기각하지 못한다."

    else:
        ans = "대표본 근사의 조건을 만족하지 못하는 경우이다."
    
    return ans


# #### 단측 모비율검정 (아래 꼬리 단측검정, 함수 : p값과 유의수준)

# In[123]:


# 모집단 1개, 표본비율 'x/n'이 가설비율(모비율) 'p0'보다 작은지 확인 (아래 꼬리 단측검정)
# 'a': 유의수준, 'n': 전체 대상 수, 'x': 해당 대상 수, 'p0': 가설비율
def P1_Un(a,n,x,p0):
    p = x/n
    if n * p0 >=5 and n * (1-p0) >=5:
        Z = round((p - p0) / math.sqrt(p0*(1 - p0)/n),17)
        print("1.검정통계량 : %g" %Z)
        
        y, z = sp.symbols('y z') 
        f = 1/sp.sqrt(2*sp.pi)*sp.exp(-(z**2)/2)
        I = sp.integrate(f,(z,0,y))
        eqn = sp.Eq(I, 0.5 - a)
        cr = round(sp.solve( eqn, y )[0],3)
        print("\n2.임계값 : {0}".format(-cr))
        print("\n3.기각역 : (-oo, {0})".format(-cr))

        if Z >= 0 :
            I2 = 0.5 + sp.Integral(f,(z,0,Z))
        else :
            I2 = 0.5 - sp.Integral(f,(z,0,abs(Z)))
        print("\n4.p값 : %g" %I2)
        print("\n5.유의수준 : %g" %a)

        if Z < -cr :
            ans = "[결과] : 귀무가설을 기각한다."
        else :
            ans = "[결과] : 귀무가설을 기각하지 못한다."

    else:
        ans = "대표본 근사의 조건을 만족하지 못하는 경우이다."
    
    return ans


# #### 단측 모비율검정 (아래 꼬리 단측검정, 표 : 검정통계량과 기각역)

# In[124]:


# 모집단 1개, 표본비율 'x/n'이 가설비율(모비율) 'p0'보다 작은지 확인 (아래 꼬리 단측검정)
# 'a': 유의수준, 'n': 전체 대상 수, 'x': 해당 대상 수, 'p0': 가설비율
def P1_Uncr(a,n,x,p0):
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    p = x/n
    if n * p0 >=5 and n * (1-p0) >=5:
        Z = round((p - p0) / math.sqrt(p0*(1 - p0)/n),17)
        print("1.검정통계량 : %g" %Z)
        
        z = sp.symbols('z') 
        f = 1/sp.sqrt(2*sp.pi)*sp.exp(-(z**2)/2)
        cr = one_tailed_pred_interval_p(a)
        print("\n2.임계값 : {0}".format(-cr))
        print("\n3.기각역 : (-oo, {0})".format(-cr))

        if Z >= 0 :
            I2 = 0.5 + sp.Integral(f,(z,0,Z))
        else :
            I2 = 0.5 - sp.Integral(f,(z,0,abs(Z)))
        print("\n4.p값 : %g" %I2)
        print("\n5.유의수준 : %g" %a)

        if Z < -cr :
            ans = "[결과] : 귀무가설을 기각한다."
        else :
            ans = "[결과] : 귀무가설을 기각하지 못한다."

    else:
        ans = "대표본 근사의 조건을 만족하지 못하는 경우이다."
    
    return ans


# ### 두 집단 모비율의 차이에 대한 추론
# - 모비율 차이의 추정량 p1-p2의 분포는 대표본인 경우 근사적으로 정규분포를 따름
# - 조건: n1p1, n1(1-p1), n2p2, n2(1-p2) >= 5

# #### 양측 두 집단 모비율 검정 (함수: p값과 유의수준)

# In[125]:


# 모집단 2개, 두 집단 모비율이 같은지 확인 (양측검정)
# 'a': 유의수준, 'nx': 첫번째 전체 대상 수, 'x': 해당 대상 수, 'ny': 두번째 전체 대상 수, 'y': 해당 대상 수, 
def P2_Ts(a,nx,x,ny,y):
    p1 = x / nx
    p2 = y / ny
    p = (x + y) / (nx + ny) #공통 모비율의 추정값 
    Z = round((p1 - p2) / math.sqrt(p*(1-p)*(1/nx + 1/ny)),17)
    print("1.검정통계량 : %g" %Z)  
    
    w, z = sp.symbols('w z') 
    f = 1/sp.sqrt(2*sp.pi)*sp.exp(-(z**2)/2)
    I = sp.integrate(f,(z,0,w))
    eqn = sp.Eq(I, 0.5 - a/2)
    cr = round(sp.solve( eqn, w )[0],3)
    print("\n2.임계값 : {0}, {1}".format(-cr, cr))
    print("\n3.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr, cr))
    
    I2 = (0.5 - sp.Integral(f,(z,0,abs(Z))))*2
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
    
    if cr < abs(Z) :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 두 집단 모비율 검정 (표 : 검정통계량과 기각역)

# In[126]:


# 모집단 2개, 두 집단 모비율이 같은지 확인 (양측검정)
# 'a': 유의수준, 'nx': 첫번째 전체 대상 수, 'x': 해당 대상 수, 'ny': 두번째 전체 대상 수, 'y': 해당 대상 수, 
def P2_Tscr(a,nx,x,ny,y):
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    p1 = x / nx
    p2 = y / ny
    p = (x + y) / (nx + ny) #공통 모비율의 추정값 
    Z = round((p1 - p2) / math.sqrt(p*(1-p)*(1/nx + 1/ny)),17)
    print("1.검정통계량 : %g" %Z)  
    
    z = sp.symbols('z') 
    f = 1/sp.sqrt(2*sp.pi)*sp.exp(-(z**2)/2)
    cr = two_tailed_pred_interval_p(a)
    print("\n2.임계값 : {0}, {1}".format(-cr, cr))
    print("\n3.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr, cr))
    
    I2 = (0.5 - sp.Integral(f,(z,0,abs(Z))))*2
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
    
    if cr < abs(Z) :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 두 집단 모비율 검정 (위 꼬리 단측검정, 함수: p값과 유의수준)

# In[127]:


# 모집단 2개, 첫번째 집단 모비율이 두번째 집단 모비율보다 큰지 확인 (위 꼬리 단측검정)
# 'a': 유의수준, 'nx': 첫번째 전체 대상 수, 'x': 해당 대상 수, 'ny': 두번째 전체 대상 수, 'y': 해당 대상 수, 
def P2_Up(a,nx,x,ny,y):
    p1 = x / nx
    p2 = y / ny
    p = (x + y) / (nx + ny) #공통 모비율의 추정값 
    Z = round((p1 - p2) / math.sqrt(p*(1-p)*(1/nx + 1/ny)),17)
    print("1.검정통계량 : %g" %Z)  
    
    w, z = sp.symbols('w z') 
    f = 1/sp.sqrt(2*sp.pi)*sp.exp(-(z**2)/2)
    I = sp.integrate(f,(z,0,w)) 
    eqn = sp.Eq(I, 0.5 - a)
    cr = round(sp.solve( eqn, w )[0], 3)
    print("\n2.임계값 : {0}".format(cr))
    print("\n3.기각역 : ({0}, oo)".format(cr))
    
    if Z >= 0 :
        I2 = 0.5 - sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 + sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
   
    if cr < Z :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 두 집단 모비율 검정 (위 꼬리 단측검정, 표 : 검정통계량과 기각역)

# In[128]:


# 모집단 2개, 첫번째 집단 모비율이 두번째 집단 모비율보다 큰지 확인 (위 꼬리 단측검정)
# 'a': 유의수준, 'nx': 첫번째 전체 대상 수, 'x': 해당 대상 수, 'ny': 두번째 전체 대상 수, 'y': 해당 대상 수, 
def P2_Upcr(a,nx,x,ny,y):
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    p1 = x / nx
    p2 = y / ny
    p = (x + y) / (nx + ny) #공통 모비율의 추정값 
    Z = round((p1 - p2) / math.sqrt(p*(1-p)*(1/nx + 1/ny)),17)
    print("1.검정통계량 : %g" %Z)  
    
    z = sp.symbols('z') 
    f = 1/sp.sqrt(2*sp.pi)*sp.exp(-(z**2)/2)
    cr = one_tailed_pred_interval_p(a)
    print("\n2.임계값 : {0}".format(cr))
    print("\n3.기각역 : ({0}, oo)".format(cr))
    
    if Z >= 0 :
        I2 = 0.5 - sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 + sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2) 
    print("\n5.유의수준 : %g" %a)
   
    if cr < Z :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 두 집단 모비율 검정 (아래 꼬리 단측검정, 함수: p값과 유의수준)

# In[129]:


# 모집단 2개, 첫번째 집단 모비율이 두번째 집단 모비율보다 작은지 확인 (아래 꼬리 단측검정)
# 'a': 유의수준, 'nx': 첫번째 전체 대상 수, 'x': 해당 대상 수, 'ny': 두번째 전체 대상 수, 'y': 해당 대상 수, 
def P2_Un(a,nx,x,ny,y):
    p1 = x / nx
    p2 = y / ny
    p = (x + y) / (nx + ny) #공통 모비율의 추정값 
    Z = round((p1 - p2) / math.sqrt(p*(1-p)*(1/nx + 1/ny)),17)
    print("1.검정통계량 : %g" %Z)  
    
    w, z = sp.symbols('w z') 
    f = 1/sp.sqrt(2*sp.pi)*sp.exp(-(z**2)/2)
    I = sp.integrate(f,(z,0,w))
    eqn = sp.Eq(I, 0.5 - a)
    cr = round(sp.solve( eqn, w)[0],3)
    print("\n2.임계값 : {0}".format(-cr))
    print("\n3.기각역 : (-oo, {0})".format(-cr))
    
    if Z >= 0 :
        I2 = 0.5 + sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 - sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2)
    print("\n5.유의수준 : %g" %a)
    
    if Z < -cr :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 단측 두 집단 모비율 검정 (아래 꼬리 단측검정, 표 : 검정통계량과 기각역)

# In[130]:


# 모집단 2개, 첫번째 집단 모비율이 두번째 집단 모비율보다 작은지 확인 (아래 꼬리 단측검정)
# 'a': 유의수준, 'nx': 첫번째 전체 대상 수, 'x': 해당 대상 수, 'ny': 두번째 전체 대상 수, 'y': 해당 대상 수, 
def P2_Uncr(a,nx,x,ny,y):
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    p1 = x / nx
    p2 = y / ny
    p = (x + y) / (nx + ny) #공통 모비율의 추정값 
    Z = round((p1 - p2) / math.sqrt(p*(1-p)*(1/nx + 1/ny)),17)
    print("1.검정통계량 : %g" %Z)  
    
    z = sp.symbols('z') 
    f = 1/sp.sqrt(2*sp.pi)*sp.exp(-(z**2)/2)
    cr = one_tailed_pred_interval_p(a)
    print("\n2.임계값 : {0}".format(-cr))
    print("\n3.기각역 : (-oo, {0})".format(-cr))
    
    if Z >= 0 :
        I2 = 0.5 + sp.Integral(f,(z,0,Z))
    else :
        I2 = 0.5 - sp.Integral(f,(z,0,abs(Z)))
    print("\n4.p값 : %g" %I2)
    print("\n5.유의수준 : %g" %a)
    
    if Z < -cr :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ---
# ---

# ## 모분산에 대한 추론

# ### 카이제곱 검정통계량을 이용한 한 모집단의 모분산에 대한 추론 검정
# 
# #### 앞으로 목적에 따라 카이제곱이나 F분포표를 이용한 검정을 많이 할 예정이라 F, t, 카이제곱 검정통계량을 이용함. <br/>  F검정, t검정,카이제곱검정이라고 부르기 보다는 어떤 통계량을 가지고 목적에 따라 어떤 것을 검정하는지 구분지어 모듈명을 정함.

# #### 양측 분산추론 검정 (기각역)

# In[131]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모분산이 'v'인지 확인 -> Var
# 모표준편차 's' 를 기준으로 하고 싶으면, 'v' 자리에 's^2'을 넣으면 됨.  
# 카이제곱검정을 사용하여 모분산 확인, 모집단 1개, 양측 기각역 검정 
# Chi_Variance_Twosided_criticalregion 축약 : ChiVar_Tscr

def ChiVar_Tscr(a,x,v) :            

    df = pd.read_csv('./chi.csv',encoding='euc-kr',index_col=0) 
    
    chi = (len(x) - 1)*Std(x)^2/v    
    print("1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", len(x) - 1)
    
    cr1 = df["%g" %(1 - a/2)][int(len(x) - 1)]
    cr2 = df["%g" %(a/2)][int(len(x) - 1)]
    print("\n3.임계값 : {0}, {1}".format(cr1, cr2))
    print("\n4.기각역 : (0, {0}) or ({1}, oo)".format(cr1, cr2))
    
    if chi < cr1 or cr2 < chi :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 분산추론 검정 (함수)

# In[132]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모분산이 'v'인지 확인 -> Var
# 모표준편차 's' 를 기준으로 하고 싶으면, 'v' 자리에 's^2'을 넣으면 됨.  
# 카이제곱검정을 사용하여 모분산 확인, 모집단 1개, 양측 p값 검정 
# Chi_Variance_Twosided_probabilityvalue 축약 : ChiVar_Tsp

def ChiVar_Tsp(a,x,v) :     
    
    k = len(x) - 1
    chi = round(k*Std(x)^2/v,17)    
    print("1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", k)
    
    z = sp.symbols('z')
    C = (z^(k/2 - 1))*(math.e**(-z/2))/((2**(k/2))*gamma(k/2))  # 카이제곱 분포 함수
    I = sp.Integral(C,(z,0,chi))    
    MI = min(I, 1 - I)
    print("\n3.p값 : %g" %(MI*2))     # 검정통계량을 기준으로 좌/우 면적 중 작은 것의 (양측이므로 2배)  
    print("\n4.유의수준 : %g" %a)  
    
    if MI < a/2 :          # 작은 쪽만 유의수준과 비교하면 기각역 범위 안에 들어가는지 확인 가능
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 분산추론 검정

# In[133]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모분산이 'v'인지 확인 -> Var
# 모표준편차 's' 를 기준으로 하고 싶으면, 'v' 자리에 's^2'을 넣으면 됨.  
# 카이제곱검정을 사용하여 모분산 확인, 모집단 1개, 양측검정 
# Chi_Variance_Twosided 축약 : ChiVar_Ts

def ChiVar_Ts(a,x,v) :     
    
    df = pd.read_csv('./chi.csv',encoding='euc-kr',index_col=0) 
    
    k = len(x) - 1
    chi = round(k*Std(x)^2/v,17)    
    print("1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", k)
     
    cr1 = df["%g" %(1 - a/2)][int(k)]
    cr2 = df["%g" %(a/2)][int(k)]
    print("\n3.임계값 : {0}, {1}".format(cr1, cr2))
    print("\n4.기각역 : (0, {0}) or ({1}, oo)".format(cr1, cr2))
    
    z = sp.symbols('z')
    C = (z^(k/2 - 1))*(e^(-z/2))/((2^(k/2))*gamma(k/2))  # 카이제곱 분포 함수
    I = sp.Integral(C,(z,0,chi))    
    MI = min(I, 1 - I)
    print("\n5.p값 : %g" %(MI*2))     # 검정통계량을 기준으로 좌/우 면적 중 작은 것의 (양측이므로 2배)  
    print("\n6.유의수준 : %g" %a)  
    
    if MI < a/2 :          # 작은 쪽만 유의수준과 비교하면 기각역 범위 안에 들어가는지 확인 가능
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 우측 분산추론 검정 (표)

# In[134]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모분산이 'v'인지 확인 -> Var
# 모표준편차 's' 를 기준으로 하고 싶으면, 'v' 자리에 's^2'을 넣으면 됨.  
# 카이제곱검정을 사용하여 모분산 확인, 모집단 1개, 우측 기각역 검정 
# Chi_Variance_Rightsided_criticalregion 축약 : ChiVar_Rcr

def ChiVar_Rcr(a,x,v) :
    
    df = pd.read_csv('./chi.csv',encoding='euc-kr',index_col=0) 
      
    chi = (len(x) - 1)*Std(x)^2/v    
    print("1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", len(x) - 1)
    
    cr = df["%g" %a][int(len(x) - 1)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    if cr < chi :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 우측 분산추론 검정 (함수)

# In[135]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모분산이 'v'인지 확인 -> Var
# 모표준편차 's' 를 기준으로 하고 싶으면, 'v' 자리에 's^2'을 넣으면 됨.  
# 카이제곱검정을 사용하여 모분산 확인, 모집단 1개, 우측 p값 검정 
# Chi_Variance_Rightsided_probabilityvalue 축약 : ChiVar_Rp

def ChiVar_Rp(a,x,v) :
    
    k = len(x) - 1
    chi = round(k*Std(x)^2/v,17)    
    print("1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", k)
    
    z = sp.symbols('z')
    C = (z^(k/2 - 1))*(e^(-z/2))/((2^(k/2))*gamma(k/2))     # 카이제곱 분포 함수
    I = 1 - sp.Integral(C,(z,0,chi))       # 검정통계량의 넓이 (비율 p) 바로 구함
    print("\n3.p값 : %g" %I)         # 검정통계량을 기준으로 오른쪽 면적
    print("\n4.유의수준 : %g" %a)    # 오른쪽 면적

    if I < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 우측 분산추론 검정

# In[136]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모분산이 'v'인지 확인 -> Var
# 모표준편차 's' 를 기준으로 하고 싶으면, 'v' 자리에 's^2'을 넣으면 됨.  
# 카이제곱검정을 사용하여 모분산 확인, 모집단 1개, 우측검정 
# Chi_Variance_Rightsided 축약 : ChiVar_R

def ChiVar_R(a,x,v) :
    
    df = pd.read_csv('./chi.csv',encoding='euc-kr',index_col=0) 
      
    k = len(x) - 1
    chi = round(k*Std(x)^2/v,17)    
    print("1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", k)
    
    cr = df["%g" %a][int(k)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    z = sp.symbols('z')
    C = (z^(k/2 - 1))*(e^(-z/2))/((2^(k/2))*gamma(k/2))     # 카이제곱 분포 함수
    I = 1 - sp.Integral(C,(z,0,chi))       # 검정통계량의 넓이 (비율 p) 바로 구함
    print("\n5.p값 : %g" %I)         # 검정통계량을 기준으로 오른쪽 면적
    print("\n6.유의수준 : %g" %a)    # 오른쪽 면적

    if I < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 좌측 분산추론 검정 (표)

# In[137]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모분산이 'v'인지 확인 -> Var
# 모표준편차 's' 를 기준으로 하고 싶으면, 'v' 자리에 's^2'을 넣으면 됨.  
# 카이제곱검정을 사용하여 모분산 확인, 모집단 1개, 좌측 기각역 검정 
# Chi_Variance_Leftsided_criticalregion 축약 : ChiVar_Lcr

def ChiVar_Lcr(a,x,v) :
    
    df = pd.read_csv('./chi.csv',encoding='euc-kr',index_col=0) 
     
    chi = (len(x) - 1)*Std(x)^2/v    
    print("1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", len(x) - 1)
    
    cr = df["%g" %(1 - a)][int(len(x) - 1)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : (0, {0})".format(cr))
    
    if chi < cr :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 좌측 분산추론 검정 (함수)

# In[138]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모분산이 'v'인지 확인 -> Var
# 모표준편차 's' 를 기준으로 하고 싶으면, 'v' 자리에 's^2'을 넣으면 됨.  
# 카이제곱검정을 사용하여 모분산 확인, 모집단 1개, 좌측 p값 검정 
# Chi_Variance_Leftsided_probabilityvalue 축약 : ChiVar_Lp

def ChiVar_Lp(a,x,v) :
    
    k = len(x) - 1
    chi = round(k*Std(x)^2/v,17)    
    print("1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", k)
    
    z = sp.symbols('z')
    C = (z^(k/2 - 1))*(e^(-z/2))/((2^(k/2))*gamma(k/2))     # 카이제곱 분포 함수
    I = sp.Integral(C,(z,0,chi))       # 검정통계량의 넓이 (비율 p) 바로 구함
    print("\n3.p값 : %g" %I)         # 검정통계량을 기준으로 왼쪽 면적
    print("\n4.유의수준 : %g" %a)    # 왼쪽 면적

    if I < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 좌측 분산추론 검정

# In[139]:


# 유의수준 'a' 로 자료 'x'를 귀납가설 (기준이 되는) 모분산이 'v'인지 확인 -> Var
# 모표준편차 's' 를 기준으로 하고 싶으면, 'v' 자리에 's^2'을 넣으면 됨.  
# 카이제곱검정을 사용하여 모분산 확인, 모집단 1개, 좌측검정 
# Chi_Variance_Leftsided 축약 : ChiVar_L

def ChiVar_L(a,x,v) :
    
    df = pd.read_csv('./chi.csv',encoding='euc-kr',index_col=0) 
     
    k = len(x) - 1
    chi = round(k*Std(x)^2/v,17)    
    print("1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", k)
    
    cr = df["%g" %(1 - a)][int(k)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : (0, {0})".format(cr))
    
    z = sp.symbols('z')
    C = (z^(k/2 - 1))*(e^(-z/2))/((2^(k/2))*gamma(k/2))     # 카이제곱 분포 함수
    I = sp.Integral(C,(z,0,chi))       # 검정통계량의 넓이 (비율 p) 바로 구함
    print("\n5.p값 : %g" %I)         # 검정통계량을 기준으로 왼쪽 면적
    print("\n6.유의수준 : %g" %a)    # 왼쪽 면적

    if I < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ### F-검정통계량을 이용한 두 모집단의 분산추론 검정
# 
# #### 두 모집단의 모분산이 같은지, 다른지 확인하기 위해 두 모집단의 표본분산비(F통계량)를 이용함.

# #### 양측 두 분산 추론 검정 (기각역)

# In[140]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 두 모분산이 같은지 확인  -> Var 
# F검정을 사용, 모집단 2개, 양측 기각역 검정 
# F_Variance2_Twosided_criticalregion 축약 : FVar2_Tscr

def FVar2_Tscr(a,x,y) :
        
    df = pd.read_csv('./F분포표(%g).csv' %(a/2), index_col=0)
    
    F = Std(x)^2 / Std(y)^2
    print("1.검정통계량 : %g" %F)
    print("\n2.두 자유도 : %g, %g" %(len(x) - 1, len(y) - 1))            
                                                                     # 임계값 관계
    cr1 = 1/(df['%g' %(len(y) - 1)][int(len(x) - 1)])
    cr2 = df['%g' %(len(x) - 1)][int(len(y) - 1)]            # 1/F(len(y) - 1,len(x) - 1, a) = F(len(x) - 1,len(y) - 1, 1-a)                                                                 # 임계값 관계      
    print("\n3.임계값 : %g, %g" %(cr1, cr2))                 
    print("\n4.기각역 : (0, %g) or (%g, oo)" %(cr1, cr2))
    
    if F < 1/cr1 or cr2 < F :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 두 분산 추론 검정 (p값)

# In[141]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 두 모분산이 같은지 확인  -> Var 
# F검정을 사용, 모집단 2개, 양측 p값 검정 
# F_Variance2_Twosided_probabilityvalue 축약 : FVar2_Tsp

def FVar2_Tsp(a,x,y) : 
    
    F = round(Std(x)^2 / Std(y)^2,17)
    print("1.검정통계량 : %g" %F)
    
    v = len(x) - 1 
    w = len(y) - 1 
    print("\n2.두 자유도 : %g, %g" %(v,w)) 
    
    z = sp.symbols('z') 
    f = (v^(0.5*v))*(w^(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(z^(0.5*(v - 2)))/(v*z + w)^(0.5*(v + w))
    i = sp.Integral(f,(z,0,F))
    mi = min(1 - i, i)
    print("\n3.p값 : %g" %(mi*2))
    print("\n4.유의수준 : %g" %a)
    
    if mi < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 양측 두 분산 추론 검정

# In[142]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 두 모분산이 같은지 확인  -> Var 
# F검정을 사용, 모집단 2개, 양측검정 
# F_Variance2_Twosided 축약 : FVar2_Ts

def FVar2_Ts(a,x,y) : 
    
    F = round(Std(x)^2 / Std(y)^2,17)
    print("1.검정통계량 : %g" %F)
    
    v = len(x) - 1 
    w = len(y) - 1 
    print("\n2.두 자유도 : %g, %g" %(v,w)) 
        
    df = pd.read_csv('./F분포표(%g).csv' %(a/2), index_col=0)        # 임계값 관계
    cr1 = 1/(df['%g' %(len(y) - 1)][int(len(x) - 1)])
    cr2 = df['%g' %(len(x) - 1)][int(len(y) - 1)]            # 1/F(len(y) - 1,len(x) - 1, a) = F(len(x) - 1,len(y) - 1, 1-a)                                                                 # 임계값 관계      
    print("\n3.임계값 : %g, %g" %(cr1, cr2))                 
    print("\n4.기각역 : (0, %g) or (%g, oo)" %(cr1, cr2))
    
    z = sp.symbols('z') 
    f = (v^(0.5*v))*(w^(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(z^(0.5*(v - 2)))/(v*z + w)^(0.5*(v + w))
    i = sp.Integral(f,(z,0,F))
    mi = min(1 - i, i)
    print("\n5.p값 : %g" %(mi*2))
    print("\n6.유의수준 : %g" %a)
    
    if mi < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 우측 두 분산 추론 검정 (기각역)

# In[143]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모분산이 y의 모분산보다 큰지 확인  -> Var 
# F검정을 사용, 모집단 2개, 단측(우측) 기각역 검정 
# F_Variance2_Right_criticalregion 축약 : FVar2_Rcr

def FVar2_Rcr(a,x,y) :
        
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    
    F = Std(x)^2 / Std(y)^2
    print("1.검정통계량 : %g" %F)
    print("\n2.두 자유도 : %g, %g" %(len(x) - 1, len(y) - 1))             
                                                                    
    cr = df['%g' %(len(x) - 1)][int(len(y) - 1)]           
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    if cr < F :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 우측 두 분산 추론 검정 (p값)

# In[144]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모분산이 y의 모분산보다 큰지 확인  -> Var 
# F검정을 사용, 모집단 2개, 단측(우측) p값 검정 
# F_Variance2_Right_probabilityvalue 축약 : FVar2_Rp

def FVar2_Rp(a,x,y) :
    
    F = round(Std(x)^2 / Std(y)^2,17)
    print("1.검정통계량 : %g" %F)
    
    v = len(x) - 1 
    w = len(y) - 1 
    print("\n2.두 자유도 : %g, %g" %(v,w))
    
    z = sp.symbols('z')
    f = (v^(0.5*v))*(w^(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(z^(0.5*(v - 2)))/(v*z + w)^(0.5*(v + w))
    i = 1 - sp.Integral(f,(z,0,F))
    print("\n3.p값 : %g" %i)
    print("\n4.유의수준 : %g" %a)
    
    if i < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 우측 두 분산 추론 검정

# In[145]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모분산이 y의 모분산보다 큰지 확인  -> Var 
# F검정을 사용, 모집단 2개, 단측(우측)검정 
# F_Variance2_Right 축약 : FVar2_R

def FVar2_R(a,x,y) :
        
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    
    F = round(Std(x)^2 / Std(y)^2,17)
    print("1.검정통계량 : %g" %F)
    
    v = len(x) - 1 
    w = len(y) - 1 
    print("\n2.두 자유도 : %g, %g" %(v,w))
                                                                    
    cr = df['%g' %(len(x) - 1)][int(len(y) - 1)]            
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    z = sp.symbols('z')
    f = (v^(0.5*v))*(w^(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(z^(0.5*(v - 2)))/(v*z + w)^(0.5*(v + w))
    i = 1 - sp.Integral(f,(z,0,F))
    print("\n5.p값 : %g" %i)
    print("\n6.유의수준 : %g" %a)
    
    if i < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 좌측 두 분산 추론 검정 (기각역)

# In[146]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모분산이 y의 모분산보다 작은지 확인  -> Var 
# F검정을 사용, 모집단 2개, 단측(좌측) 기각역 검정 
# F_Variance2_Left_criticalregion 축약 : FVar2_Lcr

def FVar2_Lcr(a,x,y) :
        
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    
    F = Std(x)^2 / Std(y)^2
    print("1.검정통계량 : %g" %F)
    print("\n2.두 자유도 : %g, %g" %(len(x) - 1, len(y) - 1))             
                                                                    
    cr = 1/(df['%g' %(len(y) - 1)][int(len(x) - 1)])           
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    if cr < F :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 좌측 두 분산 추론 검정 (p값)

# In[147]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모분산이 y의 모분산보다 작은지 확인  -> Var 
# F검정을 사용, 모집단 2개, 단측(좌측) p값 검정 
# F_Variance2_Left_probabilityvalue 축약 : FVar2_Lp

def FVar2_Lp(a,x,y) :
    
    F = round(Std(x)^2 / Std(y)^2,17)
    print("1.검정통계량 : %g" %F)
    
    v = len(x) - 1 
    w = len(y) - 1 
    print("\n2.두 자유도 : %g, %g" %(v,w))
    
    z = sp.symbols('z')
    f = (v^(0.5*v))*(w^(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(z^(0.5*(v - 2)))/(v*z + w)^(0.5*(v + w))
    i = sp.Integral(f,(z,0,F))
    print("\n3.p값 : %g" %i)
    print("\n4.유의수준 : %g" %a)
    
    if i < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 좌측 두 분산 추론 검정

# In[148]:


# 유의수준 'a' 로 두 자료 'x, y'를 귀납가설 x의 모분산이 y의 모분산보다 작은지 확인  -> Var 
# F검정을 사용, 모집단 2개, 단측(좌측)검정 
# F_Variance2_Left 축약 : FVar2_L

def FVar2_L(a,x,y) :
        
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    
    F = round(Std(x)^2 / Std(y)^2,17)
    print("1.검정통계량 : %g" %F)
    
    v = len(x) - 1 
    w = len(y) - 1 
    print("\n2.두 자유도 : %g, %g" %(v,w))
                                                                    
    cr = 1/(df['%g' %(len(y) - 1)][int(len(x) - 1)])           
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    z = sp.symbols('z')
    f = (v^(0.5*v))*(w^(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(z^(0.5*(v - 2)))/(v*z + w)^(0.5*(v + w))
    i = sp.Integral(f,(z,0,F))
    print("\n5.p값 : %g" %i)
    print("\n6.유의수준 : %g" %a)
    
    if i < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ---
# ---

# ## 카이제곱검정

# ### 하나의 범주형 변수

# #### i범주 기댓값

# In[149]:


# 'x': 각 표본 수의 전체 리스트, 'p': 각 범주의 확률 전체 리스트, 'i': i번째 범주
def fit_expected_value(x,p,i):
    return sum(x)*p[i-1]


# #### 적합도 검정통계량의 근사분포

# In[150]:


# 'x': 각 표본 수의 전체 리스트, 'p': 각 범주의 확률 전체 리스트
def fit_chi(x,p):
    return round(sum(map(lambda i,q:(i-fit_expected_value(x,p,x.index(i)))**2/fit_expected_value(x,p,x.index(i)),x,p)),17)


# #### 피어슨 잔차(Pearson residual)

# In[151]:


# 'x': 각 표본 수의 전체 리스트, 'p': 각 범주의 확률 전체 리스트
def pea_res(x,p):
    return sqrt(fit_chi(x,p))


# ### 적합도 검정
# - 실제 표본과 비교하여 가정된 분포가 맞는지를 확인 즉 가정된 분포가 적합한지 검정하는 것

# - 포아송분포
#     - 모수 lambda가 주어진 경우는 그대로 사용하면 되고, 모수 lambda가 주어지지 않았다면 포아송분포의 평균인 lambda를 자료의 표본평균으로부터 추정할 수 있다.

# In[152]:


# 'x': 자료 수 (리스트), 'y': 관측도수(관측빈도)
# 포아송분포의 적합도 검정 (Ho(귀무가설): -가 포아송분포를 따른다. H1(대립가설): -가 포아송분포를 따르지 않는다.)
def Po1_Ts(x, y):
    lambd = (sum(map(lambda a, b: (a * b), x, y))) / sum(y)
    
    ex_list = list(map(lambda k: po_pmf(lambd, k), x))
    exp_list = list(map(lambda k: po_pmf(lambd, k) * sum(y), x))
    A = pd.DataFrame({'기대빈도': ex_list,
                      'Exp=n*f(x)': exp_list},
                     index=x)
    
    collapsed_A = A.copy()
    
    # 기대빈도표
    A.loc['%g 이상'%(max(x)+1)] = (1 - A['기대빈도'].sum() , sum(y) - A['Exp=n*f(x)'].sum()) 
    A.loc['합계'] = A.sum()  
    print("\n[기대빈도표]")
    print(A)
    
    #붕괴된 기대빈도표
    index_below_5 = collapsed_A[collapsed_A['Exp=n*f(x)'] < 5].index

    start_index = collapsed_A.index.get_loc(index_below_5[0]) - 1  
    end_index = collapsed_A.index.get_loc(index_below_5[-1])  
    
    collapsed_A = collapsed_A.drop(collapsed_A.index[start_index:end_index+1])
    collapsed_A.loc['%g 이상'%(index_below_5[0]-1)] = (1 - collapsed_A['기대빈도'].sum() , sum(y) - collapsed_A['Exp=n*f(x)'].sum()) 
    coll2 = collapsed_A.copy()
    collapsed_A.loc['합계'] = collapsed_A.sum()  
    print("\n[붕괴된(collapsed) 기대빈도표]")
    print(collapsed_A)
    
    #카이제곱통계량의 계산표
    y[start_index]+=sum(y[start_index+1:end_index+1])
    coll2['(Oi-Ei)**2/Ei'] = list(map(lambda a,b: (a-b)**2 / b, y, coll2['Exp=n*f(x)']))
    chi = coll2['(Oi-Ei)**2/Ei'].sum()
    dfl = len(coll2.index)-2
    coll2.loc['합계'] = coll2.sum()
    print("\n[카이제곱통계량의 계산표]")
    print(coll2)
    print("\n[카이제곱 적합도 검정의 자유도:]",len(coll2.index)-3)
    df = pd.read_csv('./chi.csv',encoding='euc-kr',index_col=0)
 
    print("\n1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", dfl)
    
    cr = df["%g" %0.05][int(len(x) - 1)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    if cr < chi :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# In[153]:


# 'x': '자료 수 (리스트), 'y': 기대 개수
# 데이터 값이 가정에 "충분히" 적합한지 확인
# 자료 개수와 기대 개수의 가정에 적합도를 판별하는 경우
def Po1_Ts2(x, y):
    A = pd.DataFrame({'관측값':x,
                      '기대 개수':y})
    diff_A = A.copy()
    print(A)
    diff_list = list(map(lambda a,b:(a - b),x,y))
    diff_square = list(map(lambda a: (a**2),diff_list))
    diff_A['(관측값-기대값)'] = diff_list
    diff_A['차이제곱값'] = diff_square
    print("\n[차이 제곱값 계산]")
    print(diff_A)
    
    #카이제곱통계량의 계산표
    chi_A = diff_A.copy()
    chi_A['차이제곱/기대개수'] = list(map(lambda a,b: round(sp.N(a/b),7),diff_square,y))
    chi = chi_A['차이제곱/기대개수'].sum()
    print("\n[제곱값/기대 개수 계산]")
    print(chi_A)
    
    df = pd.read_csv('./chi.csv',encoding='euc-kr',index_col=0)
 
    print("\n1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", int(len(x) - 1))
    
    cr = df["%g" %0.05][int(len(x) - 1)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    if cr < chi :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# In[ ]:





# - 정규분포
#     - 정규성 가정의 타당성을 보장하기 위해 카이제곱분포를 이용하여 검정할 수 있다.
#     - 정규분포하는 자료는 연속형 변수이므로 이를 몇 개의 급간(class)로 나누어 도수분포표를 만들어, 즉 이산형화하여 카이제곱검정을 하게 된다.
#     - 구간 나누기 check 必

# In[154]:


# 속도 수정
# 'x': 자료 (리스트)
# 정규분포의 적합도 검정 (Ho(귀무가설): -가 정규분포를 따른다. H1(대립가설): -가 정규분포를 따르지 않는다.)
# 표준정규분포의 누적 분포 함수 (CDF)
def norm_cdf(x):
    return 0.5 * (1 + erf(x / sqrt(2)))

# 누적 확률 값 계산 함수
def calculate_cpr(cp3_val):
    lo, hi = -10, 10  # 초기 탐색 범위 설정
    while hi - lo > 1e-5:  # 원하는 정밀도에 도달할 때까지 반복
        mid = (lo + hi) / 2
        if norm_cdf(mid) < cp3_val:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 3)

# 정규분포의 적합도 검정
def Z1_fit_Ts(x):
    min_val = min(x)
    max_val = max(x)
    range_val = max_val - min_val

    cp = len(x) / 5  # 각 구간의 기대도수가 5가 되도록 설정
    cp2 = float(cp / 100)
    cp3_values = [cp2 + i * cp2 for i in range(int(cp) - 1)]

    cpr_list = list(map(calculate_cpr, cp3_values))
    xv_list = list(map(lambda cpr: cpr * Std(x) + Mean(x), cpr_list))

    if range_val <= 20:
        interval_list = [f'~{xv_list[0]}'] + [
            f'{xv_list[i]}~{xv_list[i + 1]}' if i < len(xv_list) - 1 else f'{xv_list[i]}~' for i in range(len(xv_list))
        ]
    else:
        interval_list = [f'~{xv_list[0]}'] + [
            f'{xv_list[i]}~{xv_list[i + 1]}' if i < len(xv_list) - 1 else f'{xv_list[i]}~' for i in range(len(xv_list))
        ]

    intervals_len = len(xv_list)
    interval_indices = list(
        map(lambda value: next((i for i, interval in enumerate(xv_list) if value <= interval), intervals_len), x)
    )
    counts = list(map(lambda i: interval_indices.count(i), range(intervals_len + 1)))
    O_E = list(map(lambda x, y: float((x - y) ** 2 / y), counts, [5] * len(counts)))

    print("\n[카이제곱통계량의 계산표]")
    A = pd.DataFrame({
        '구간': interval_list,
        '관측도수(Oi)': counts,
        '기대도수(Ei)': [5] * len(counts),
        '(Oi-Ei)**2/Ei': O_E
    })
    A.set_index('구간', inplace=True)
    chi = A['(Oi-Ei)**2/Ei'].sum()
    A.loc['합계'] = A.sum()
    print(A)

    print("\n[카이제곱 적합도 검정의 자유도:]", len(interval_list) - 3)
    df = pd.read_csv('./chi.csv', encoding='euc-kr', index_col=0)

    print("1.검정통계량 : %g" % chi)
    print("\n2.자유도 :", len(interval_list) - 3)

    cr = df["%g" % 0.05][int(len(interval_list) - 3)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))

    if cr < chi:
        ans = "[결과] : 귀무가설을 기각한다."
    else:
        ans = "[결과] : 귀무가설을 기각하지 못한다."

    return ans


# In[ ]:





# In[ ]:





# ##### 나이에 대한 정규분포 적합도 검정 (추가 작업함)

# In[155]:


# 속도 수정
def classify_age(x):
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    
    # 연령대를 계산하는 함수
    calc_age_group = lambda age: (age // 10) * 10

    # 각 나이를 연령대로 변환
    age_groups = list(map(calc_age_group, x))

    # 연령대별 데이터를 그룹화
    unique_age_groups = list(set(age_groups))
    age_ranges = {age_group: list(filter(lambda age: calc_age_group(age) == age_group, x)) for age_group in unique_age_groups}

    # 연령대별 인원 수
    count = dict(map(lambda age_group: (age_group, len(age_ranges[age_group])), age_ranges.keys()))
    
    # 연령대 리스트 (단, 10세는 제외합니다)
    numbers = [key for key in sorted(age_ranges.keys()) if key != 10]
    probs = []
    mean_x = round(Mean(x), 3)
    std_x = round(Std(x), 3)

    probs = list(map(lambda num: abs(round((num - mean_x) / std_x, 2)), numbers))

    # prob_list 계산
    prob_list = list(map(lambda prob: df.loc[float(math.floor(prob * 10) / 10), str(float(math.floor(prob * 100) % 10) / 100)] if float(math.floor(prob * 100) % 10) / 100 != 0 else None, probs))

    total_sample_size = len(x)
    expected_probs = []
    expected_freqs = []
    age_groupings = []
    count_ages = []
    
    # 기대확률 계산 및 출력
    for i, age_group in enumerate(sorted(age_ranges.keys())):
        if age_group == min(age_ranges.keys()):
            expected_prob = abs(0.5 - prob_list[0])
            expected_freq = expected_prob * total_sample_size
            count_age = count[age_group]
            age_groupings.append((f"{age_group + 10}세 미만"))
        elif age_group == max(age_ranges.keys()):
            expected_prob = abs(0.5 - prob_list[-1])
            expected_freq = expected_prob * total_sample_size
            count_age = count[age_group]
            age_groupings.append((f"{age_group}세 이상"))
        else:
            expected_prob = abs(prob_list[i-1] - prob_list[i])
            expected_freq = expected_prob * total_sample_size
            count_age = count[age_group]
            age_groupings.append((f"{age_group}세 이상 ~ {age_group + 10}세 미만"))

        expected_probs.append(expected_prob)
        expected_freqs.append(expected_freq)
        count_ages.append(count_age)
        
    # 데이터 프레임 생성
    A = pd.DataFrame({
        '구간': age_groupings,
        '관찰도수': count_ages,
        '기대빈도': expected_freqs,
        '기대확률': expected_probs
    })
    A.set_index('구간', inplace=True)
    print("\n[N(m,a**2)]에서 각 구간별 기대확률과 기대도수]")
    print(A)
    
    # 관찰도수 계산
    observed_freqs = [count[age_group] for age_group in sorted(age_ranges.keys())]
    
    # 기대도수가 작은 구간 합치기
    merged_groups = []
    merged_observed_freqs = []
    merged_expected_probs = []
    merged_expected_freqs = []

    i = 0
    while i < len(expected_freqs):
        if expected_freqs[i] <= 5:
            if i == 0:
                merged_groups.append(f"{age_groupings[i]} ~ {age_groupings[i + 1]}")
                merged_observed_freqs.append(observed_freqs[i] + observed_freqs[i + 1])
                merged_expected_probs.append(expected_probs[i] + expected_probs[i + 1])
                merged_expected_freqs.append(expected_freqs[i] + expected_freqs[i + 1])
                i += 2
            elif i == len(expected_freqs) - 1:
                merged_groups[-1] = f"{merged_groups[-1]} ~ {age_groupings[i]}"
                merged_observed_freqs[-1] += observed_freqs[i]
                merged_expected_probs[-1] += expected_probs[i]
                merged_expected_freqs[-1] += expected_freqs[i]
                i += 1
            else:
                merged_groups.append(f"{age_groupings[i]} ~ {age_groupings[i + 1]}")
                merged_observed_freqs.append(observed_freqs[i] + observed_freqs[i + 1])
                merged_expected_probs.append(expected_probs[i] + expected_probs[i + 1])
                merged_expected_freqs.append(expected_freqs[i] + expected_freqs[i + 1])
                i += 2
        else:
            merged_groups.append(age_groupings[i])
            merged_observed_freqs.append(observed_freqs[i])
            merged_expected_probs.append(expected_probs[i])
            merged_expected_freqs.append(expected_freqs[i])
            i += 1

    B = pd.DataFrame({
        '구간': merged_groups,
        '관찰도수': merged_observed_freqs,
        '기대확률': merged_expected_probs,
        '기대도수': merged_expected_freqs
    })
    B.set_index('구간', inplace=True)
    print("\n[기대도수가 작은 구간을 인접구간과 합친 표]")
    print(B)
    
    print("\n[카이제곱통계량의 계산표]")
    chi = sum(((B['관찰도수'] - B['기대도수']) ** 2) / B['기대도수'])

    print("1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", len(B)-1)
    
    cr = df["%g" %0.05][int(len(B)-3)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    if cr < chi :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
    return ans

x = [28, 55, 26, 35, 43, 47, 47, 10, 35, 26, 65, 57, 34, 28, 43, 20, 30, 53, 27, 32, 34, 43, 18, 38, 29, 44, 67, 48, 45, 43]
classify_age(x)


# In[ ]:





# In[156]:


# 속도 수정(중)
def classify_age2(x):
    df = pd.read_csv('./표준정규분포표.csv', encoding='euc-kr', index_col=0)
    
    # 연령대를 계산하는 함수
    calc_age_group = lambda age: (age // 10) * 10

    # 각 나이를 연령대로 변환
    age_groups = list(map(calc_age_group, x))

    # 연령대별 데이터를 그룹화
    unique_age_groups = list(set(age_groups))
    age_ranges = {age_group: list(filter(lambda age: calc_age_group(age) == age_group, x)) for age_group in unique_age_groups}

    # 연령대별 인원 수
    count = dict(map(lambda age_group: (age_group, len(age_ranges[age_group])), age_ranges.keys()))
    
    # 연령대 리스트 (단, 10세는 제외합니다)
    numbers = [key for key in sorted(age_ranges.keys()) if key != 10]
    
    mean_x = round(Mean(x), 3)
    std_x = round(Std(x), 3)

    probs = list(map(lambda num: abs(round((num - mean_x) / std_x, 2)), numbers))
    # prob_list 계산
    prob_list = list(map(lambda prob: df.loc[float(math.floor(prob * 10) / 10), str(float(math.floor(prob * 100) % 10) / 100)] if float(math.floor(prob * 100) % 10) / 100 != 0 else None, probs))

    total_sample_size = len(x)
     
    # 계급 이름 생성
    age_groupings = list(map(lambda age_group: (f"{age_group + 10}세 미만" if age_group == min(age_ranges.keys())
                                                else f"{age_group}세 이상" if age_group == max(age_ranges.keys())
                                                else f"{age_group}세 이상 ~ {age_group + 10}세 미만"), sorted(age_ranges.keys())))

    # 기대확률 및 기대도수 계산
    expected_probs = list(map(lambda i, age_group: abs(0.5 - prob_list[0]) if i == 0
                              else abs(0.5 - prob_list[-1]) if i == len(age_ranges) - 1
                              else abs(prob_list[i-1] - prob_list[i]), range(len(age_ranges)), sorted(age_ranges.keys())))
    
    expected_freqs = list(map(lambda expected_prob: expected_prob * total_sample_size, expected_probs))
    count_ages = list(map(lambda age_group: count[age_group], sorted(age_ranges.keys())))

        
    # 데이터 프레임 생성
    A = pd.DataFrame({
        '구간': age_groupings,
        '관찰도수': count_ages,
        '기대빈도': expected_freqs,
        '기대확률': expected_probs
    })
    A.set_index('구간', inplace=True)
    print("\n[N(m,a**2)]에서 각 구간별 기대확률과 기대도수]")
    print(A)
    
    # 관찰도수 계산
    observed_freqs = [count[age_group] for age_group in sorted(age_ranges.keys())]
    
        # 기대도수가 작은 구간 합치기
    merged_groups = []
    merged_observed_freqs = []
    merged_expected_probs = []
    merged_expected_freqs = []

    i = 0
    while i < len(expected_freqs):
        if expected_freqs[i] <= 5:
            if i == 0:
                merged_groups.append(f"{age_groupings[i]} ~ {age_groupings[i + 1]}")
                merged_observed_freqs.append(observed_freqs[i] + observed_freqs[i + 1])
                merged_expected_probs.append(expected_probs[i] + expected_probs[i + 1])
                merged_expected_freqs.append(expected_freqs[i] + expected_freqs[i + 1])
                i += 2
            elif i == len(expected_freqs) - 1:
                merged_groups[-1] = f"{merged_groups[-1]} ~ {age_groupings[i]}"
                merged_observed_freqs[-1] += observed_freqs[i]
                merged_expected_probs[-1] += expected_probs[i]
                merged_expected_freqs[-1] += expected_freqs[i]
                i += 1
            else:
                merged_groups.append(f"{age_groupings[i]} ~ {age_groupings[i + 1]}")
                merged_observed_freqs.append(observed_freqs[i] + observed_freqs[i + 1])
                merged_expected_probs.append(expected_probs[i] + expected_probs[i + 1])
                merged_expected_freqs.append(expected_freqs[i] + expected_freqs[i + 1])
                i += 2
        else:
            merged_groups.append(age_groupings[i])
            merged_observed_freqs.append(observed_freqs[i])
            merged_expected_probs.append(expected_probs[i])
            merged_expected_freqs.append(expected_freqs[i])
            i += 1

    B = pd.DataFrame({
        '구간': merged_groups,
        '관찰도수': merged_observed_freqs,
        '기대확률': merged_expected_probs,
        '기대도수': merged_expected_freqs
    })
    B.set_index('구간', inplace=True)
    print("\n[기대도수가 작은 구간을 인접구간과 합친 표]")
    print(B)
    
    print("\n[카이제곱통계량의 계산표]")
    chi = sum(((B['관찰도수'] - B['기대도수']) ** 2) / B['기대도수'])

    print("1.검정통계량 : %g" %chi)
    print("\n2.자유도 :", len(B)-1)
    
    cr = df["%g" %0.05][int(len(B)-3)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    if cr < chi :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
    return ans

x = [28, 55, 26, 35, 43, 47, 47, 10, 35, 26, 65, 57, 34, 28, 43, 20, 30, 53, 27, 32, 34, 43, 18, 38, 29, 44, 67, 48, 45, 43]
classify_age2(x)


# In[ ]:





# In[ ]:





# ### 두 개의 범주형 변수

# #### 독립성 검정
# - 두 개의 범주형 변수가 독립인지 검정
# - 두 변수가 독립이라면 결합확률이 독립이어야 함.
#     - Oij: ij번째 결합범주의 표본수, Oi: i번째 행의 합, Oj: j번째 열의 합, n: 전체 표본수, pi_i = Oi / n : πi의 추정값, pi_j = Oj / n : πj의 추정값, pi_ij = pi_i * pi_j

# In[157]:


# 속도 수정
# 'x': 중첩된 딕셔너리(nested dictionary)
def chi_ind_Ts(x):
    print("\n[입력한 데이터인 두 개의 범주형 변수의 분할표]")
    A = pd.DataFrame(x).T
    n = A.values.sum()
    B = A.copy()
    A.loc['합계'] = A.sum()
    A['합계'] = A.sum(axis=1)
    print(A)

    print("\n[독립인 경우 추정 결합확률표]")
    row_totals = B.sum(axis=1).values[:, None]  # 행 합계 (열 방향으로 확장)
    col_totals = B.sum(axis=0).values[None, :]  # 열 합계 (행 방향으로 확장)

    C = (row_totals @ col_totals) / (n * n)  # 독립인 경우 추정 결합확률 계산
    C = pd.DataFrame(C, index=B.index, columns=B.columns)
    C.loc['합계'] = C.sum()
    C['합계'] = C.sum(axis=1)
    print(C)

    print("\n[독립인 경우 기댓값표]")
    D = (row_totals @ col_totals) / n  # 독립인 경우 기댓값 계산
    D = pd.DataFrame(D, index=B.index, columns=B.columns)
    D.loc['합계'] = D.sum()
    D['합계'] = D.sum(axis=1)
    E = (B - D) ** 2 / D
    E.loc['합계'] = E.sum()
    E['합계'] = E.sum(axis=1)
    print(E)

    print("\n[카이제곱 독립성 검정의 자유도:]", (len(B.columns)-1) * (len(B.index)-1))



    chi = E['합계']['합계']
    df = pd.read_csv('./chi.csv', encoding='euc-kr', index_col=0)

    print("\n1.검정통계량 : %g" % chi)
    dof = (len(B.columns) - 1) * (len(B.index) - 1)
    print("\n2.자유도 :", dof)

    cr = df["%g" % 0.05][int(dof)]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr),'\n')

    if chi > cr:
        ans = "[결과] : 귀무가설을 기각한다."
    else:
        ans = "[결과] : 귀무가설을 기각하지 못한다."

    return ans


# #### 동질성 검정
# - 범주형 자료의 분포에 대한 두 집단의 동질성 검정(test of homogeneity)을 카이제곱분포에 근사하여 수행할 수 있다.
# - 범주형 자료는 이항분포나 다항분포를 하게 되고 이들 분포가 두 집단에서 같은지 검정하게 된다.

# - 이항분포의 등확률검정(test of equal probabilities)
#     - 두 개의 이항분포가 같은지 검정하는 것이므로 1개의 모수를 추정한 것이어 자유도는 1이다.

# In[158]:


# 속도 수정
# 'x': 중첩된 딕셔너리(nested dictionary)
def bi_equal_Ht(x):
    print("\n[입력한 데이터인 두 개의 범주형 변수의 분할표]")
    A = pd.DataFrame(x).T
    B = A.copy()
    A.loc['합계'] = A.sum()
    A['합계'] = A.sum(axis=1)
    print(A)
    
    print("\n[추정 확률표]")
    row_indices = B.index
    column_indices = B.columns

    C = pd.DataFrame(index=row_indices, columns=column_indices)
    C[column_indices] = list(map(lambda i: list(B.sum())[i] / sum(B.sum(axis=1)), range(len(column_indices))))
    C['합계'] = C.sum(axis=1)    
    print(C)
    
    print("\n[기댓값표]")
    D = pd.DataFrame(index=row_indices, columns=column_indices)
    D[column_indices] = list(map(lambda i: list(B.sum())[i] / sum(B.sum(axis=1)), range(len(column_indices))))
    D.loc[row_indices] = D.loc[row_indices].apply(lambda row: row * list(B.sum(axis=1)), axis=0)
    D['합계'] = D.sum(axis=1)   
    print(D)
    
    print("\n[카이제곱표]")
    E = ((A - D) ** 2).div(D)
    E.loc['합계'] = E.sum()
    E['합계'] = E.sum(axis=1)
    print(E)
    
    print("\n[등확률검정의 자유도:]", 1)
    df = pd.read_csv('./chi.csv', encoding='euc-kr', index_col=0)
    
    chi = E.loc['합계', '합계']
    print("\n1.검정통계량 : %g" % chi)
    
    print("\n2.자유도 :", 1)
    
    cr = df["0.05"][int((len(B.columns) - 1) * (len(B.index) - 1))]
    print("\n3.임계값 : {0}".format(cr))
    print("\n4.기각역 : ({0}, oo)".format(cr))
    
    if cr < chi:
        ans = "[결과] : 귀무가설을 기각한다."
    else:
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# In[ ]:





# In[ ]:





# ---

# ## 분산분석

# ### 일원분산분석
# - 여러 집단의 평균이 같은지 분석
# - 앞서 Z나 t 통계량 등을 이용하여 두 모집단의 평균 비교에 관한 내용을 다룸. 분산분석은 3개 이상의 모집단의 평균을 비교.

# #### 처리제곱합

# In[159]:


# 'A': 집단 자료 (리스트 or pd.Series 형태)
def SSTR(*A) :
    x = sum(map(sum, A))/sum(map(len, A))
    return sum(map(lambda a : len(a)*(Mean(a) - x)^2, A))


# #### 처리평균제곱

# In[160]:


# 'A': 집단 자료 (리스트 or pd.Series 형태)
def MSTR(*A) :                  
    return SSTR(*A)/(len(A) - 1)


# #### 오차제곱합

# In[161]:


# 'A': 집단 자료 (리스트 or pd.Series 형태)
def SSE(*A) :
    return sum(map(lambda a : (len(a) - 1)*Std(a)^2, A))


# #### 오차평균제곱

# In[162]:


# 'A': 집단 자료 (리스트 or pd.Series 형태)
def MSE(*A) :
    return SSE(*A)/(sum(map(len, A)) - len(A))


# #### 일원분산분석의 F 통계량

# In[163]:


# 'A': 집단 자료 (리스트 or pd.Series 형태)
def Fstt(*A) :
    return MSTR(*A)/MSE(*A)


# #### 총제곱합

# In[164]:


# 'A': 집단 자료 (리스트 or pd.Series 형태)
def SST(*A) :
    x = sum(map(sum,A))/sum(map(len,A))
    return float(sum(map(lambda a : sum(map(lambda a1 : (a1 - x)^2, a)), A)))

def SST2(*A) :
    return SSTR(*A) + SSE(*A)


# #### 일원분산분석에서의 F통계량 가설검정 (함수 : p값과 유의수준)

# In[165]:


# 'a': 유의수준, 'A': 집단 자료 (리스트 or pd.Series 형태)
def FAOVp(a,*A) :
    f = x
    F = round(Fstt(*A),17)
    print("1.검정통계량 : %g" %F)
    
    v = len(A) - 1 
    w = sum(map(len,A)) - len(A) 
    print("\n2.두 자유도 : %g, %g" %(v,w))
    
    x = sp.symbols('x')
    f = (v^(0.5*v))*(w^(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(x^(0.5*(v - 2)))/(v*x + w)^(0.5*(v + w))
    i = float(1 - sp.integrate(f, (x, 0, F)))
    print("\n3.p값 : %g" %i)
    print("\n4.유의수준 : %g" %a)
    
    if i < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else:
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 일원분산분석에서의 F통계량 가설 검정 (표 : 검정통계량과 기각역)

# In[166]:


def FAOVcr(a,*A) :
    F = round(Fstt(*A),17)
    print("1.검정통계량 : %g" %F)
    
    v = len(A) - 1 
    w = sum(map(len,A)) - len(A) 
    print("\n2.두 자유도 : %g, %g" %(v,w))
    
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    
    cr = df['%g' %(v)][int(w)]           
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    if cr < F :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 일원분산분석에서의 F통계량 가설검정 (함수 & 표)

# In[167]:


def FAOV(a,*A) :

    F = round(Fstt(*A),17)
    print("1.검정통계량 : %g" %F)
    
    v = len(A) - 1 
    w = sum(map(len,A)) - len(A) 
    print("\n2.두 자유도 : %g, %g" %(v,w))
    
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    cr = df['%g' %(v)][int(w)]           
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    x = sp.symbols('x')
    f = (v^(0.5*v))*(w^(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(x^(0.5*(v - 2)))/(v*x + w)^(0.5*(v + w))
    i = float(1 - integral(f,x,0,F))
    print("\n3.p값 : %g" %i)
    print("\n4.유의수준 : %g" %a)
    
    if i < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else:
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 일원분산분석표

# In[168]:


# 'A': 집단 자료 (리스트 or pd.Series 형태)
def AOVtbl(*A) :
    A = pd.DataFrame({'변동요인' : ['처리', '오차', '총계'],
                  '자유도     ' : [len(A) - 1, sum(map(len, A)) - len(A), sum(map(len, A)) - 1],
                  '제곱합        ' : [SSTR(*A), SSE(*A), SST(*A)],
                  '평균제곱합             ' : [MSTR(*A), MSE(*A), ''],
                  'F통계량                ' : [Fstt(*A), '', '']},
                index = ['','',''])
    return A


# ### 일원분산분석의 수행 절차

# #### 일원분산분석의 수행 절차(함수: p값과 유의수준)

# In[169]:


def Ow_AOVp(a,*A) :

    print('1.유의수준 : %g' %a)
    print('\n2.일원분산분석표 : \n\n',AOVtbl(*A))
    
    F = round(Fstt(*A),17)
    v = len(A) - 1
    w = sum(map(len,A)) - len(A)
    print("\n3.두 자유도 : %g, %g" %(v,w))
    
    x = sp.symbols('x')
    f = (v^(0.5*v))*(w^(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(x^(0.5*(v - 2)))/(v*x + w)^(0.5*(v + w))
    i = 1 - integral(f,x,0,F)  
    print('\n4.F 통계량 : %g' %F)
    print('\n5.p값 : %g' %i)
    
    if i < a:
        ans = "[결과] : 귀무가설을 기각한다."
    else:
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 일원분산분석의 수행 절차(표: 검정통계량과 기각역)

# In[170]:


def Ow_AOVcr(a,*A) :

    print('1.유의수준 : %g' %a)
    print('\n2.일원분산분석표 : \n\n',AOVtbl(*A))
    
    F = round(Fstt(*A),17)
    v = len(A) - 1
    w = sum(map(len,A)) - len(A)
    print("\n3.두 자유도 : %g, %g" %(v,w))
    print('\n4.F 통계량 : %g' %F)
    
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    cr = df['%g' %(v)][int(w)]           
    print("\n5.임계값 : %g" %cr)                                    
    print("\n6.기각역 : (%g, oo)" %cr)
    
    if cr < F :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 일원분산분석의 수행 절차(함수 & 표)

# In[171]:


def Ow_AOV(a,*A) :
    
    print('[귀무가설] : 각 모집단의 평균들은 유의한 차이가 없다. \n[대립가설] : 각 모집단의 평균들 중 유의한 차이가 존재한다.')
    print('\n1.일원분산분석표 : \n\n',AOVtbl(*A))
    
    F = round(Fstt(*A),17)
    v = len(A) - 1
    w = sum(map(len,A)) - len(A)
    print("\n2.두 자유도 : %g, %g" %(v,w))
    
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    
    cr = df['%g' %(v)][int(w)] 
    print('\n3.F 통계량 : %g' %F)
    print("\n4.임계값 : %g" %cr)                                    
    print("\n5.기각역 : (%g, oo)" %cr)
    
    x = sp.symbols('x')
    f = (v^(0.5*v))*(w^(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(x^(0.5*(v - 2)))/(v*x + w)^(0.5*(v + w))
    i = 1 - integral(f,x,0,F)  
    print('\n6.p값 : %g' %i)
    print('\n7.유의수준 : %g' %a)   
    if i < a:
        ans = "[결과] : 귀무가설을 기각한다."
    else:
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ### 다중비교
# - 일원분산분석 결과 귀무가설이 기각되어 모집단의 평균 중에는 차이가 존재한다고 결론을 내리게 되면, 그 차이를 보이는 모집단이 어떤 것들인지에 대한 분석이 추가적으로 필요하다. 이러한 분석절차를 다중비교(multiple comparison)라고 한다. 

# #### 스튜던트화 범위(Studentized range) 분포상의 q값

# In[172]:


# 유의수준은 0.01과 0.05만 가능
def q(*A) :
    a = float(input('유의수준은 0.05 또는 0.01 만 가능합니다. \n유의수준 : '))
    df = pd.read_csv('./Studentized Range q Table(%g).csv' %a, encoding='euc-kr',index_col=0)
    return df[str(len(A))][int(sum(map(len, A)) - len(A))]


# #### 다중비교 신뢰구간

# In[173]:


def q_ci(*A) :
    i = int(input("i ==> ")) - 1
    j = int(input("j ==> ")) - 1
    x = int(len(A[i]))
    y = int(len(A[j]))
    q1 = q(*A)
    return Mean(A[i]) - Mean(A[j]) - round(q1/sqrt(2),5)*sqrt(MSE(*A)*(1/x + 1/y)), Mean(A[i])-Mean(A[j]) + round(q1/sqrt(2),5)*sqrt(MSE(*A)*(1/x + 1/y))


# #### Tukey의 다중비교 방법

# In[174]:


# 속도 수정
def Tukey(a, *x):
    m = list(map(Mean, x))
    n = list(map(len, x))
    print('1.유의수준 : {0}({1}%), 신뢰수준 : {2}({3}%)'.format(float(a), int(a * 100), float(1 - a), int((1 - a) * 100)))

    df = pd.read_csv('./Studentized Range q Table(%g).csv' % a, encoding='euc-kr', index_col=0)
    q = df[str(len(x))][int(sum(n) - len(x))]
    print('\n2.모집단 개수 : {0}, 자유도 : {1}, q값 : {2}'.format(len(x), sum(n) - len(x), q))
    print('\n3.구간에 대한 평균 비교 결과 :\n')

    dfempty = pd.DataFrame(index=range(2, len(m) + 1), columns=range(1, len(m)))

    indices = [(i, j) for i in range(1, len(m) + 1) for j in range(i + 1, len(m) + 1)]
    results = list(map(lambda ij: (ij[1], ij[0], round(m[ij[0] - 1] - m[ij[1] - 1] - q * sqrt(MSE(*x) * (1 / n[ij[0] - 1] + 1 / n[ij[1] - 1]) / 2), 2), round(m[ij[0] - 1] - m[ij[1] - 1] + q * sqrt(MSE(*x) * (1 / n[ij[0] - 1] + 1 / n[ij[1] - 1]) / 2), 2)), indices))
    
    for j, i, minus, plus in results:
        dfempty.loc[j:j, int(i)] = str((minus, plus))
        if 0 in range(floor(minus), ceil(plus)):
            print('  {0}번째와 {1}번째의 모평균은 서로 다르지 않고,'.format(i, j))
    
    print('  그 외에 다른 것들의 모평균은 유의적으로 차이가 있다고 결론 내릴 수 있다.')
    print('\n4.신뢰구간 표 : \n', dfempty)

    return print('\n5.결과 : 이와 같은 결론은 {0}% 신뢰도를 가진다.'.format(int((1 - a) * 100)))

### 여기서부터 yoon 수정중(24.10.24)
# ### 이원분산분석
# - 영향을 미치는 요인이 두 가지인 경우의 분산분석
# - 여기서부터는 입력값을 먼저 데이터프레임으로 설정

# #### 총제곱합 SST = 일원분산분석의 총제곱합과 동일

# In[175]:


# 입력값: 데이터프레임 내에서 열 값
def SST(*A) :
    x = sum(map(sum,A))/sum(map(len,A))
    return float(sum(map(lambda a : sum(map(lambda a1 : (a1 - x)**2, a)), A)))


# #### 요인1 처리제곱합 SSTR1

# In[176]:


# 입력값: 데이터프레임 내에서 열 값
def SSTR1(*A) :
    x = sum(map(sum, A))/sum(map(len, A))
    return sum(map(lambda a : len(a)*(Mean(a) - x)**2, A))


# #### 요인2 처리제곱합 SSTR2  [수정함]

# In[177]:


# 입력값: 데이터프레임 내에서 행 값
def SSTR2(*B):
    if isinstance(B[0], pd.DataFrame):
        # 모든 DataFrame에서 숫자만 추출하여 합산
        total_sum = sum(b.values.sum() for b in B)
        # 전체 평균 x 계산
        x = total_sum / (len(B[0]) * B[0].shape[1] * len(B))
        
        # 편차 제곱 합계 계산
        return sum(map(lambda b: ((b.values.sum() / (len(b) * b.shape[1])) - x) ** 2, B)) * B[0].shape[1] * len(B[0])
    
    else:
        # DataFrame이 아닌 경우 리스트 등의 경우
        x = sum(map(sum, B)) / sum(map(len, B))
        return sum(map(lambda b: len(b) * (Mean(b) - x) ** 2, B))


# #### 상호작용제곱합 SSINT [수정함]

# In[178]:


# 입력값: 데이터프레임 내에서 행 값
def SSINT(*B):
    # 요인1: 자동차 요인2: 제조사 
    if isinstance(B[0], pd.DataFrame):
        # 전체 평균
        total_sum = sum(b.values.sum() for b in B)
        x = total_sum / (len(B[0]) * B[0].shape[1] * len(B))
        # 요인1의 각 평균
        y = sum(b.values.sum(axis=0) for b in B) / (len(B) * len(B[0]))
        # 요인2의 각 평균
        z = [b.mean().mean() for b in B]
        #상호작용제곱합
        ssint = 0
        for i in range(len(z)):
                # 요인1과 요인2의 평균
                w = sum(map(lambda x: x, B[i].values)) / len(B[i])
                ssint += sum(map(lambda y_val, w_val: (w_val - y_val - z[i] + x)**2, y, w))
        return len(B[0]) * ssint
    
    else:
        x = sum(map(sum,B)) / (len(B[0])*len(B)) # 모든 표본의 평균 #len(B[0]):열의 갯수 #len(B): 행의 갯수
        y = list(map(lambda b: sum(b)/len(b),B)) # 요인2의 각 그룹의 평균 (행)
        z = sum(map(lambda b: b.values,B)) / len(B) # 요인1의 각 그룹의 평균 (열)
        return sum(sum(map(lambda b,y,z:b-y-z+x,B,y,z)))


# #### 이원분산분석 오차제곱합 SSE2

# In[179]:


# A = 요인 1 (소형자동차, 준중형자동차, 중형자동차, 대형자동차)
# B = 요인 2 (제조사 A, 제조사 B)
def SSE2(A = [ ], B = [ ]) : 
    return SST(*A) - SSTR1(*A) - SSTR2(*B) - SSINT(*B)    


# #### 요인 1 처리 평균제곱합 MSTR1

# In[180]:


# A = 요인 1 (소형자동차, 준중형자동차, 중형자동차, 대형자동차)
def MSTR1(*A) :
    return SSTR1(*A) / (len(A) - 1)


# #### 요인 2 처리 평균제곱합 MSTR2

# In[181]:


# B = 요인 2 (제조사 A, 제조사 B)
def MSTR2(*B) :
    return SSTR2(*B) / (len(B) - 1)


# #### 상호작용평균제곱합 MSINT [수정함]

# In[182]:


# B = 요인 2 (제조사 A, 제조사 B)
def MSINT(*B):
    if isinstance(B[0], pd.DataFrame):
        return SSINT(*B)/((B[0].shape[1] - 1)*(len(B)-1))
    else:
        return SSINT(*B)/((len(B[0]) - 1)*(len(B)-1))


# #### 이원분산분석 오차평균제곱합 MSE2 [수정함]

# In[183]:


# A = 요인 1 (소형자동차, 준중형자동차, 중형자동차, 대형자동차)
# B = 요인 2 (제조사 A, 제조사 B)
def MSE2(A = [ ], B = [ ]) : 
    if isinstance(B[0], pd.DataFrame):
        return SSE2(A,B) / (len(A)*len(B)*(len(B[0]) - 1))
    else:
        return SSE2(A,B) / (len(A)*len(B))


# #### 요인의 유의성 검정
# - 한 요인이 가지는 평균에 미치는 영향이 다른 요인의 처리 그룹에 따라 달라지는 경우를 상호작용이 존재한다고 함.
# - 1. 상호작용의 효과에 대한 유의성 검정을 먼저 수행
# - 2. 상호작용의 효과가 유의적이지 않다면 각 요인에 대한 주효과의 검증을 수행할 수 있음

# #### 요인 1에 대한 F통계량 F_statistic_factor1 =  MSTR1/MSE2

# In[184]:


# A = 요인 1 (소형자동차, 준중형자동차, 중형자동차, 대형자동차)
# B = 요인 2 (제조사 A, 제조사 B)
def Fstt1(A = [ ], B = [ ]) :
    return MSTR1(*A)/MSE2(A, B)


# #### 요인 2에 대한 F통계량 F_statistic_factor2 = MSTR2/MSE2

# In[185]:


# A = 요인 1 (소형자동차, 준중형자동차, 중형자동차, 대형자동차)
# B = 요인 2 (제조사 A, 제조사 B)
def Fstt2(A = [ ], B = [ ]) :
    return MSTR2(*B)/MSE2(A, B)


# #### 상호작용에 대한 F통계량 F_interaction = MSINT/MSE2

# In[186]:


# A = 요인 1 (소형자동차, 준중형자동차, 중형자동차, 대형자동차)
# B = 요인 2 (제조사 A, 제조사 B)
def Fint(A = [ ], B = [ ]) :
    return MSINT(*B)/MSE2(A, B)


# #### 분산분석표 [수정함]

# In[187]:


# A = 요인 1 (소형자동차, 준중형자동차, 중형자동차, 대형자동차)
# B = 요인 2 (제조사 A, 제조사 B)
def AOVtbl2(A = [ ], B = [ ]) :
    if isinstance(B[0], pd.DataFrame):
        A = pd.DataFrame({'변동요인' : ['요인1', '요인2', '상호작용', '오차', '총계'],
                          '자유도     ' : [len(A) - 1, len(B) - 1, '%g  '%((len(A) - 1)*(len(B) - 1)), len(A)*len(B)*(len(B[0]) - 1), len(A)*len(B)*len(B[0]) - 1],
                          '제곱합        ' : [SSTR1(*A), SSTR2(*B), '%g  '%SSINT(*B), SSE2(A, B), SST(*A)],
                          '평균제곱합             ' : [MSTR1(*A), MSTR2(*B), '%g  '%MSINT(*B), MSE2(A, B), ''],
                          'F통계량                ' : [Fstt1(A,B), Fstt2(A,B), '%g  '%Fint(A,B), '', '']},
                         index = ['','','','',''])
    else:
        A = pd.DataFrame({'변동요인' : ['요인1', '요인2', '상호작용', '오차', '총계'],
                  '자유도     ' : [len(A) - 1, len(B) - 1, '%g  '%((len(A) - 1)*(len(B) - 1)), len(A)*len(B), len(A)*len(B) - 1],
                  '제곱합        ' : [SSTR1(*A), SSTR2(*B), '%g  '%SSINT(*B), SSE2(A, B), SST(*A)],
                  '평균제곱합             ' : [MSTR1(*A), MSTR2(*B), '%g  '%MSINT(*B), MSE2(A, B), ''],
                  'F통계량                ' : [Fstt1(A,B), Fstt2(A,B), '%g  '%Fint(A,B), '', '']},
                 index = ['','','','',''])
    return A


# ### 이원분산분석의 수행 절차
# - 함수가 아닌 표로 진행하는 코드 추가 必
# - 일원분산분석과 마찬가지로 F통계량이 충분히 커야 귀무가설을 기각하게 되므로 사용되는 가설검정 방법은 항상 우측검정

# In[188]:


# A = 요인 1 (소형자동차, 준중형자동차, 중형자동차, 대형자동차)
# B = 요인 2 (제조사 A, 제조사 B)
def Tw_AOV(a, A = [ ], B = [ ]) :
    print('가정사항: (1) 독립적인 표본  (2) 모집단의 정규성  (3) 모집단의 등분산성')
    print('\n1.[귀무가설1] 요인1과 요인2의 상호작용은 없다.',
          '\n  [대립가설1] 요인1과 요인2의 상호작용은 있다.',
          '\n\n  [귀무가설2] 요인1의 처리 집단별 평균차이는 없다.',
          '\n  [대립가설2] 요인1의 처리 집단별 평균차이는 있다.',
          '\n\n  [귀무가설3] 요인2의 처리 집단별 평균차이는 없다.',
          '\n  [대립가설3] 요인2의 처리 집단별 평균차이는 있다.')
    print('\n2.이원분산분석표 :\n\n', AOVtbl2(A,B))
    
    df = pd.read_csv('./F분포표(%g).csv' % a, index_col=0)  
    
    dfint = (len(A) - 1)*(len(B) - 1)
    if isinstance(B[0], pd.DataFrame):
        dferr = len(A)*len(B)*(len(B[0]) - 1)
    else:
        dferr = len(A)*len(B)
        
    F = round(Fint(A,B),17)
    x = sp.symbols('x')
    fint = (dfint**(0.5*dfint))*(dferr**(0.5*dferr))*(math.gamma((dfint+dferr)/2))/(math.gamma(0.5*dfint)*math.gamma(0.5*dferr))*(x**(0.5*(dfint-2)))/(dfint*x+dferr)**(0.5*(dfint+dferr))
    fint_num = sp.lambdify(x, fint, 'numpy')
    iinte, error = spi.quad(fint_num, 0, F)
    iint = round(1 - iinte, 4)
    cr = df['%g' % dfint][int(dferr)] 
    
    print('%-15s' %'\n3.상호작용 F통계량 : ','%g' %F)
    print('%-15s' %'  유의수준 : ', '  %g' %a)
    print('%-15s' %'  상호작용의 p값 : ' , iint)
    print('%-15s' %'  임계값 : %g' %cr)                                    
    print('%-15s' %'  기각역: (%g, oo)' %cr)
    
    if iint < a:
        ans = '\n[결과] : [상호작용에 대한 귀무가설1]을 기각한다. 따라서 두 요인의 상호작용이 있다.'
    else :
        ans = '\n[결과] : [상호작용에 대한 귀무가설1]을 기각하지 못한다. 따라서 두 요인의 상호작용이 없다. '
        
        df1 = len(A) - 1                                   
        df2 = len(B) - 1
        F1 = round(Fstt1(A,B),17)
        F2 = round(Fstt2(A,B),17)
        cr_a = df['%g' % df1][int(dferr)]   
        cr_b = df['%g' % df2][int(dferr)]   
        
        f1 = (df1**(0.5*df1))*(dferr**(0.5*dferr))*(math.gamma((df1+dferr)/2))/(math.gamma(0.5*df1)*math.gamma(0.5*dferr))*(x**(0.5*(df1-2)))/(df1*x+dferr)**(0.5*(df1+dferr))
        f1_num = sp.lambdify(x, f1, 'numpy')
        i1e, error = spi.quad(f1_num, 0, F1)
        i1 = round(1 - i1e, 4)
                      
        print('%-17s'%'\n4.요인1 F통계량 : ','%g' %F1)
        print('%-17s'%'  유의수준 : ', '%g' %a)
        print('%-17s'%'  요인1의 p값 : ' , i1)
        print('%-15s' %'  임계값 : %g' %cr_a)                                    
        print('%-15s' %'  기각역: (%g, oo)'%cr_a)
        
        f2 = (df2**(0.5*df2))*(dferr**(0.5*dferr))*(math.gamma((df2+dferr)/2))/(math.gamma(0.5*df2)*math.gamma(0.5*dferr))*(x**(0.5*(df2-2)))/(df2*x+dferr)**(0.5*(df2+dferr))
        f2_num = sp.lambdify(x, f2, 'numpy')
        i2e, error = spi.quad(f2_num, 0, F2)
        i2 = round(1 - i2e, 4)

        print('%-17s'%'\n  요인2 F통계량 : ','%g' %F2)
        print('%-17s'%'  유의수준 : ', '%g' %a)
        print('%-17s'%'  요인2의 p값 : ' , i2)
        print('%-15s' %'  임계값 : %g' %cr_b)                                    
        print('%-15s' %'  기각역: (%g, oo)'%cr_b)
        
        if i1 < a :
            ans = ans + '\n         [요인1에 대한 귀무가설2]를 기각한다. '
        else :
            ans = ans + '\n         [요인1에 대한 귀무가설2]를 기각하지 못한다. '
            
        if i2 < a :
            ans = ans + '\n         [요인2에 대한 귀무가설3]을 기각한다. '
        else :
            ans = ans + '\n         [요인2에 대한 귀무가설3]을 기각하지 못한다. '    
        
    return print(ans)


# ### 확률화블록설계
# - 완전확률화실험: 연구의 대상이 되는 개체들이 모든 가능한 처리 그룹에 확률적으로 할당되는 실험
# - 실제로 처리 그룹 간에 평균의 차이가 있을지라도 외부요인에 의한 변동으로 인해 오차항의 변동이 실제보다 더 커지게 되어, 유의적인 결과를 얻지 못할 수 있다.
# - 확률화블록설계: 연구의 대상이 되는 개체들에 대한 외생변수를 고려하여 이러한 변동을 어느 정도 제어함으로써 보다 정확한 결론을 내리는 데 사용
# - 행은 블록에 해당, 열은 요인에 해당
# - 확률화블록설계하에서의 분산분석은 블록을 통해 외생변수에 의한 변동을 제어한 뒤, 요인수준에 따라 비교대상이 되는 모집단 간의 평균에 차이가 있는지를 분석하는 것을 목표

# #### 총제곱합 SST = 일원분산분석의 총제곱합과 동일

# In[189]:


# 입력값: 데이터프레임 내에서 열 값 (요인)
def SST(*A) :
    x = sum(map(sum,A))/sum(map(len,A))
    return float(sum(map(lambda a : sum(map(lambda a1 : (a1 - x)**2, a)), A)))


# #### 처리제곱합 SSTR = 일원분산분석의 처리제곱합과 동일

# In[190]:


# 입력값: 데이터프레임 내에서 열 값
def SSTR(*A) :
    x = sum(map(sum, A))/sum(map(len, A))
    return sum(map(lambda a : len(a)*(Mean(a) - x)**2, A))


# #### 블록제곱합 SSB

# In[191]:


# 입력값: 데이터프레임 내에서 행 값 (블록)
def SSB(*B) :
    x = sum(map(sum, B))/sum(map(len, B))
    return sum(map(lambda b : len(b)*(Mean(b) - x)**2, B))


# #### 오차제곱합 SSEB

# In[192]:


# 입력값-'A':데이터프레임 내에서 열 값(요인),'B':데이터프레임 내에서 행 값(블록) 
def SSEB(A = [ ], B = [ ]) :
    return SST(*A) - SSTR(*A) - SSB(*B)


# #### 처리평균제곱합 MSTR = 일원분산분석의 처리평균제곱과 동일

# In[193]:


# 입력값: 데이터프레임 내에서 열 값
def MSTR(*A) :                  
    return SSTR(*A)/(len(A) - 1)


# #### 블록평균제곱합 MSB

# In[194]:


# 입력값: 데이터프레임 내에서 행 값
def MSB(*B) :
    return SSB(*B)/(len(B) - 1)


# #### 오차평균제곱합 MSEB 

# In[195]:


# 입력값-'A':데이터프레임 내에서 열 값(요인),'B':데이터프레임 내에서 행 값(블록) 
def MSEB(A = [ ], B = [ ]) :
    return SSEB(A,B)/((len(A)-1)*(len(B)-1))


# #### 요인처리F통계량 F_statistic_randomized = 처리평균제곱합(MSTR) / 오차평균제곱합(MSE)
# - 확률화블록설계하의 분산분석에서는 블록을 통해 외생변수에 의한 변동을 제어한 뒤 요인에 대한 효과에 대해 검정을 하게 됨.(열 값)
# - 귀무가설인 평균은 유의한 차이가 없다를 기각하는 것에 의의.

# In[196]:


def Fsttrd(A = [ ], B = [ ]) :
    return MSTR(*A) / MSEB(A,B)


# #### 블록 F통계량 F_statistic_block = 블록평균제곱합(MSB) / 오차평균제곱합(MSE)
# - 블록은 오차평균제곱합에서 외생변수로 인한 변동을 제거하기 위해 정의된 것이므로, 블록별 평균 간의 차이가 있다는 것은 이미 가정된 것이고 이를 검정하는 것이 목표가 되지 않음.
# - 하지만 앞으로의 실험에서 같은 종류의 블록을 정의하는 것이 적절한지를 살펴보기 위해, 블록별 평균 간의 차이에 대한 유의성을 검정할 수 있음.

# In[197]:


def Fsttb(A = [ ], B = [ ]) :
    return MSB(*B) / MSEB(A,B)


# #### 확률화블록설계 분산분석표

# In[198]:


def BAOVtbl(A = [ ], B = [ ]) :
    
    A = pd.DataFrame({'변동요인' : ['처리', '블록', '오차', '총계'],
                      '자유도   ' : [len(A) - 1, len(B) - 1, (len(A) - 1)*(len(B) - 1), len(A)*len(B) - 1],
                      '제곱합       ' : [SSTR(*A), SSB(*B), SSEB(A,B), SST(*A)],
                      '평균제곱합          ' : [MSTR(*A), MSB(*B), MSEB(A,B), ''],
                      'F통계량               ' : [Fsttrd(A,B), Fsttb(A,B), '', '']},
                     index = ['','','',''])
    
    return A


# #### 확률화블록설계 분산분석의 처리F통계량 검정(함수: p값과 유의수준)

# In[199]:


def Fsttrd_testp(a, A = [ ], B = [ ]) :

    v = len(A)-1                         # 처리자유도
    w = (len(A)-1)*(len(B)-1)            # 오차자유도
    Frd = round(Fsttrd(A, B),17)
    x = sp.symbols('x')
    f = (v**(0.5*v))*(w**(0.5*w))*(math.gamma((v + w)/2))/(math.gamma(0.5*v)*math.gamma(0.5*w))*(x**(0.5*(v - 2)))/(v*x + w)**(0.5*(v + w))
    i = 1 - sp.integrate(f,(x,0,Frd))    
    print('1.확률화블록설계 처리 F통계량 : %g' %Frd)
    print('\n2.p값 : %g' %i)
    print('\n3.유의수준 : %g' %a)
    
    if i < a:
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 확률화블록설계 분산분석의 처리F통계량 검정 (표: 검정통계량과 기각역)

# In[200]:


def Fsttrd_testcr(a, A = [ ], B = [ ]) :

    v = len(A)-1                         # 처리자유도
    w = (len(A)-1)*(len(B)-1)            # 오차자유도
    Frd = round(Fsttrd(A, B),17)
    print('1.확률화블록설계 처리 F통계량 : %g' %Frd)
    print("\n2.처리자유도 : %g, 오차자유도 : %g" %(v,w))
    
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    cr = df['%g' %(v)][int(w)]           
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    if cr < Frd :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 확률화블록설계 분산분석의 처리F통계량 검정 (함수&표)

# In[201]:


def Fsttrd_test(a, A = [ ], B = [ ]) :

    v = len(A)-1                         # 처리자유도
    w = (len(A)-1)*(len(B)-1)            # 오차자유도
    Frd = round(Fsttrd(A, B),17)
    print('1.확률화블록설계 처리 F통계량 : %g' %Frd)
    print("\n2.처리자유도 : %g, 오차자유도 : %g" %(v,w))
    
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    cr = df['%g' %(v)][int(w)]           
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    x = sp.symbols('x')
    f = (v**(0.5*v))*(w**(0.5*w))*(math.gamma((v + w)/2))/(math.gamma(0.5*v)*math.gamma(0.5*w))*(x**(0.5*(v - 2)))/(v*x + w)**(0.5*(v + w))
    i = 1 - sp.integrate(f,(x,0,Frd))    
    print('\n5.p값 : %g' %i)
    print('\n6.유의수준 : %g' %a)
    
    if cr < Frd :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 확률화블록설계 분산분석의 블록F통계량 검정에 대한 설명
# - 블록별 평균 간의 차이가 있어야 요인의 처리 집단별 평균 간의 차이를 검정할 수 있다.
# - 따라서 블록F통계량 검정을 통해 귀무가설을 기각하여 블록별 평균 간의 차이가 있다는 것을 보여야 한다.
# - 블록별 평균 간의 차이가 있다는 것을 가정한 상태에서 위의 처리F통계량 검정을 진행했지만 이제부터는 블록F통계량 검정을 진행한 후 처리F통계량 검정을 진행해야한다.

# #### 확률화블록설계 분산분석의 블록F통계량 검정(함수: p값과 유의수준)

# In[202]:


def Fsttb_testp(a, A = [ ], B = [ ]) :

    v = len(B) - 1                         # 블록자유도
    w = (len(A)-1)*(len(B)-1)              # 오차자유도
    Fb = round(Fsttb(A, B),17)
    
    x = sp.symbols('x')
    f = (v**(0.5*v))*(w**(0.5*w))*(math.gamma((v + w)/2))/(math.gamma(0.5*v)*math.gamma(0.5*w))*(x**(0.5*(v - 2)))/(v*x + w)**(0.5*(v + w))
    f_num = sp.lambdify(x, f, 'numpy')
    ie, error = spi.quad(f_num, 0, Fb)
    i = 1 - ie    
    print('1.확률화블록설계 블록 F통계량 : %g' %Fb)
    print('\n2.p값 : %g' %i)
    print('\n3.유의수준 : %g' %a)
    
    if i < a:
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 확률화블록설계 분산분석의 블록F통계량 검정 (표: 검정통계량과 기각역)

# In[203]:


def Fsttb_testcr(a, A = [ ], B = [ ]) :

    v = len(B) - 1                         # 블록자유도
    w = (len(A)-1)*(len(B)-1)              # 오차자유도
    Fb = round(Fsttb(A, B),17)
    
    print('1.확률화블록설계 블록 F통계량 : %g' %Fb)
    print("\n2.블록자유도 : %g, 오차자유도 : %g" %(v,w))
    
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    cr = df['%g' %(v)][int(w)]           
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    if cr < Fb :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 확률화블록설계 분산분석의 블록F통계량 검정 (함수 & 표)

# In[204]:


def Fsttb_test(a, A = [ ], B = [ ]) :

    v = len(B) - 1                         # 블록자유도
    w = (len(A)-1)*(len(B)-1)              # 오차자유도
    Fb = round(Fsttb(A, B),17)
    
    print('1.확률화블록설계 블록 F통계량 : %g' %Fb)
    print("\n2.블록자유도 : %g, 오차자유도 : %g" %(v,w))
    
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    cr = df['%g' %(v)][int(w)]           
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    x = sp.symbols('x')
    f = (v**(0.5*v))*(w**(0.5*w))*(math.gamma((v + w)/2))/(math.gamma(0.5*v)*math.gamma(0.5*w))*(x**(0.5*(v - 2)))/(v*x + w)**(0.5*(v + w))
    f_num = sp.lambdify(x, f, 'numpy')
    ie, error = spi.quad(f_num, 0, Fb)
    i = 1 - ie  
    print('\n5.p값 : %g' %i)
    print('\n6.유의수준 : %g' %a)
    
    if cr < Fb :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# #### 확률화블록설계 분산분석 최종(처리F통계량 & 분산분석표)

# In[205]:


def B_AOV(a, A = [ ], B = [ ]) :
    
    print('[귀무가설] : 각 모집단의 평균들은 유의한 차이가 없다. \n[대립가설] : 각 모집단의 평균들 중 유의한 차이가 존재한다.')  
    print('\n1.확률화블록설계 후 분산분석표 : \n\n', BAOVtbl(A,B))
    
    v = len(A)-1                         # 처리자유도
    w = (len(A)-1)*(len(B)-1)            # 오차자유도
    Frd = round(Fsttrd(A, B),17)
    print('\n2.확률화블록설계 처리 F통계량 : %g' %Frd)
    print("\n3.처리자유도 : %g, 오차자유도 : %g" %(v,w))
    
    df = pd.read_csv('./F분포표(%g).csv' %a, index_col=0)
    cr = df['%g' %(v)][int(w)]           
    print("\n4.임계값 : %g" %cr)                                    
    print("\n5.기각역 : (%g, oo)" %cr)
    
    x = sp.symbols('x')
    f = (v**(0.5*v))*(w**(0.5*w))*(math.gamma((v + w)/2))/(math.gamma(0.5*v)*math.gamma(0.5*w))*(x**(0.5*(v - 2)))/(v*x + w)**(0.5*(v + w))
    i = 1 - sp.integrate(f,(x,0,Frd))    
    print('\n6.p값 : %g' %i)
    print('\n7.유의수준 : %g' %a)
    
    if cr < Frd :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# ---
# ---

# In[ ]:





# # 회귀분석
# - 두 변수 사이의 관계를 선형함수 관계로 분석하는 것이 회귀분석
# - 사회현상이나 자연현상에서 흔히 발생하는 관심사 중 하나가 어떤 속성이나 특성들에 대한 연관성 또는 함수적 관계를 파악하여 보고자 함.

# ## 단순선형회귀분석
# - 두 연속형 변수 간의 연관성이나 함수적 관계에 관해 논함.
# - 두 변수 간의 관계를 수학에서의 X와 Y 변수처럼 선형관계를 통계적으로 표현하는 단순선형회귀모형
# - X 변수가 하나인 경우를 단순선형회귀(simple linear regression)
# - 여러 개인 경우를 다중선형회귀(multiple linear regression)
# - Y변수: 반응변수, 종속변수
# - X변수(Y변수를 설명하기 위함): 설명변수, 예측변수, 독립변수
# - 회귀식(regression equation): 반응변수가 설명변수에 어떻게 연관되어 있는지 나타낸 식

# ### 단순선형회귀

# #### 단순선형회귀모형

# In[206]:


# 입력값 'x': 설명변수, 'y': 반응변수 (모두 리스트 형태) (B0, B1: 모수여서 입력값으로 받아야 함.)
def simple_linear_Reg_model(x, y, B0, B1):

    print(f"단순선형회귀식: y = {B0:.2f} + {B1:.2f}x")
    
    if B1 > 0:
        print("기울기가 양수이므로 x와 y는 양의 선형 관계에 있습니다.")
    elif B1 < 0:
        print("기울기가 음수이므로 x와 y는 음의 선형 관계에 있습니다.")
    else:
        print("기울기가 0이므로 x와 y는 아무런 연관성이 없습니다.")
        
    return B0, B1


# #### 단순선형회귀식

# In[207]:


# 입력값 'x': 설명변수, 'y': 반응변수 (모두 리스트 형태) (B0, B1: 모수여서 입력값으로 받아야 함.)
def simple_linear_Reg_equation(x, y, B0, B1):
    B0, B1 = simple_linear_Reg_model(x, y, B0, B1)
    return B0 + B1 * Mean(x)


# ### 최소제곱추정법
# - 회귀분석의 목적은 회귀식 E(Y)=β_0+β_1X에서 미지의 모수 β_0,β_1을 추정하는 것
# - b_0, b_1을 β_0,β_1의 추정값이라고 가정하면 추정된 단순선형회귀식을 나타낼 수 있다.

# #### 추정된 단순선형회귀식(& 최소제곱추정법)

# In[208]:


# 입력값 'x': 설명변수, 'y': 반응변수 (모두 리스트 형태)
def est_sl_Reg_equation(x, y):
    n = len(x)
   
    # 최소 제곱법을 이용하여 기울기(b) 계산
    numerator = 0
    denominator = 0
    
    for i in range(n):
        numerator += (x[i] - Mean(x)) * (y[i] - Mean(y))
        denominator += (x[i] - Mean(x)) ** 2
    
    b = numerator / denominator #β_1: 기울기
    a = Mean(y) - b * Mean(x) #β_0: 절편
    #print(f"단순선형회귀식: y = {a:.2f} + {b:.2f}x")
    
    #if b > 0:
    #    print("기울기가 양수이므로 x와 y는 양의 선형 관계에 있습니다.")
    #elif b < 0:
    #    print("기울기가 음수이므로 x와 y는 음의 선형 관계에 있습니다.")
    #else:
    #    print("기울기가 0이므로 x와 y는 아무런 연관성이 없습니다.")
        
    return a, b


# ### 단순회귀모형의 가정사항
# - 회귀모형의 가정사항은 설명변수와 반응변수의 함수적 연관성을 표현하는 회귀방정식과 회귀식이 설명할 수 없는 오차에 관한 내용을 포함
# - 1. 오차항(ε_i)의 평균은 0이고 분산은 σ^2이다. (등분산 가정)
# - 2. 오차항(ε_i)들은 서로 독립이다.
# - 3. 오차항(ε_i)은 정규분포를 따른다.

# ##### 1. 오차항(ε_i)의 평균은 0이고 분산은 σ^2이다. (등분산 가정)
# - 잔차의 산포도를 통해 등분산성을 확인
# - 잔차의 산포도가 일정하게 분포되어 있다면 등분산성을 만족한다고 할 수 있다.

# ##### 예측함수

# In[209]:


def predict(a, b, x):
    return a + b * x


# ##### 잔차계산함수

# In[210]:


# 입력값 수정
def residuals(x, y):
    a, b = est_sl_Reg_equation(x, y)
    return [y[i] - predict(a, b, x[i]) for i in range(len(x))]


# ##### 잔차의 산포도 그리기 함수

# In[211]:


# 입력값 'x': 설명변수, 'y': 반응변수, residuals': 각 설명변수에 대한 잔차, 'x_label': 설명변수의 축 이름(영어만 가능)
def plot_residuals(x, y, x_label):
    a, b = est_sl_Reg_equation(x, y)
    residual = residuals(x, y)
    plt.figure(figsize=(4.5, 3))
    plt.scatter(x, residual, marker='o', color='blue', s=10)
    plt.axhline(y=0, color='red', linestyle='--', linewidth=0.7)
    font_size = 7
    plt.xlabel(x_label, fontsize=font_size)
    plt.ylabel('Residuals', fontsize=font_size)
    plt.xticks(fontsize=font_size)  
    plt.yticks(fontsize=font_size)  
    plt.show()


# ###### 여기서부터 입력값 형태 때문에 예시 적용도 함께 함 

# In[212]:




# ##### 2. 오차항(ε_i)들은 서로 독립이다.
# - 잔차들 간의 독립성을 확인하기 위해 잔차 산포도 그래프를 생성 및 확인

# ##### 잔차들 간의 산포도 함수

# In[213]:


#입력값 'residuals':잔차 리스트, 'variable' (list, optional): 잔차에 대응하는 변수 리스트 (기본값: None), 'variable_name' (str, optional): 변수(또는 축) 이름 (기본값: 'Variable')
def residual_independence_check(residuals, variable=None, variable_name='Variable'):
    if variable is None:
        variable = list(range(1, len(residuals) + 1))  # 변수가 제공되지 않으면 인덱스를 사용
    
    # 잔차들의 산포도 그래프 생성
    plt.figure(figsize=(4.5, 3))
    plt.scatter(variable, residuals, marker='o', color='blue', s=10)
    plt.axhline(y=0, color='red', linestyle='--', linewidth=0.7)
    font_size = 7
    plt.xlabel(variable_name, fontsize=font_size)
    plt.ylabel('Residuals', fontsize=font_size)
    plt.xticks(fontsize=font_size)  
    plt.yticks(fontsize=font_size)  
    plt.show()


# In[214]:


# ##### 3. 오차항(ε_i)은 정규분포를 따른다.

# In[215]:


#입력값 'residuals':잔차 리스트
def normality_test(residuals):
    n = len(residuals)
    mean_res = sum(residuals) / n
    std_res = math.sqrt(sum((x - mean_res) ** 2 for x in residuals) / n)
    
    w_stat = sum(((i + 1 - 0.5) / n - (residuals[i] - mean_res) / std_res) ** 2 for i in range(n))
    p_value = 1 - math.exp(-2 * w_stat / math.pi)
    
    alpha = 0.05  # 유의수준
    if p_value > alpha:
        print("잔차는 정규분포를 따릅니다.")
    else:
        print("잔차는 정규분포를 따르지 않습니다.")


# ### 회귀계수 유의성 검정
# - 설명변수와 반응변수의 선형관계에 대한 존재여부에 대하여 검정하려는 것
# - 만일 선형관계가 없다면 회귀계수 β_1의 값이 0일 것이며, 그렇게 되면 회귀식에서 설명변수는 없어지고 반응변수 하나만 남게 되어 더 이상 회귀식을 논할 이유가 없게 된다.
# - 그래서 β_1의 값이 0인지 아닌지에 관심을 갖게 됨.

# #### Y(반응변수)의 총제곱합 SST

# In[216]:


# 입력값 'y': 반응변수 리스트
def Y_SST(y):
    return sum(map(lambda yi: (yi - Mean(y))**2, y))


# #### Y의 총변동량 MST

# In[217]:


# 입력값 'y': 반응변수 리스트
def Y_MST(y):
    return (sum(map(lambda yi: (yi - Mean(y))**2, y))) / (len(y)-1)


# In[218]:




# #### Y의 회귀제곱합 SSR

# In[219]:


# 입력값 'x': 설명변수 리스트, 'y': 반응변수 리스트
def Y_SSR(x, y):
    a, b = est_sl_Reg_equation(x, y)
    return sum(map(lambda xi: (predict(a, b, xi) - Mean(y))**2, x))


# #### Y의 회귀변동량 MSR

# In[220]:


# 입력값 'x': 설명변수 리스트, 'y': 반응변수 리스트
def Y_MSR(x, y):
    a, b = est_sl_Reg_equation(x, y)
    return (sum(map(lambda xi: (predict(a, b, xi) - Mean(y))**2, x))) / 1


# In[221]:





# #### Y의 오차제곱합 SSE

# In[222]:


# 입력값 'x': 설명변수 리스트, 'y': 반응변수 리스트
def Y_SSE(x, y):
    a, b = est_sl_Reg_equation(x, y)
    return sum(map(lambda xi, yi: (yi-predict(a, b, xi))**2, x, y))


# #### Y의 오차변동량 MSE (모분산의 추정값)

# In[223]:


# 입력값 'x': 설명변수 리스트, 'y': 반응변수 리스트
def Y_MSE(x, y):
    a, b = est_sl_Reg_equation(x, y)
    return (sum(map(lambda xi, yi: (yi-predict(a, b, xi))**2, x, y))) / (len(x)-2)


# In[224]:





# #### 반응변수와 설명변수 사이에 선형 연관성 검정을 위한 F통계량

# In[225]:


# 입력값 'x': 설명변수 리스트, 'y': 반응변수 리스트
def simple_linear_F(x, y):
    return Y_MSR(x, y) / Y_MSE(x, y)


# #### 단순선형회귀모형의 분산분석표

# In[226]:


# 입력값 'x': 설명변수 리스트, 'y': 반응변수 리스트
def simple_linear_AOVtbl(x, y) :
    A = pd.DataFrame({'변동요인' : ['회귀', '잔차', '총계'],
                      '제곱합(SS)' : ['SSR', 'SSE', 'SST'],
                      '자유도     ' : [1, len(x) - 2, len(x) - 1],
                      '제곱평균(MS)        ' : [Y_MSR(x, y), Y_MSE(x, y), ''],
                      'F통계량                ' : [simple_linear_F(x, y), '', '']},
                     index = ['','',''])
    return A


# In[227]:





# #### 기울기(β_1)에 대한 유의성 t검정
# - 모수의 통계적 유의성 검정(가설에 의해 양측검정만 존재)
# - 귀무가설(H0): 설명변수 X가 반응변수 Y에 선형적으로 연관성이 없다.(β_1 = 0)
# - 대립가설(H1): 설명변수 X가 반응변수 Y에 선형적으로 연관성이 있다.(β_1 != 0)

# ##### 양측 t검정 (표: 검정통계량과 기각역)

# In[228]:


# 입력값 'a': 유의수준,'x': 설명변수 리스트, 'y': 반응변수 리스트
def Beta_T_Tscr(a, x, y) :
    
    df = pd.read_csv('./t분포표.csv', encoding='euc-kr', index_col=0) 
    
    _, b = est_sl_Reg_equation(x, y)
    S = math.sqrt(Y_MSE(x, y))
    S_b1 = S / math.sqrt(sum(map(lambda xi: (xi - Mean(x))**2, x)))
    T1 = b / S_b1
    
    print("1.검정통계량: %g" %T1)              
    print("\n2.자유도 :", len(x) - 2)
    
    cr = df["%g" %(a/2)][int(len(x) - 2)]
    print("\n3.임계값 : {0}, {1}".format(-cr,cr))
    print("\n4.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))
    
    if cr < abs(T1) :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# In[229]:





# ##### 양측 t검정(함수: p값과 유의수준)

# In[230]:


# 입력값 'a': 유의수준,'x': 설명변수 리스트, 'y': 반응변수 리스트
def Beta_T_Tsp(a, x, y) :

    _, b = est_sl_Reg_equation(x, y)
    S = math.sqrt(Y_MSE(x, y))
    S_b1 = S / math.sqrt(sum(map(lambda xi: (xi - Mean(x))**2, x)))
    t = b / S_b1
    
    print("1.검정통계량 : %g" %t)
    
    v = len(x) - 2                  
    print("\n2.자유도 :",v)
    
    z = sp.symbols('z')
    fint = (math.gamma((v+1)/2)/(math.sqrt(v*math.pi)*math.gamma(v/2)))*((1+(z**2)/v)**(-(v+1)/2))     
    fint_num = sp.lambdify(z, fint, 'numpy')
    iinte, error = spi.quad(fint_num, 0, abs(t))
    I = round(0.5 - iinte, 4)
         
    print("\n3.p값 : %g" %(I*2))
    print("\n4.유의수준 : %g" %a)
    
    if I < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# In[231]:





# #### 단순회귀모형에 대한 유의성 F검정
# - 반응변수와 설명변수 사이에 선형 연관성 또는 함수적 관계를 설정하여 모형화한 것이 타당하느냐에 대한 검정
# - β_1인 음수로 큰 값이거나 양수로 큰 값이거나 두 경우 모두 F값이 큰 값이 나오므로 여기서 F검정은 오른쪽 단측검정이다.
# - 귀무가설(H0): 설명변수 X가 반응변수 Y에 선형적으로 연관성이 없다.(β_1 = 0)
# - 대립가설(H1): 설명변수 X가 반응변수 Y에 선형적으로 연관성이 있다.(β_1 != 0)

# ##### 우측 F검정 (표: 검정통계량과 기각역)

# In[232]:


# 입력값 'a': 유의수준,'x': 설명변수 리스트, 'y': 반응변수 리스트
def Beta_F_Rcr(a, x, y) :
        
    df = pd.read_csv('./F분포표(%g).csv' %(a), index_col=0)
    
    F = Y_MSR(x, y) / Y_MSE(x, y)
    print("1.검정통계량 : %g" %F)
    print("\n2.두 자유도 : %g, %g" %(1, len(y) - 2))             
                                                                    
    cr = df['%g' %(1)][int(len(y) - 2)]           
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    if cr < F :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# In[233]:





# ##### 우측 F검정 (함수: p값과 유의수준)

# In[234]:


# 입력값 'a': 유의수준,'x': 설명변수 리스트, 'y': 반응변수 리스트
def Beta_F_Rp(a, x, y) :
        
    df = pd.read_csv('./F분포표(%g).csv' %(a), index_col=0)
    
    F = Y_MSR(x, y) / Y_MSE(x, y)
    print("1.검정통계량 : %g" %F)
    
    v = 1 
    w = len(y) - 2 
    print("\n2.두 자유도 : %g, %g" %(v,w))
    
    z = sp.symbols('z')
    f = (v**(0.5*v))*(w**(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(z**(0.5*(v - 2)))/(v*z + w)**(0.5*(v + w))
    i = 1 - sp.integrate(f,(z,0,F))
    print("\n3.p값 : %g" %i)
    print("\n4.유의수준 : %g" %a)
    
    if round(i,17) < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# In[235]:





# ### 결정계수
# - Y의 총변동량(SST) 중 추정된 회귀식이 설명하는 변동량(SSR)의 비중이 크면 클수록 회귀식이 원래의 자료를 잘 정리 요약하여 반영하고 있다고 할 수 있다.
# - Y의 총변동량(SST)에 대한 추정된 회귀식이 설명하는 변동량(SSR)의 비율을 결정계수(coefficient of determination)인 R^2로 표기한다.
# - 회귀모형의 적합성에 대한 중요한 판단 기준으로 사용한다.

# In[236]:


# 입력값 'x': 설명변수 리스트, 'y': 반응변수 리스트
def CodeR2(x, y):
    R2 = Y_SSR(x, y) / Y_SST(y)
    # R^2 값 해석
    if R2 == 1:
        print("R^2이 1이므로 추정된 회귀식이 총변동량의 모든 부분을 설명한다.")
    elif R2 > 0.7:
        print("R^2이 1에 가까우므로 추정된 회귀식이 총변동량의 많은 부분을 설명한다.")
    elif R2 > 0.3:
        print("R^2이 중간 정도의 값을 가지므로 추정된 회귀식이 총변동량을 적절히 설명한다.")
    else:
        print("R^2이 0에 가까우므로 추정된 회귀식이 총변동량을 적절하게 설명하지 못한다.")
    return R2


# In[237]:





# ### 회귀모형을 이용한 예측
# - 추정된 회귀식이 적절하다고 판단되면 x의 특정값에 대하여 y의 값을 추정 또는 예측할 필요가 생긴다.
# - 이 경우, 점추정과 구간추정을 고려할 수 있고,
# - 설명변수 X가 어떤 특정값 X=x0셈 값일 때 반응변수 Y의 평균은 구간추정인 신뢰구간으로 추정한다.

# #### 반응변수 평균 E(Y0)의 (1-α)100% 신뢰구간
# - 설명변수가 평균 Mean(x)에 가까울수록 신뢰구간의 폭이 작아지고, 평균 Mean(x)에 멀어질수록 신뢰구간의 폭이 커짐을 알 수 있다.
# - 평균 Mean(x)에서 너무 멀리 그리고 추정된 회귀식에 이용된 x의 범위를 많이 이탈하는 경우, 그 예측력에는 신뢰성이 떨어진다는 것을 의미한다.

# In[238]:


# 입력값 'alpha': 유의수준,'x': 설명변수 리스트, 'y': 반응변수 리스트, 'x0': 지정값
def E_con_interval(alpha, x, y, x0):
    df = pd.read_csv('./t분포표.csv', encoding='euc-kr', index_col=0) 
    a, b = est_sl_Reg_equation(x, y)
    y0 = predict(a, b, x0)
    s = math.sqrt(Y_MSE(x, y))
    Sy0 = s * math.sqrt(1 / len(x) + (x0-Mean(x))**2 / sum(map(lambda xi: (xi - Mean(x))**2, x)))
    cr = df["%g" %(alpha/2)][int(len(x) - 2)]
    return (y0 - cr*Sy0, y0 + cr*Sy0)


# In[239]:





# #### 개별 반응변수 값의 (1-α)100% 예측구간

# In[240]:


# 입력값 'alpha': 유의수준,'x': 설명변수 리스트, 'y': 반응변수 리스트, 'x0': 지정값
def E_pre_interval(alpha, x, y, x0):
    df = pd.read_csv('./t분포표.csv', encoding='euc-kr', index_col=0) 
    a, b = est_sl_Reg_equation(x, y)
    y0 = predict(a, b, x0)
    s = math.sqrt(Y_MSE(x, y))
    Sy0 = s * math.sqrt(1 + 1 / len(x) + (x0-Mean(x))**2 / sum(map(lambda xi: (xi - Mean(x))**2, x)))
    cr = df["%g" %(alpha/2)][int(len(x) - 2)]
    return (y0 - cr*Sy0, y0 + cr*Sy0)


# In[241]:





# ### 회귀모형 진단 및 처방
# - 최소제곱법에 의한 단순회귀추정식이 설명변수와 반응변수 사이의 연관성을 얼마나 잘 설명하고 있을까 하는 의문이 생기고 이러한 의문은 회귀모형의 점검 또는 진단에 관한 것이다.
# #### 회귀진단 항목
# - 1.모형의 선형성
# - 2.오차의 정규성, 등분산성, 독립성
# - 3.특잇값의 존재
# - 4.영향관찰값의 존재
# - 모형의 선형성의 적합 여부, 특잇값의 존재 여부, 영향력이 큰 관찰값의 존재 여부는 XY산점도에서 볼 수 있으므로 회귀분석 시작 시 산점도를 그리고 점검하여야 한다.

# #### i번째 잔차
# - 잔차 = 남아 있는 오차
# - 추정된 회귀식이 반응변수(Y) 관찰값을 설명하지 못하는 부분
# - 잔차 e_i는 ε_i에 대한 최상의 정보를 제공
# - 따라서 잔차를 이용하여 오차의 가정사항을 점검할 필요가 있고 만일 오차의 가정들이 만족되지 못할 경우 추정된 회귀식이 적절하지 못하다는 추론을 할 수 있는 근거가 된다. 
# - 잔차그림(잔차도)로 오차의 가정사항을 점검하고 어떠한 패턴을 보이고 있지 않는 경우 추정된 회귀식이 설명변수와 반응변수 간의 회귀모형을 적절하게 설명하는 이상적인 유형을 나타낸다.

# In[242]:


# 입력값 'x': 설명변수 리스트, 'y': 반응변수 리스트, 'i': 위치
def residuals_i(x, y, i):    
    a, b = est_sl_Reg_equation(x, y)
    return y[i] - predict(a, b, x[i])


# In[243]:





# In[244]:





# In[ ]:





# ## 다중선형회귀분석

# ### 다중선형회귀
# - 다중선형회귀모형은 2개 이상의 설명변수를 고려하여 반응변수를 설명하는 회귀모형
# - 회귀분석의 목적은 다중선형회귀식을 추정하는 것
# - 다중선형회귀식은 반응변수 Y의 기댓값을 추정

# #### 다중선형회귀모형

# In[245]:


# 속도 수정
# 입력값 'x': 설명변수, 'y': 반응변수 (모두 리스트 형태) (B: 모수여서 입력값으로 받아야 함.)
def multiple_linear_Reg_model(x, y, B):
    m = len(x)       # 설명변수의 수 (열의 수)
    n = len(x[0])    # 데이터 포인트의 수 (행의 수)

    # 다중선형회귀식
    equation_terms = [f"{B[0]:.2f}"] + list(map(lambda i: f"{B[i+1]:.2f}x{i+1}", range(m)))
    equation = " + ".join(equation_terms)
    print(f"다중선형회귀식: y = {equation}")
    
    # 기울기 (모수 B1, B2, ..., Bm)의 관계
    for i in range(1, m + 1):
        if B[i] > 0:
            print(f"x{i}의 기울기가 양수이므로 x{i}와 y는 양의 선형 관계에 있습니다.")
        elif B[i] < 0:
            print(f"x{i}의 기울기가 음수이므로 x{i}와 y는 음의 선형 관계에 있습니다.")
        else:
            print(f"x{i}의 기울기가 0이므로 x{i}와 y는 아무런 연관성이 없습니다.")
    
    return B


# In[246]:





# #### 다중선형회귀식

# In[247]:


# 속도 수정
# 입력값 'x': 설명변수, 'y': 반응변수 (모두 리스트 형태) (B: 모수여서 입력값으로 받아야 함.)
def multiple_linear_Reg_equation(x, y, B):
    B = multiple_linear_Reg_model(x, y, B)
    m = len(B) - 1  # 설명변수의 수 (B0 제외)
    n = len(x[0])   # 데이터 포인트의 수 (행의 수)
    # 예측값(기댓값) 계산
    predictions = list(map(lambda j: B[0] + sum(B[i] * x[i - 1][j] for i in range(1, m + 1)), range(n)))
    return predictions


# In[248]:




# #### 추정된 다중선형회귀식(&최소제곱추정법)

# In[249]:


# 속도 수정(create_row)
def create_row(i, x_list):
    return [sp.Integer(1)] + list(map(lambda j: x_list[j][i], range(len(x_list))))

#입력값 'x_list': 설명변수 리스트, 'y': 반응변수
def est_mul_Reg_equation(x_list, y):
    X = list(map(lambda i: create_row(i, x_list), range(len(y))))

    X = matrix(X)
    y = vector(y)
    
    X_transpose = X.transpose()
    beta = (X_transpose * X).inverse() * X_transpose * y
    
    beta = list(map(lambda x: float(x.n(digits=7)), beta))
    
    equation_terms = list(map(lambda i_b: f"{i_b[1]}" if i_b[0] == 0 else f"{i_b[1]}(x^{i_b[0]})", enumerate(beta)))
    equation = " + ".join(equation_terms)
    # print(f"다중선형회귀식: y = {equation}")
    
    return beta


# In[250]:





# ### 유의성 검정

# #### i번째 관찰값의 추정된 다중선형회귀식에 대한 총제곱합 SST

# In[251]:


#입력값 'y': 반응변수
def Y_i_SST(y):
    return sum(map(lambda yi: (yi - Mean(y))**2, y))


# In[252]:



# #### i번째 관찰값의 추정된 다중선형회귀식에 대한 회귀제곱합 SSR

# In[253]:


# 속도 수정(create_row)
#입력값 'x_list': 설명변수 리스트, 'y': 반응변수
def Y_i_SSR(x_list, y):
    X = list(map(lambda i: create_row(i, x_list), range(len(y))))
    beta = est_mul_Reg_equation(x_list, y)
    y_pred = list(map(lambda i: sum(map(lambda j: beta[j] * X[i][j], range(len(beta)))), range(len(y))))
    return sum(map(lambda yi_pred: (yi_pred - Mean(y)) ** 2, y_pred))


# #### i번째 관찰값의 추정된 다중선형회귀식에 대한 회귀제곱평균 MSR

# In[254]:


# 속도 수정(create_row)
#입력값 'x_list': 설명변수 리스트, 'y': 반응변수
def Y_i_MSR(x_list, y):
    X = list(map(lambda i: create_row(i, x_list), range(len(y))))
    beta = est_mul_Reg_equation(x_list, y)
    y_pred = list(map(lambda i: sum(map(lambda j: beta[j] * X[i][j], range(len(beta)))), range(len(y))))
    return sum((yi_pred - Mean(y)) ** 2 for yi_pred in y_pred) / len(x_list)


# In[255]:





# #### i번째 관찰값의 추정된 다중선형회귀식에 대한 오차제곱합 SSE

# In[256]:


# 속도 수정(create_row)
#입력값 'x_list': 설명변수 리스트, 'y': 반응변수
def Y_i_SSE(x_list, y):
    X = list(map(lambda i: create_row(i, x_list), range(len(y))))
    beta = est_mul_Reg_equation(x_list, y)
    y_pred = list(map(lambda i: sum(map(lambda j: beta[j] * X[i][j], range(len(beta)))), range(len(y))))
    return sum((y[i] - y_pred[i]) ** 2 for i in range(len(y)))


# #### i번째 관찰값의 추정된 다중선형회귀식에 대한 오차평균제곱 MSE

# In[257]:


# 속도 수정(create_row)
#입력값 'x_list': 설명변수 리스트, 'y': 반응변수
def Y_i_MSE(x_list, y):
    X = list(map(lambda i: create_row(i, x_list), range(len(y))))
    beta = est_mul_Reg_equation(x_list, y)
    y_pred = list(map(lambda i: sum(map(lambda j: beta[j] * X[i][j], range(len(beta)))), range(len(y))))
    return sum((y[i] - y_pred[i]) ** 2 for i in range(len(y))) / (len(y) - len(x_list) - 1)


# In[258]:




# #### 설명변수들(X1,...,Xp)과 반응변수(Y) 사이에 선형 연관성 검정을 위한 F통계량

# In[259]:


#입력값 'x_list': 설명변수 리스트, 'y': 반응변수
def multiple_linear_F(x_list, y):
    return Y_i_MSR(x_list, y) / Y_i_MSE(x_list, y)


# #### 다중선형회귀모형의 분산분석표

# In[260]:


# 입력값 'x': 설명변수 리스트, 'y': 반응변수
def multiple_linear_AOVtbl(x_list, y) :
    A = pd.DataFrame({'변동요인' : ['처리', '오차', '총계'],
                      '제곱합(SS)' : [Y_i_SSR(x_list, y), Y_i_SSE(x_list, y), Y_i_SST(y)],
                      '자유도     ' : [len(x_list), len(y) - len(x_list) - 1, len(y) - 1],
                      '제곱평균(MS)        ' : [Y_i_MSR(x_list, y), Y_i_MSE(x_list, y), ''],
                      'F통계량                ' : [multiple_linear_F(x_list, y), '', '']},
                     index = ['','',''])
    return A


# In[261]:




# #### 다중선형회귀모형에 대한 유의성 F검정
# - 귀무가설(H0): 설명변수 Xi들이 반응변수 Y에 선형적으로 연관성이 없다.(β_i = 0)
# - 대립가설(H1): 설명변수 Xi들이 반응변수 Y에 선형적으로 연관성이 있다.(β_i != 0)

# ##### 우측 F검정 (표: 검정통계량과 기각역)

# In[262]:


# 입력값 'a': 유의수준,'x': 설명변수 리스트, 'y': 반응변수
def Beta_i_F_Rcr(a, x_list, y) :
        
    df = pd.read_csv('./F분포표(%g).csv' %(a), index_col=0)
    
    F = Y_i_MSR(x_list, y) / Y_i_MSE(x_list, y)
    print("1.검정통계량 : %g" %F)
    print("\n2.두 자유도 : %g, %g" %(len(x_list), len(y) - len(x_list) - 1))             
                                                                    
    cr = df['%g' %(len(x_list))][int(len(y) - len(x_list) - 1)]           
    print("\n3.임계값 : %g" %cr)                                    
    print("\n4.기각역 : (%g, oo)" %cr)
    
    if cr < F :                
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# In[263]:





# ##### 우측 F검정 (함수: p값과 유의수준)

# In[264]:


# 입력값 'a': 유의수준,'x': 설명변수 리스트, 'y': 반응변수
def Beta_i_F_Rp(a, x_list, y) :
        
    df = pd.read_csv('./F분포표(%g).csv' %(a), index_col=0)
    
    F = Y_i_MSR(x_list, y) / Y_i_MSE(x_list, y)
    print("1.검정통계량 : %g" %F)
    
    v = len(x_list) 
    w = len(y) - len(x_list) - 1
    print("\n2.두 자유도 : %g, %g" %(v,w))
    
    z = sp.symbols('z')
    f = (v**(0.5*v))*(w**(0.5*w))*(gamma((v + w)/2))/(gamma(0.5*v)*gamma(0.5*w))*(z**(0.5*(v - 2)))/(v*z + w)**(0.5*(v + w))
    i = 1 - sp.integrate(f,(z,0,F))
    print("\n3.p값 : %g" %i)
    print("\n4.유의수준 : %g" %a)
    
    if round(i,17) < a :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# In[265]:





# #### 개별 계수(β_j)에 대한 유의성 t검정
# - 위의 F검정에서 귀무가설이 기각되면, 최소한 하나 이상의 β_j가 0이 아닌 것이므로 개별적 변수에 대한 유의성 검정을 실시
# - 귀무가설(H0): 설명변수 X_j가 반응변수 Y에 선형적으로 연관성이 없다.(β_j = 0)
# - 대립가설(H1): 설명변수 X_j가 반응변수 Y에 선형적으로 연관성이 있다.(β_j != 0)

# ##### 양측 t검정 (표: 검정통계량과 기각역)

# In[266]:


# 속도 수정(create_row)
# 입력값 'a': 유의수준,'x': 설명변수 리스트, 'y': 반응변수
def Beta_j_T_Tscr(a, j, x_list, y) :
    
    df = pd.read_csv('./t분포표.csv', encoding='euc-kr', index_col=0) 
    
    def standard_error_j(j, x_list, y):
        X = list(map(lambda i: create_row(i, x_list), range(len(y))))
        X = matrix(X)
        X_transpose = X.transpose()
        XT_X_inv = (X_transpose * X).inverse()
        var_beta_j = Y_i_MSE(x_list, y) * XT_X_inv[j, j]
        return math.sqrt(var_beta_j)

    
    def t_statistic_j(j, x_list, y):
        return est_mul_Reg_equation(x_list, y)[j] / standard_error_j(j, x_list, y)
    
    
    T1 = t_statistic_j(j, x_list, y)
    
    print("1.검정통계량: %g" %T1)              
    print("\n2.자유도 :", len(y) - len(x_list) - 1)
    
    cr = df["%g" %(a/2)][int(len(y) - len(x_list) - 1)]
    print("\n3.임계값 : {0}, {1}".format(-cr,cr))
    print("\n4.기각역 : (-oo, {0}) or ({1}, oo)".format(-cr,cr))
    
    if cr < abs(T1) :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# In[267]:





# ##### 양측 t검정(함수: p값과 유의수준)

# In[268]:


# 속도 수정(create_row)
# 입력값 'a': 유의수준,'x': 설명변수 리스트, 'y': 반응변수
def Beta_j_T_Tsp(a, j, x_list, y) :

    def standard_error_j(j, x_list, y):
        X = list(map(lambda i: create_row(i, x_list), range(len(y))))
        X = matrix(X)
        X_transpose = X.transpose()
        XT_X_inv = (X_transpose * X).inverse()
        var_beta_j = Y_i_MSE(x_list, y) * XT_X_inv[j, j]
        return math.sqrt(var_beta_j)

    
    def t_statistic_j(j, x_list, y):
        return est_mul_Reg_equation(x_list, y)[j] / standard_error_j(j, x_list, y)
    
    
    t = t_statistic_j(j, x_list, y)
    
    print("1.검정통계량 : %g" %t)
    
    v = len(y) - len(x_list) - 1                
    print("\n2.자유도 :",v)
    
    z = sp.symbols('z')
    f = (gamma((v+1)/2)/(math.sqrt(v*math.pi)*gamma(v/2)))*((1+(z**2)/v)**(-(v+1)/2))     
    I = 0.5 - sp.integrate(f,(z,0,abs(t)))           
    print("\n3.p값 : %g" %(I*2))
    print("\n4.유의수준 : %g" %a)
    
    if I < a/2 :
        ans = "[결과] : 귀무가설을 기각한다."
    else :
        ans = "[결과] : 귀무가설을 기각하지 못한다."
        
    return ans


# In[269]:





# In[ ]:





# ### 결정계수
# - 설명변수(X)들이 반응변수(Y)를 선형적으로 얼마나 설명하고 있는지를 표현하는 것

# In[270]:


# 입력값 'x': 설명변수 리스트, 'y': 반응변수
def iCodeR2(x_list, y):
    R2 = Y_i_SSR(x_list, y) / Y_i_SST(y)
    # R^2 값 해석
    if R2 == 1:
        print("R^2이 1이므로 추정된 회귀식이 총변동량의 모든 부분을 설명한다.")
    elif R2 > 0.7:
        print("R^2이 1에 가까우므로 추정된 회귀식이 총변동량의 많은 부분을 설명한다.")
    elif R2 > 0.3:
        print("R^2이 중간 정도의 값을 가지므로 추정된 회귀식이 총변동량을 적절히 설명한다.")
    else:
        print("R^2이 0에 가까우므로 추정된 회귀식이 총변동량을 적절하게 설명하지 못한다.")
    return R2


# In[271]:





# ### 다중회귀모형의 가정사항과 진단
# - 1. 오차항(ε_i)의 평균은 0이고 분산은 σ^2이다. (등분산 가정)
# - 2. 오차항(ε_i)들은 서로 독립이다.
# - 3. 오차항(ε_i)은 정규분포를 따른다.
# - X변수가 여러 개이므로 다중공선성에 대한 진단이 추가된다.

# ##### 1. 오차항(ε_i)의 평균은 0이고 분산은 σ^2이다. (등분산 가정)
# - 잔차의 산포도를 통해 등분산성을 확인
# - 잔차의 산포도가 일정하게 분포되어 있다면 등분산성을 만족한다고 할 수 있다.
# 
# ##### 2. 오차항(ε_i)들은 서로 독립이다.
# - 잔차들 간의 독립성을 확인하기 위해 잔차 산포도 그래프를 생성 및 확인
# 
# ##### 3. 오차항(ε_i)은 정규분포를 따른다.
# - 단순회귀모형에서의 normality_test과 동일

# #### 잔차계산함수

# In[272]:


# 속도 수정(create_row)
def cal_residuals(x_list, y):
    X = list(map(lambda i: create_row(i, x_list), range(len(y))))
    X = matrix(X)
    y = vector(y)
    beta = est_mul_Reg_equation(x_list, y)
    y_pred = list(map(lambda i: sum(map(lambda j: beta[j] * X[i,j], range(len(beta)))), range(len(y))))
    residuals = list(map(lambda i: y[i] - y_pred[i], range(len(y))))
    return residuals


# In[273]:





# #### 잔차의 산포도 그리기 함수

# In[274]:


# 입력값 'x_list': 설명변수 리스트, 'y': 반응변수, 'x_label': 설명변수의 축 이름(영어만 가능)
def m_plot_residuals(x_list, y, x_label):
    residuals = cal_residuals(x_list, y)
    
    for i, x in enumerate(x_list):
        data = list(zip(x, residuals))
        scatter_plot = list_plot(data, plotjoined=False, marker='o')
        scatter_plot += line([(min(x), 0), (max(x), 0)], color='red', linestyle='--')
        scatter_plot.axes_labels([x_label, 'Residuals'])
        scatter_plot.show(frame=True, figsize=4, fontsize=5)


# In[275]:





# #### 다중공선성의 진단
# - 다중공선성은 X변수들 사이의 선형독립성이 성립하지 못한 상태
# - X변수 중 하나와 다른 X변수들의 선형결합이 매우 높은 상관관계에 있을 때를 뜻함
# - 다중공선성이 존재하면, X변수들의 기울기를 정확히 계산하지 못하거나 아예 계산이 되지 않는다.
# 
# [다중공선성 의심 상황]
# - (1) 산점도행렬 또는 개별 X변수끼리의 산점도에서 거의 직선에 가까운 선형관계를 보이거나,
# - (2) X변수 하나를 뺄 때와 추가할 때 다른 X변수들의 기울기 추정값들이 많이 변동하거나,
# - (3) 분산분석표에 의해서 유의적으로 기울기들이 모두 0이 아니지만 문제가 되는 X변수의 기울기는 비유의적일 때

# #### 다중공선성 계산 함수

# In[276]:


# 속도 수정(필)
def calculate_vif(x_list):
    X = matrix([
    [1] + x_list[j] for j in range(len(x_list))]).transpose()
        
    n, k = X.nrows(), X.ncols()
    vif = []

    for i in range(k):
        # y_i는 X의 i번째 열 (설명변수)
        y_i = X.column(i)
        X_i = X.delete_columns([i])  # X에서 i번째 열을 제거한 행렬
        
        X_i_transpose = X_i.transpose()
        beta_i = (X_i_transpose * X_i).inverse() * X_i_transpose * y_i
        y_i_pred = X_i * beta_i
        
        # R^2 계산
        sst_i = sum((y_i[j] - Mean(y_i))**2 for j in range(n))
        ssr_i = sum((y_i_pred[j] - Mean(y_i))**2 for j in range(n))
        
        if sst_i == 0:
            r_squared_i = float('inf')
        else:
            r_squared_i = ssr_i / sst_i

        # VIF 계산
        if r_squared_i == 1:
            vif_i = float('inf')
        else:
            vif_i = 1 / (1 - r_squared_i)
        
        vif.append(vif_i)
        
    for i, vif_i in enumerate(vif):
        if vif_i == float('inf'):
            print(f"Variable {i}: VIF = inf (분산이 0인 경우로, 유의미한 독립 변수가 아닐 가능성이 높습니다.)")
        else:
            print(f"Variable {i}: VIF = {vif_i:.3f}")
            if vif_i == 1:
                print("  이 변수는 다른 변수들과 전혀 상관관계가 없습니다.")
            elif 1 < vif_i < 5:
                print("  다중공선성이 있지만 크게 문제 되지 않는 수준입니다.")
            elif 5 <= vif_i < 10:
                print("  다중공선성이 의심됩니다.")
            else:
                print("  일반적으로 심각한 다중공선성 문제로 간주됩니다.")
    
    return vif


# In[277]:





# In[ ]:





# #### 개별 X변수끼리의 산점도 함수

# In[278]:


# 속도 수정
def recursive_combinations(i, j, n):
    if i >= n:
        return []
    if j >= n:
        return recursive_combinations(i + 1, i + 2, n)
    return [(i, j)] + recursive_combinations(i, j + 1, n)

def scatter_plots(*args):
    colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink', 'gray', 'cyan', 'magenta']
    n = len(args)

    pairs = recursive_combinations(0, 1, n)

    list(map(lambda ij: list_plot(
        list(zip(args[ij[0]], args[ij[1]])), 
        legend_label=f'List {ij[0]+1} vs List {ij[1]+1}', 
        color=colors[(ij[0] * n + ij[1]) % len(colors)], 
        gridlines=True, 
        frame=True, 
        figsize=4
    ).show(), pairs))


# In[279]:



# In[ ]:





# ### 가변수
# - 앞선 회귀분석은 독립변수 또는 설명변수가 모두 양적 자료를 갖는 양적변수인 경우에 해당
# - 질적 자료를 갖는 질적변수에 대해 다루고자 함.
# - 질적변수가 취하는 값들은 통계분석을 위하여 0과 1로 코딩된 변수를 가변수(dummy variable)라고 한다.
# - [가변수로 표현하는 과정]
# - (1) 기준 설정 (어떤 값을 통해 이상, 이하, 유, 무를 판단할 것인지에 대한 기준 설정)
# - (2) 기준을 토대로 0과 1부여
# - 가변수로 표현된 설명변수 중 하나인 X_i에 대해 0인 경우와 1인 경우를 나누어 다중선형회귀식을 고려

# #### 가변수 기준 다중선형회귀식

# In[280]:


#입력변수 'i': 몇번째 설명변수, 't': 기준값, 'x_list': 설명변수 리스트, 'y': 반응변수
def dummy_sel(i, t, x_list, y):
    xi = list(map(lambda value: 1 if value >= t else 0, x_list[i]))
    x_list[i] = xi
    
    beta = est_mul_Reg_equation(x_list, y)
    
    equation_terms = [f"{beta[0]}"] + list(map(lambda j: f"{beta[j]}(X_{j})", range(1, len(beta))))
    equation = "Y = " + " + ".join(equation_terms)
    
    return equation


# In[281]:




# #### 가변수 중 '0'에 대한 다중선형회귀식

# In[282]:


#입력변수 'i': 몇번째 설명변수, 't': 기준값, 'x_list': 설명변수 리스트, 'y': 반응변수
def dummy_sel0(i, t, x_list, y):
    xi = list(map(lambda value: 1 if value >= t else 0, x_list[i]))
    x_list[i] = xi
    
    # 회귀 계수 계산
    beta = est_mul_Reg_equation(x_list, y)
    beta[i + 1] *= 0
    
    # 회귀 방정식 생성
    equation_terms = [f"{beta[0]}"] + list(map(lambda j: f"{beta[j]}(X_{j})", range(1, len(beta))))
    equation = "Y = " + " + ".join(equation_terms)
    print(equation)
    
    return beta


# In[283]:





# #### 가변수 중 '1'에 대한 다중선형회귀식

# In[284]:


#입력변수 'i': 몇번째 설명변수, 't': 기준값, 'x_list': 설명변수 리스트, 'y': 반응변수
def dummy_sel1(i, t, x_list, y):
    xi = list(map(lambda value: 1 if value >= t else 0, x_list[i]))
    x_list[i] = xi
    
    beta = est_mul_Reg_equation(x_list, y)
    
    beta[0] += beta[i + 1]
    beta[i + 1] = None
    
    equation_terms = [f"{beta[0]}"]
    equation_terms.extend(map(lambda j: f"{beta[j]}(X_{j})" if beta[j] is not None else "0", range(1, len(beta))))
    equation = "Y = " + " + ".join(equation_terms)
    
    print(equation)
    
    return beta


# In[285]:




# #### 가변수 더미함수

# In[286]:


def my_get_dummies(data, dummy_na=True):
    """
    Args:
        data (list or list of lists): 변환할 데이터. 단일 리스트 또는 리스트의 리스트.
        dummy_na (bool): NaN 값을 포함하여 더미 변수를 생성할지 여부.
        
    Returns:
        list of lists: 더미 변수로 변환된 데이터.
    """
    if isinstance(data[0], list):  # 데이터가 리스트의 리스트인 경우
        transformed_data = [my_get_dummies(column, dummy_na) for column in data]
        return transformed_data
    
    unique_values = sorted(set(data))
    if dummy_na and None not in unique_values:
        unique_values.append(None)
    
    dummy_data = []
    for value in data:
        dummy_row = [1 if value == unique_value else 0 for unique_value in unique_values]
        dummy_data.append(dummy_row)
    
    return dummy_data


# In[287]:





# In[ ]:





# In[ ]:





# In[ ]:





# #### 독립변수가 둘이고, 그 중 하나가 가변수인 경우의 분산분석표

# In[288]:


# 입력값 'x': 설명변수 리스트, 'y': 반응변수
def dummy_multiple_linear_AOVtbl(i, t, x_list, y) :
    xi = [1 if value >= t else 0 for value in x_list[i]] #인덱스 명
    x_list[i] = xi
    A = pd.DataFrame({'변동요인' : ['처리', '오차', '총계'],
                      '제곱합(SS)' : [Y_i_SSR(x_list, y), Y_i_SSE(x_list, y), Y_i_SST(y)],
                      '자유도     ' : [len(x_list), len(y) - len(x_list) - 1, len(y) - 1],
                      '제곱평균(MS)        ' : [Y_i_MSR(x_list, y), Y_i_MSE(x_list, y), ''],
                      'F통계량                ' : [multiple_linear_F(x_list, y), '', '']},
                     index = ['','',''])
    return A


# In[289]:




# ### 피어슨 상관계수

# #### 피어슨 상관계수 t 양측검정

# In[290]:


# 속도 수정(필)
def PearsonCor(*X) :
    X_lst = input('\n설명변수(X1,X2,...) : ').split(',') #인덱스 명
    dfempty = pd.DataFrame(index = X_lst, columns = X_lst)     
    for i in range(len(X_lst)) :
        dfempty['%s'%(X_lst[i])][int(i)] = 1
        for j in range(i+1,len(X_lst)) :
            cor = sum(map(lambda xi, xj : (xi - Mean(X[i]))*(xj - Mean(X[j])) , X[i], X[j])) / (math.sqrt(sum(map(lambda xi : (xi - Mean(X[i]))**2 , X[i])))*math.sqrt(sum(map(lambda xj : (xj - Mean(X[j]))**2 , X[j]))))
            dfempty['%s'%(X_lst[i])][int(j)],dfempty['%s'%(X_lst[j])][int(i)] = cor , cor     
    return dfempty


# In[291]:





# In[292]:


# 속도 수정(필)
#보통 유의수준인 0.05보다 작으면 선형관계가 있다고 봄
def Corcoeff_Test(*X) :
    X_lst = input('\n설명변수(X1,X2,...) : ').split(',')
    df = len(X[0]) - 2
    z = sp.symbols('z')
    f = (gamma((df + 1)/2)/(math.sqrt(df*math.pi)*gamma(df/2)))*((1 + (z**2)/df)**(-(df + 1)/2))
    n = len(X)
    
    dfempty = pd.DataFrame(index = X_lst*2, columns = X_lst)     
    for i in range(len(X_lst)) :   # 열
        dfempty['%s'%(X_lst[i])][int(i)] = 1
        dfempty['%s'%(X_lst[i])][int(n+i)] = 0
        for j in range(i+1,len(X_lst)) :    # 행
            cor = sum(map(lambda xi, xj : (xi - Mean(X[i]))*(xj - Mean(X[j])) , X[i], X[j])) / (math.sqrt(sum(map(lambda xi : (xi - Mean(X[i]))**2 , X[i])))*math.sqrt(sum(map(lambda xj : (xj - Mean(X[j]))**2 , X[j]))))
            dfempty['%s'%(X_lst[i])][int(j)], dfempty['%s'%(X_lst[j])][int(i)] = cor, cor 
            t = cor*math.sqrt(df/(1 - cor**2))
            p_value = float((0.5 - sp.integrate(f,(z,0,abs(t))))*2)
            dfempty['%s'%(X_lst[i])][int(n+j)], dfempty['%s'%(X_lst[j])][int(n+i)] = p_value, p_value 
    br = pd.DataFrame([['']*len(X)], index = [''], columns = dfempty.columns)
    test_name = pd.DataFrame([X_lst], index = ['[유의성검정 p값]'], columns = dfempty.columns)
    new_df = pd.concat([dfempty.iloc[:len(X)], br, test_name, dfempty.iloc[len(X):]])
    return new_df


# In[293]:





# ---

# ### 회귀분석 데이터 이상처리

# In[294]:


# user는 'drop','mean','zero' 중 method입력
def missing_value(df, method):
    if method == 'drop':
        df = df.dropna(axis=0)
        df.head()
    elif method == 'mean':
        df = df.fillna(df.mean())
        df.head()
    elif method == 'zero':
        df = df.fillna(0)
        df.head()
    else:
        print("Invalid method")
    return df


# ### 데이터 시각화 처리

# #### 종속변수 탐색

# In[295]:


# y: target(종속변수)
def target_EDA(df, y):
    # 기초통계량 
    y_desc = df[y].describe()
    print(y_desc)
    
    # 분포 시각화
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    df[y].hist(bins=50, ax=axes[0])
    axes[0].set_title('Histogram of Target')
    
    df.boxplot(column=[y], ax=axes[1])
    axes[1].set_title('Boxplot of Target')

    plt.tight_layout()
    plt.show()


# #### 설명변수 탐색

# In[296]:


# x_columns: 설명변수(x_columns = 'Target'으로 작성하면 종속변수 제외 모두 포함)
def numeric_EDA(df, x_columns):
    # 제외할 열을 뺀 수치형 열 목록 생성
    cols = df.select_dtypes(include='number').columns.tolist()
    cols = [col for col in cols if col != x_columns]

    # 히스토그램 그리기
    fig = plt.figure(figsize=(16, 20))
    ax = fig.gca()
    df[cols].hist(ax=ax)
    plt.show()


# #### 설명변수와 종속변수 간 관계 탐색

# In[297]:


# 상관계수
# x_columns: 설명변수(x_columns = 'Target'으로 작성하면 종속변수 제외 모두 포함)
def corr_relation(df, x_columns):
    cols = df.select_dtypes(include='number').columns.tolist()
    cols = [col for col in cols if col != x_columns]
    
    # 상관계수 행렬 계산
    corr = df[cols].corr(method='pearson')    
    print(corr)
    
    # heatmap 
    fig = plt.figure(figsize = (12, 10))
    ax = fig.gca()

    sns.set(font_scale = 1.5)  # heatmap 안의 font-size 설정
    heatmap = sns.heatmap(corr.values, annot = True, fmt='.2f', annot_kws={'size':15},
                          yticklabels = cols, xticklabels = cols, ax=ax, cmap = "RdYlBu")
    plt.tight_layout()
    plt.show()


# In[298]:


# scatter plot
# 종속 - 설명 변수 관계탐색, x: 사용할 설명변수, y: 종속변수
def scatter_relation(df, x_val, y_val):
    sns.scatterplot(data=df, x=x_val, y=y_val, markers='o',color='green',alpha=0.5)
    plt.title('Scatter Plot')
    plt.show()


# ---

# ### 다항회귀
# - 앞선 회귀분석은 독립변수 또는 설명변수가 종속변수와 직선적인 관계를 갖는 경우만을 설명
# - 하지만 독립변수와 종속변수의 관계가 곡선 관계를 가질 수도 있다.
# - 곡선식을 표현하기 위해서는 회귀모형에 독립변수(X)의 2차항 또는 3차항이 포함되는 것이 더 적절
# - 다항회귀모형: 2차항 이상의 항이 추가되어 있는 것
# - 2차다항회귀모형: 2차항이 포함되는 회귀모형
# - 다항회귀를 사용하면 일차식만을 포함하는 단순회귀모형에 비하여 더 다양한 회귀모형을 만들어낼 수 있다.

# #### 다항회귀추정식 (다항회귀모형)

# In[299]:


# 속도 수정(필)
# 입력값 'x': 설명변수, 'y': 종속변수, 'degree': 설명변수에 대한 차수
def nonlinear_Reg_equation(x, y, degree):
    X = matrix([[xi^d for d in range(degree + 1)] for xi in x])
    Y = vector(y)

    beta = (X.transpose() * X).inverse() * X.transpose() * Y
    
    equation_terms = [f"{float(beta[i])}*X^{i}" for i in range(len(beta))]
    equation = " + ".join(equation_terms)
    print(f"다항회귀 추정식: Y = {equation}")
    
    return beta


# In[300]:





# #### 다항회귀선

# In[301]:


# 입력값 'x': 설명변수, 'y': 종속변수, 'degree': 설명변수에 대한 차수
def nonlinear_Reg_model(x, y, degree):
    beta = nonlinear_Reg_equation(x, y, degree)
    
    x_range = range(min(x), max(x) + 0.1, 0.1)
    y_pred = [sum(beta[i] * (xi^i) for i in range(len(beta))) for xi in x_range]

    poly_line = line(list(zip(x_range, y_pred)), color='blue', legend_label=f'degree{degree} regression line', frame=True, figsize=4, fontsize=5)
    poly_line.show()


# In[302]:





# In[303]:




# In[ ]:



