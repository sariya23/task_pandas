#!/usr/bin/env python
# coding: utf-8

# In[460]:


import pandas as pd


# In[461]:


df = pd.read_json('data.json')


# In[462]:


df.head()


# In[463]:


df.loc[df['highway_cost'] > 0]


# In[464]:


df['highway_cost'] = abs(df['highway_cost'])


# In[465]:


df.head()


# ## Тарифы складов

# In[466]:


def get_quantity(products: list[dict]) -> int:
    return sum([i['quantity'] for i in products])


# In[467]:


unique_warehouse = df.drop_duplicates(subset='warehouse_name')


# In[468]:


unique_warehouse


# In[469]:


tarifs = unique_warehouse['highway_cost'] / unique_warehouse['products'].apply(get_quantity)


# In[470]:


d = zip(unique_warehouse['warehouse_name'], tarifs)


# In[471]:


answer1_dict = dict(d)


# In[472]:


answer1_dict


# In[473]:


answer1 = pd.DataFrame({
    'warehouse_name': unique_warehouse['warehouse_name'],
    'tarif_cost': tarifs
}
)


# ### Ответ

# In[474]:


answer1


# ## Суммарное количество , суммарный доход , суммарный расход и суммарную прибыль для каждого товара

# доходом с товара является цена продажи * количество товара
# 
# расходом является тариф для данного склада * количество товара
# 
# прибылью является доход - расход

# In[475]:


df.head()


# In[476]:


answer1_dict[df.iloc[0]['warehouse_name']]


# In[477]:


hash_quantity = {}
hash_income = {}
hash_expenses = {}
hash_profit = {}


# In[478]:


for i, products in enumerate(df['products']):
    for product in products:
        name, price, quantity = product['product'], product['price'], product['quantity']

        if name not in hash_quantity:
            hash_quantity[name] = quantity
        else:
            hash_quantity[name] += quantity
            
        if name not in hash_income:
            hash_income[name] = quantity * price
        else:
            hash_income[name] += quantity * price


# In[479]:


for i, products in enumerate(df['products']):
    for product in products:
        name, price, quantity = product['product'], product['price'], product['quantity']
        
        if name not in hash_expenses:
            hash_expenses[name] = answer1_dict[df.iloc[i]['warehouse_name']] * hash_quantity[name]
        else:
            hash_expenses[name] += answer1_dict[df.iloc[i]['warehouse_name']] * hash_quantity[name]
    


# In[480]:


hash_quantity


# In[481]:


hash_income


# In[482]:


hash_expenses


# In[483]:


unique_products = hash_quantity.keys()


# In[484]:


unique_products


# In[485]:


for i in unique_products:
    hash_profit[i] = hash_income[i] - hash_expenses[i]
    


# In[486]:


hash_profit


# In[487]:


answer2_dict = {
    'product': unique_products,
    'quantity': hash_quantity.values(),
    'income': hash_income.values(),
    'expenses': hash_expenses.values(),
    'profit': hash_profit.values()
}


# In[488]:


answer_2 = pd.DataFrame(answer2_dict)


# ### Ответ

# In[489]:


answer_2


# ## Составить табличку со столбцами 'order_id' (id заказа) и 'order_profit'. Средняя прибыль с заказа

# In[490]:


df.head()


# In[491]:


order_profit = []


# In[492]:


for i in range(len(df)):
    products = df.loc[i]['products']
    warehouse = df.loc[i]['warehouse_name']
    income = sum(map(lambda x: x['price'] * x['quantity'], products))
    expenses = sum([i['quantity'] * answer1_dict[warehouse] for i in products])
    order_profit.append(income - expenses)


# In[493]:


dict3 = {
    'order_id': df['order_id'],
    'order_profit': order_profit
}


# In[494]:


answer_3_df = pd.DataFrame(dict3)


# ### Ответ

# In[495]:


answer_3_df


# In[496]:


asnwer_3_avg = answer_3_df['order_profit'].mean()


# In[497]:


asnwer_3_avg


# ## Составить табличку типа 'warehouse_name' , 'product','quantity', 'profit', 'percent_profit_product_of_warehouse' (процент прибыли продукта заказанного из определенного склада к прибыли этого склада)

# In[604]:


warehouse_name_list = []
product_list = []
quantity_list = []
profit_list = []

dict4 = {
    'warehouse_name': [],
    'product': [],
    'quantity': [],
    'profit': [],
}


# In[605]:


df.head()


# In[606]:


df = df.sort_values(by='warehouse_name')


# In[607]:


df


# In[608]:


df.loc[30]['products']


# In[609]:


for i in df.index:
    warehouse = df.loc[i]['warehouse_name']
    warehouse_name_list.append(warehouse)
    
    products = df.loc[i]['products']
    product_list.append(', '.join(map(lambda x: x['product'], products)))
    
    income = sum(map(lambda x: x['price'] * x['quantity'], products))
    expenses = sum([i['quantity'] * answer1_dict[warehouse] for i in products])
    profit = income - expenses
    profit_list.append(profit)
    
    quantity = sum(map(lambda x: x['quantity'], products))
    quantity_list.append(quantity)


# In[610]:


dict4 = {
    'warehouse_name': warehouse_name_list,
    'product': product_list,
    'quantity': quantity_list,
    'profit': profit_list
}


# In[611]:


df4 = pd.DataFrame(dict4)


# In[612]:


df4


# In[613]:


percent_profit_product_of_warehouse = []


# In[614]:


profit_by_warehouse = df4.groupby('warehouse_name').sum()


# In[625]:


for i in df4.index:
    cur_profit = df4.loc[i]['profit']
    cur_ware = df4.loc[i]['warehouse_name']
#     print(profit_by_warehouse.loc[cur_ware]['profit'])
    percent_profit_product_of_warehouse.append((cur_profit / profit_by_warehouse.loc[cur_ware]['profit']) * 100)


# In[627]:


df4['percent_profit_product_of_warehouse'] = percent_profit_product_of_warehouse


# ### Ответ

# In[629]:


df4


# ## Взять предыдущую табличку и отсортировать 'percent_profit_product_of_warehouse' по убыванию, после посчитать накопленный процент. Накопленный процент - это новый столбец в этой табличке, который должен называться
# 'accumulated_percent_profit_product_of_warehouse'. По своей сути это постоянно растущая сумма отсортированного по убыванию столбца 'percent_profit_product_of_warehouse'.

# In[630]:


df5 = df4.copy()


# In[634]:


df5 = df5.sort_values(by='percent_profit_product_of_warehouse', ascending=False)


# In[635]:


df5


# In[674]:


res5 = [df5.percent_profit_product_of_warehouse[0]]
lst = df5.percent_profit_product_of_warehouse.to_list()


# In[675]:


for i in range(1, len(lst)):
    res5.append(lst[i] + sum(lst[:i]))


# In[677]:


df5['accumulated_percent_profit_product_of_warehouse'] = res5


# ### Ответ

# In[678]:


df5


# ## Присвоить A,B,C - категории на основании значения накопленного процента ('accumulated_percent_profit_product_of_warehouse'). Если значение накопленного процента меньше или равно 70, то категория A.
# Если от 70 до 90 (включая 90), то категория Б. Остальное - категория C. Новый столбец обозначить в таблице как 'category'

# In[696]:


bins = [0, 70, 91, 900]
labels = ['А', 'Б', 'С']


# In[697]:


cuts = pd.cut(df5['accumulated_percent_profit_product_of_warehouse'], bins, labels=labels)


# In[698]:


df5['category'] = cuts


# ### Ответ 

# In[699]:


df5


# In[ ]:




