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