# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie.
  """
)

#option = st.selectbox(
#    'What is your favorite fruit?',
#    ('Banana','Strawberry', 'Peaches'),
#    index=None
#)

#if option != None:
#    st.write('You selceted: ', option)

from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


name_on_order = st.text_input('Name on Smoothie:')
if name_on_order:
    st.write('Name for the Smoothie order will be: '+name_on_order)

ingredient_list = st.multiselect(
    'Chose upto 5 ingredients',
    my_dataframe,
    max_selections=5
)

ingredient_string = ''
if ingredient_list:
    for fruit in ingredient_list:
        ingredient_string += fruit + '|' 

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredient_string + """','"""+name_on_order+"""')"""

time_to_insert = st.button('Submit')


if time_to_insert:
    st.write(my_insert_stmt)
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

