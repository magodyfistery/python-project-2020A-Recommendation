import numpy as np
allusers = {	'1': [5.0, 0, 4.95, 5.0, 0, 0, 4.0, 0, 5.0], 
		'2': [0, 0, 0, 5.0, 2.0, 4.0, 0, 0, 0], 
		'3': [0, 0, 3.0, 0, 5.0, 5.0, 0, 0, 0], 
		'4': [0, 0, 0, 0, 0, 0, 0, 0, 0], 
		'5': [4.0, 0, 0, 0, 0, 0, 0, 0, 0], 
		'6': [4.0, 0, 0, 0, 0, 0, 0, 0, 0]
	}
#Tengo que validar si el usuario que se logea tiene al menos un registro en user_product_rating. Si lo tiene, mando template con grs, sino, mando el que está.

#select city from user group by city order by city;
cities = ['Boston','Quito']

#select id,city from user order by city;
#user_cities = [['4','Boston'],['6','Boston'],['7','Boston'],
#		['1','Quito'],['2','Quito'],['3','Quito'],['5','Quito']]

#select id,city from user where username in (select username_user from user_product_rating) order by city;
user_cities = [['6','Boston'],
		['1','Quito'],['2','Quito'],['3','Quito'],['5','Quito']]
groups = {c:{} for c in cities}

"""
for city in cities:
	for item in user_cities:
		if item.city == city:
			groups[city][item.id]=allusers[item.id]
"""

for city in cities:
	for item in user_cities:
		if item[1] == city:
			groups[city][item[0]]=allusers[item[0]]

#print(groups['Boston'])

#select city from user where id=2;
# Aquí mando id de la variable session.
#select city from user where id=2 and username in (select username_user from user_product_rating);
#Si retorna empty, le mando template original.
city = 'Quito'
grupo = groups[city]
print(grupo)
#Aditive Utilitarian Strategy
print("#########ADITIVE#######")
suma = np.zeros(len(grupo['1']))# Siempre habrá producto con id = 1 
for k,v in grupo.items():
	suma = suma + v
print(suma)
print(-np.sort(-(np.argpartition(suma,-3)[-3:]+1)))
#Multiplicative Utilitarian Strategy
print("#########MULTIPLICATIVE#######")
mult = np.ones(len(grupo['1']))
for k,v in grupo.items():
	varr = np.array(v)
	varr[varr==0]=1
	mult = mult * varr
print(mult)
print(-np.sort(-(np.argpartition(mult,-3)[-3:]+1)))
#Least Misery Strategy
print("#########LEAST MISERY#######")
least = np.array(grupo['1'])
least[least==0]=1
for k,v in grupo.items():
	varr = np.array(v)
	varr[varr==0]=1
	i=0
	for x in least:
		if varr[i]<=x:
			least[i]=varr[i]
		i+=1
print(least)
print(-np.sort(-(np.argpartition(least,-3)[-3:]+1)))
#Most Pleasure
print("#########MOST PLEASURE#######")
most = np.array(grupo['1'])
for k,v in grupo.items():
	varr = np.array(v)
	i=0
	for x in most:
		if varr[i]>x:
			most[i]=varr[i]
		i+=1
print(most)
print(-np.sort(-(np.argpartition(most,-3)[-3:]+1)))

