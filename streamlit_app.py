# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom Smoothie !
    """
)

cnx = st.connection("Snwoflake")
session = cnx.session()

name_on_order = st.text_input("Name on smoothie")
st.write("The name on your smoothie will be: ", name_on_order)

ingredients_list = st.multiselect (
    'Choose up to 5 ingrendients: ',
    my_dataframe, max_selections = 5
)
if ingredients_list: 
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """"','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered, ' + name_on_order + '!', icon="✅")





