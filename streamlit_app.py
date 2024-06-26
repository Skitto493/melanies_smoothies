# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Order your smoothie:
    """
)

order_name = st.text_input("Your name: ")
st.write("Order for: ", order_name)

cnx = st.connection("snowflake")
session = cnx.session()
my_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_df, use_container_width=True)

pd_df = my_df.to_pandas()
#st.dataframe(pd_df)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_df,
    max_selections=5
    )
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '  
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + search_on)
        if(fruityvice_response):
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        else:
            st.write('Nutrition data not available for ' + fruit_chosen)
    #st.write(ingredients_string)

    insert_event = st.button('Submit Order')
    if(insert_event):
    
        insert_stmnt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','"""+order_name+"""')"""
        session.sql(insert_stmnt).collect()
        #st.write(insert_stmnt)
        success_msg = 'Your Smoothie has been ordered, ' + order_name + '!'
        st.success(success_msg, icon="✅")
