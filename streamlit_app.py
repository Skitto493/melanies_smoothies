# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Order your smoothie:
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_df, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_df,
    max_selections=5
    )
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '  
    #st.write(ingredients_string)

    insert_event = st.button('Submit Order')
    if(insert_event):
    
        insert_stmnt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','"""+order_name+"""')"""
        session.sql(insert_stmnt).collect()
        #st.write(insert_stmnt)
        success_msg = 'Your Smoothie has been ordered, ' + order_name + '!'
        st.success(success_msg, icon="✅")
