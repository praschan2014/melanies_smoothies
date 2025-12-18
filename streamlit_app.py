# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd

#### New set of libraries for Nutrition information
import requests


# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie.
  """
)

### Added line for connection from outside SiS app
cnx = st.connection("snowflake")
sess = cnx.session() ##get_active_session()

my_dataframe = sess.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

name_on_order = st.text_input('Name on Smoothie:')
if name_on_order:
    st.write('Name for the Smoothie order will be: '+name_on_order)

#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredient_list = st.multiselect(
    'Chose upto 5 ingredients',
    my_dataframe,
    max_selections=5
)

ingredient_string = ''
if ingredient_list:
    for fruit in ingredient_list:
        ingredient_string += fruit + '|'
        #gets = "https://my.smoothiefroot.com/api/fruit/" + fruit
        st.subheader(fruit + ' Nutrition Information')
        #smoothiefroot_response = requests.get(gets)
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredient_string + """','"""+name_on_order+"""')"""

time_to_insert = st.button('Submit')

if time_to_insert:
    ###st.write(my_insert_stmt)
    sess.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response)
#sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)
