#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 09:01:06 2021

@author: jaimegde
"""

import numpy as np
import pandas as pd
from plotnine import *

bar = pd.read_excel('Bar.xlsx')
net = pd.read_excel('Netflix.xlsx')
bar.columns
net.columns

# SCATTERPLOTS

#1 - negative correlation
ggplot(aes(x='bill', y="tip"), bar) + geom_point() 
bar.bill.corr(bar.tip)

#2 - positive correlation
ggplot(aes(x='bill', y="orders"), bar) + geom_point() 
ggplot(aes(x='bill', y="orders", color='gender'), bar) + geom_point() 
bar.bill.corr(bar.orders)

# BARPLOT

#3 
ggplot(aes(x = "service"), bar) + geom_bar()
bar.service.value_counts()

#3b
aux = bar.loc[ bar.service.isin(['very good', 'excellent', 'brilliant']),:]
ggplot(aes(x = "service", fill='service'), aux) + geom_bar() + coord_flip()

#4
aux = bar.loc[bar.year == 2019,:]
ggplot(aes(x = "gender", y = 'bill', fill='gender'), aux) + geom_bar(stat='identity') 

#5
aux = bar.loc[:,['week_day', 'orders', 'service']].groupby(by=['week_day', 'service'], as_index=False).sum()
ggplot(aes(x='factor(week_day)', y='orders', fill='service'), aux) + geom_bar(stat='identity', position='dodge')

# LINEPLOT

#6
aux = net.loc[:,["budget","release_year"]].groupby(by="release_year",as_index=False).sum().tail(30)
ggplot(aes(x = "release_year", y = "budget"),aux) + geom_line(size=3,color = "Blue")+geom_point(size=5,color='yellow')

#6b
ggplot(aes(x='release_year', y='budget', fill='budget'), aux) + geom_bar(stat='identity', position='dodge')
ggplot(aes(x='release_year', y='budget', fill='budget'), aux) + geom_point()

#7
aux = net.loc[:,["month_added","country","title"]].loc[net.country.isin(["Canada", "United", "India", "Spain"]),:].groupby(by=["month_added","country"],as_index=False).count()
ggplot(aes(group='country', x='factor(month_added)', y = 'title', color = 'country'), aux) + geom_line() + facet_grid(('country','.'))

# HISTOGRAMS

#8
ggplot(aes(x="duration"),net) + geom_histogram() + coord_cartesian(xlim=(0,200)) # para limitar el rango a 200

#9
ggplot(aes(x = 'duration', fill='genres'), net) + geom_histogram() + facet_wrap(('genres')) + coord_cartesian(ylim=(0,50))

# DENSITY

#10 
#ggplot(aes(x="duration",color="color"),net)+geom_density()+facet_grid(("color","."))

# BOXPLOT

#11
ggplot(aes(y="tip",x="gender",fill="service"),bar) + geom_boxplot()

#12
ggplot(aes(y="tip",x="gender",fill="service"),bar) + geom_boxplot() + facet_wrap(('year')) + coord_cartesian(ylim=(0,37))

# HEATMAPS

#13
aux = bar.loc[:,['orders', 'month', 'day']].loc[bar.year == 2020,:]
ggplot(aes(x = "factor (day)",y ="factor (month)", fill = "orders"),aux)+geom_tile(color="white",size=1)

#14
aux = pd.crosstab(bar.supervisor,bar.service) 
aux.reset_index(inplace=True) 
aux = pd.melt(aux,id_vars=["supervisor"])
ggplot(aes(y = "supervisor",x ="service", fill = "value"),aux)+geom_tile()

#14b
aux = pd.crosstab(bar.supervisor,bar.service) 
aux.reset_index(inplace=True) 
aux = pd.melt(aux,id_vars=["supervisor"])
aux["service"] = pd.Categorical(aux.service,categories=["brilliant","excellent","very good","good","normal"])
ggplot(aes(y = "supervisor",x ="service", fill = "value"),aux)+geom_tile(color="white",size=1) +geom_text(aes(label='value'), size=9)

# PLOTS

#15
aux = bar.loc[:,['nationality', 'items']].groupby(by='nationality', as_index=False).sum()
aux.reset_index(inplace = True)
ggplot(aes(x = 'nationality', y = 'items', fill='nationality'), aux) + geom_bar(stat='identity')\
+ geom_text(aes(label='items'),position = position_stack(vjust=1.05),size=10,color='black')

#15b
aux = bar.loc[:,['nationality', 'items']].groupby(by='nationality', as_index=False).sum().sort_values(by='items', ascending=0)
aux["nationality"] = pd.Categorical(aux.nationality,categories = aux.nationality.unique())
aux = aux.round(2)
ggplot(aes(x = 'nationality', y = 'items', fill='nationality'), aux) + geom_bar(stat='identity')\
    + geom_text(aes(label='items'),position = position_stack(vjust=1.05),size=10,color='black')

#16
aux = bar.loc[:,['orders', 'week_day']].groupby(by='week_day', as_index=False).sum()
aux.reset_index(inplace = True)
ggplot(aes(x = 'week_day', y='orders'), aux) + geom_line()\
    + geom_text(aes(label='orders'),position=position_stack(vjust=1.05),size=7,color='black')

#17
aux = bar.loc[:,['supervisor','gender','service']].groupby(by=['supervisor', 'service'], as_index = False).count()
ggplot(aes(x="supervisor",y="gender",fill="service"),aux)+geom_bar(stat="identity",position="fill")\
    +geom_text(aes(y="gender",label ="gender"),size=10,position=position_fill(vjust=1.05))

#18
aux = bar.loc[:,['nationality', 'tip']].groupby(by='nationality', as_index=False).sum().sort_values('tip', ascending=True)
aux = aux.iloc[:3]
ggplot(aes(x="nationality", y = "tip", fill = "nationality"), aux) + geom_bar(stat="identity")\
    + xlab('nationality') + ylab('tips') + geom_text(aes(label='tip'), position= position_stack(vjust=1.05),size=10,color="black")

#19
aux = bar.loc[:,["nationality", "bill"]].loc[(bar.bill <= 1000) & (bar.bill >= 500)].sort_values('bill',ascending=False).groupby('nationality', as_index=False).head(1)
ggplot(aes(x="nationality",y="bill",fill="nationality"),aux) + geom_bar(stat="identity")\
   + scale_fill_brewer(type="seq", palette="Blues")

#20
aux = net.loc[net.release_year.isin(range(2005,2021,1)),:].groupby(by=["genres","release_year"], as_index=False).sum()
ggplot(aes(aux="factor(release_year)", y = "genres", fill = "actors"), x) + geom_tile()

#21
x = net.loc[net.release_year.isin(range(2005,2021,1)),:].groupby(by=["genres","release_year"],as_index=False).sum()
ggplot(aes(x = "factor(release_year)", y ="genres", fill = "actors"),x)+geom_tile(color="white",size=1)\
+scale_fill_gradient(low="Yellow", high="Red")+geom_text(aes(label="actors"), size=7)\
+theme(panel_background = element_rect(fill = "white"),axis_text_x = element_text(angle = 45, hjust = 1),
axis_text_y = element_text(angle = 45, hjust = 1),axis_line = element_line(color = "black"))

#22
aux = net.corr()
aux.reset_index(inplace=True)
aux = pd.melt(aux,id_vars=['index'])
aux.columns = ["variable1", "variable2", "correlation"]

ggplot(aes(x = "variable1", y="variable2", fill="correlation"), aux) + geom_tile()\
    + scale_fill_gradient2(limit = [-1,1]) + ggtitle("Correlation Matrix") + ylab("variables")\
        + xlab("variables") + theme(panel_background = element_rect(fill = "white"), axis_text_x = element_text(angle = 45, hjust= 1),axis_text_y = element_text(angle=45, hjust = 1),axis_line = element_line(color ="black") )

#23
net.columns
aux = net.loc[net.budget >= 5000000,:].loc[:,["budget","country"]].sort_values("budget", ascending=False).drop_duplicates(subset=["country"], keep="first").head(8)
ggplot(aes(x = "country", y="budget", fill="country"),aux) + geom_bar(stat="identity")

#24
aux = net.loc[:,["color", "genres","title"]].groupby(by=["color","genres"],as_index=False).count()
ggplot(aes(x="genres", y="title", fill="color"), aux) + geom_bar(stat="identity", position="fill") + coord_flip()

#25
aux = net.loc[:,["director","budget"]].groupby(by=["director"],as_index=False).sum(). sort_values("budget",ascending=0).head(5)
ggplot(aes(x="director", y="budget", fill="director"),aux) + geom_bar(stat ="identity")

#26
bar.columns
aux = bar.loc[:,["orders","gender","service"]].groupby(by=["service","gender"]).agg(Max = ("orders","max"),Min = ("orders","min"),Med=("orders","mean")).reset_index()
aux.Med = aux.Med.round()
aux = pd.melt(aux,id_vars=['service',"gender"])
ggplot(aes(x="service",y="value",fill="variable"),aux)+geom_bar(stat="identity",position="stack") +facet_grid(("gender","."))

#26a
aux = bar.loc[:,["orders","gender","service"]].groupby(by=["service","gender"]).agg(Max = ("orders","max"),Min = ("orders","min"),Med=("orders","mean")).reset_index()
aux.Med = aux.Med.round()
aux = pd.melt(aux,id_vars=['service',"gender"])
ggplot(aes(x="service",y="value",fill="variable"),aux)+geom_bar(stat="identity",position="stack") +facet_grid(("gender","."))\
+ggtitle("Metrics value by type of service") +geom_text(aes(label='value'),position=position_stack(vjust=1.05),size=10,color="black")\
+scale_fill_brewer(type = "seq", palette = "Blues")

#26b
aux = bar.loc[:,["orders","gender","service"]].groupby(by=["service","gender"]).agg(Max = ("orders","max"),Min = ("orders","min"),Med=("orders","mean")).reset_index()
aux.Med = aux.Med.round()
aux = pd.melt(aux,id_vars=['service',"gender"])
ggplot(aes(x="service",y="value",fill="variable"),aux)+geom_bar(stat="identity",position="stack") +facet_grid(("gender","."))\
+ ggtitle("Metrics value by type of service") +geom_text(aes(label='value'),position=position_stack(vjust=1.05),size=10,color="black") +scale_fill_brewer(type = "seq", palette = "Blues") +theme(panel_background=element_rect(fill='white'),axis_text_y=element_blank())\
+ xlab("type of service") +ylab("orders")

#27
aux = bar.loc[bar.nationality.isin(["Filipino", "Mexican", "German", "Italian"]),:].loc[:,["orders","month","nationality","year",]].groupby(by=["month","nationality","year"],as_index=False).sum().sort_values("month",ascending = 1)
aux['month'] = pd.Categorical(aux.month, categories = aux.month.unique())
aux['month'] = aux.month.map({1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"})
ggplot(aes(group="nationality",x ="month", y="orders", color ="nationality"),aux)+geom_line() + facet_grid(("year","."))

#27a
aux = bar.loc[bar.nationality.isin(["Filipino", "Mexican", "German", "Italian"]),:].loc[:,["orders","month","nationality","year",]].groupby(by=["month","nationality","year"],as_index=False).sum().sort_values("month",ascending = 1)
aux['month'] = pd.Categorical(aux.month, categories = aux.month.unique())
aux['month'] = aux.month.map({1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"})
ggplot(aes(group="nationality",x ="month", y="orders", color ="nationality"),aux)+geom_line() +facet_grid(("year","."))\
+ggtitle("total orders per nationality") +xlab("Months") +ylab("Total orders")+theme(axis_text_x = element_text(angle = 45),panel_background=element_rect(fill='white'))

#28
aux = bar.loc[:,["tip","month","year","day"]].loc[bar.year == 2020,:].groupby(by=["month","day","year"],as_index=False).sum()
aux['month'] = pd.Categorical(aux.month, categories=aux.month.unique())
aux['month'] = aux.month.map({1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"})
ggplot(aes(x ="factor(day)", y ="month", fill ="tip"),aux)+geom_tile()

#28a
aux = bar.loc[:,["tip","month","year","day"]].loc[bar.year ==2020,:].groupby(by=["month","day","year"],as_index=False).sum()
aux['month'] = pd.Categorical(aux.month, categories=aux.month.unique())
aux['month'] = aux.month.map({1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"})
ggplot(aes(x ="factor(day)",y="month",fill="tip"),aux)+geom_tile(aes(width=.95,height=.95)) +scale_fill_gradient(low="#D3D3D3", high="Blue")\
+ ggtitle("Yearly Tips") +xlab("Days") +ylab("Months") + theme(panel_background=element_rect(fill='white'))

#28b
aux = bar.loc[bar.day.isin (range(1,16,1)),:].loc[bar.month.isin (range(1,7,1)),:].loc[:,["tip","month","year","day"]].loc[bar.year ==2020,:].groupby(by=["month","day","year"],as_index=False).sum()
aux['month'] = pd.Categorical(aux['month'], categories=aux.month.unique())
aux['month'] = aux["month"].map({1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio"})
aux.tip = aux.tip.round().astype(int)
ggplot(aes(x ="factor(day)",y="month",fill="tip"),aux)+geom_tile(aes(width=.95,height=.95))\
+scale_fill_gradient(low="#D3D3D3", high="Blue") + ggtitle("Yearly Tips") +xlab("Days")\
+ylab("Months") +theme(panel_background=element_rect(fill='white')) +geom_text(aes(label='tip'), size=9)

















