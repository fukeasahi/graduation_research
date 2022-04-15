import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def round2(num):
    return(round(num, 2))

data_Covid19 = pd.read_csv("/Users/asahi/Desktop/Pistat/Covid19.csv", sep=",")

def question11(country):
    print(country,"mean",round2(data_Covid19[country].describe()["mean"]))
    print(country,"50%",round2(data_Covid19[country].describe()["50%"]))
    print(country,"std",round2(data_Covid19[country].describe()["std"]))
question11("Bangladesh")
question11("Singapore")

def question12(country):
    x = data_Covid19[country]
    print(country,"歪度",round2(np.mean((x-np.mean(x))**3/(np.std(x,ddof=1)**3))))
    print(country,"尖度",round2(np.mean((x-np.mean(x))**4/(np.std(x,ddof=1)**4))-3))
question12("Bangladesh")
question12("Singapore")

def histg(country):
    plt.hist(data_Covid19[country])
    plt.title(country+"の1日あたりの新規感染者数")
    plt.xlabel("1日あたりの新規感染者数")
    plt.ylabel("日数(日)")
    plt.show()
histg("Bangladesh")
histg("Singapore")

def question3(country):
    Smean = np.mean(data_Covid19[country]) 
    n = data_Covid19[country].count()
    u2 = np.var(data_Covid19[country],ddof=1)
    Ssig2 = u2/n
    Ssig = Ssig2**(1/2)
    Smean = round2(Smean)
    Ssig = round2(Ssig)
    print(country,"Smean",Smean)
    print(country,"Ssig",Ssig)
question3("Bangladesh")
question3("Singapore")

def question4(country):
    Smean = np.mean(data_Covid19[country]) 
    n = data_Covid19[country].count()
    u2 = np.var(data_Covid19[country],ddof=1)
    Ssig2 = u2/n
    Ssig = Ssig2**(1/2)
    tvalue = stats.t.ppf(0.975,df=n-1)
    min1 = round2(Smean-tvalue*Ssig)
    max1 = round2(Smean+tvalue*Ssig)
    print(country,"Smean-tvalue*Ssig", min1)
    print(country, "Smean+tvalue*Ssig", max1)
question4("Bangladesh")
question4("Singapore")

mu = 1560
n = data_Covid19["Bangladesh"].count()
Smean = np.mean(data_Covid19["Bangladesh"])
u2 = np.var(data_Covid19["Bangladesh"],ddof=1)
Ssig2 = u2/n
Ssig = Ssig2**(1/2)
t0 = (Smean-mu)/Ssig
t0 = round2(t0)
print("統計量",t0)
t = stats.t.ppf(0.95,df=1)
t = round2(t)
print("右片側点",t)

n = 2306
p = 3.37/100
mu = n*p
Ssig2 = n*p*(1-p)
Ssig = Ssig2**(1/2)
print(round2(stats.norm.pdf(95,loc=mu,scale=Ssig)))

# ## P(Z>=1.96) 
# - norm.cdf

# ## P(z>=K) = 0.05を見たす確率点K
# - norm.ppf



# ###母分散が未知の時
# - 標本不偏分散