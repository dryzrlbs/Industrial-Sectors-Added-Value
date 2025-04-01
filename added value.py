
from glob2 import glob
import pandas
import matplotlib

# "sanayi_icio_mex_china_data_prep_v4.ipynb" uygulayıp, ilgili directory'de csv dosyalarını hazırladıktan sonra bu kodun calistirilmasi gerekiyor

a=glob("D:/Kaynaklar_Master/OECD_ICIO/all_years_chn_mex_adjusted/*.csv") 

#Makine sektörü NACE 28, 2005-2018 yılları

loc=[]
fore=[]
val=[]

for years in a:
    #print(years[-8:-4])
    df=pandas.read_csv(years, index_col=0)
    df2=df.loc[[m for m in df.index.tolist() if "TAXSUB" not in m],[m for m in df.columns.tolist() if "TUR" in m][:-6]]
    loc.append(df2.loc[[n for n in df2.index.tolist() if "TUR" in n], "TUR_28"].sum()/(df2.loc["OUTPUT","TUR_28"]-df.loc["TUR_TAXSUB","TUR_28"]))
    fore.append(df2.loc[[n for n in df2.index.tolist() if "TUR" not in n],"TUR_28"][:-2].sum()/(df2.loc["OUTPUT","TUR_28"]-df.loc["TUR_TAXSUB","TUR_28"]))
    val.append(df2.loc["VALU","TUR_28"]/(df2.loc["OUTPUT","TUR_28"]-df.loc["TUR_TAXSUB","TUR_28"]))

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np

labels=[years[-8:-4] for years in a]

#Line graph

fig, ax = plt.subplots()

ax.plot(labels, loc, linewidth=2,label="yerli g.")
ax.plot(labels, val, linewidth=2, label="k. değer")
ax.plot(labels, fore, linewidth=2, label="yabancı g.")

ax.legend(loc="upper right")

fig.set_size_inches(10,5)
plt.show()

fig.savefig("makine_çizgi.png")

# Stacked bar chart

labels=[years[-8:-4] for years in a]
width=0.4

fig, ax = plt.subplots()

ax.bar(labels, val, width, label="k. değer")
ax.bar(labels, loc, width, bottom=val, label="yerli g.")
ax.bar(labels, fore, width, bottom=np.array(loc)+np.array(val), label="yabancı g.")

ax.set_ylabel("Paylar, %")
ax.set_xlabel("Yıllar")
ax.legend(loc="lower right")

fig.set_size_inches(10,5)

plt.show()

fig.savefig("makine_stacked.png")

#Tüm sektörler, 2005-2018 yılları

df4=pandas.DataFrame()
for years in a:
    #print(years[-8:-4])
    df=pandas.read_csv(years, index_col=0)
    df2=df.loc[[m for m in df.index.tolist() if "TAXSUB" not in m],[m for m in df.columns.tolist() if "TUR" in m][:-6]]
    df_d=df.loc[[m for m in df.index.tolist() if "TUR" in m][:-1],[n for n in df.columns.tolist() if "TUR" not in n]]
    loc=[]
    fore=[]
    val=[]
    out=[]
    for m in df2.columns.tolist():
        loc.append(df2.loc[[n for n in df2.index.tolist() if "TUR" in n], m].sum()/(df2.loc["OUTPUT",m]-df.loc["TUR_TAXSUB",m]))
        fore.append(df2.loc[[n for n in df2.index.tolist() if "TUR" not in n],m][:-2].sum()/(df2.loc["OUTPUT",m]-df.loc["TUR_TAXSUB",m]))
        val.append(df2.loc["VALU",m]/(df2.loc["OUTPUT",m]-df.loc["TUR_TAXSUB",m]))
        out.append(df_d.loc[m,:"ROW_DPABR"].sum()/df_d.loc[m,"TOTAL"])

    yy=[years[-8:-4] for n in range(len(df2.columns.tolist()))]
    df3=pandas.DataFrame([val,loc,fore,out,yy]).transpose()
    df3.columns=["kdeğer","yerli","yabancı_g","yabancı_ç","yıl"]
    df3.index=df2.columns.tolist()
    df4=pandas.concat([df4,df3])


#Tüm sektörler 2018 sade scatter

x=df4[df4["yıl"]=="2018"]["yabancı_g"].values
y=df4[df4["yıl"]=="2018"]["yabancı_ç"].values

fig, ax =plt.subplots()

ax.scatter(x,y)

ax.set_xlabel("yabancı girdi")
ax.set_ylabel("yabancı satışı")

plt.show()
fig.savefig("sektörler_basit_scatter.png")

# tüm sektörleri ana sektör sınıflarına ayırma

imalat=df4.index.tolist()[5:22]
tarım=df4.index.tolist()[:2]
maden=df4.index.tolist()[2:5]
ins_en_ç=df4.index.tolist()[22:25]
hizm=df4.index.tolist()[25:45]

cl=[]

for m in df4.index.tolist():
    if m in imalat:
        cl.append(1)
    elif m in tarım:
        cl.append(2)
    elif m in maden:
        cl.append(3)
    elif m in ins_en_ç:
        cl.append(4)
    elif m in hizm:
        cl.append(5)

df4["sınıf"]=cl

cl2=[]

for m in df4.index.tolist():
    if m in imalat:
        cl2.append("imalat")
    elif m in tarım:
        cl2.append("tarım")
    elif m in maden:
        cl2.append("maden")
    elif m in ins_en_ç:
        cl2.append("ins_en_ç")
    elif m in hizm:
        cl2.append("hizm")

df4["sınıf2"]=cl2

#df4'ü ilerde başka uygulamalar için kullanmak istersek diye kaydetmekte fayda var

df4.to_csv("sektörel_girdi_kullanımı.csv")

#Sınıflar, renk kodları ve ortalama çizgileriyle tüm sektörler 2018 scatter

x=df4[df4["yıl"]=="2018"]["yabancı_g"].values
y=df4[df4["yıl"]=="2018"]["yabancı_ç"].values
la=df4[df4["yıl"]=="2018"]["sınıf"].values
colors=["red","green","blue","purple","black"]

fig, ax =plt.subplots()

ax.plot([x.mean(),x.mean()], [0,1], color="0.7")
ax.plot([0,1], [y.mean(),y.mean()], color="0.7")

scatter = ax.scatter(x,y, c=la, cmap=matplotlib.colors.ListedColormap(colors))

ax.legend(handles=scatter.legend_elements()[0], labels=["imalat","tarım","maden","ins_en_ç","hizm"])

ax.set_xlabel("yabancı girdi")
ax.set_ylabel("yabancı satışı")

fig.set_dpi(100)

plt.show()
fig.savefig("sektörler_güzel_scatter.png")
