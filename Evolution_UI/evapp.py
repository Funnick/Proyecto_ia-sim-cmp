import streamlit as st
import os

st.title("Evolution")
st.header("This is a simulation")

def compile(code):
    return 1

code = st.text_area("Write your code here")
if st.button(label="Run!"):
    compile(code)
    st.success("Compile!")

filename = st.text_input('Enter a file path:')
try:
    with open(filename) as input:
        st.code(input.read())
except FileNotFoundError:
    st.error('File not found.')
    
st.write('You selected `%s`' % filename)

import sim_ui
import matplotlib.pyplot as plt

width = int(st.text_input("Width",value=1000))
heigth = int(st.text_input("Heigth",value=1000))
iterations = int(st.text_input("Iterations",value=1000))

sim_ui.pygame.init()
if st.button("Show"):
    game = sim_ui.main(width=width,height=heigth, iterations=iterations)
    sim_ui.pygame.init()

#import plotly.express as px
import pandas as pd

import numpy as np
chart_data = pd.DataFrame(
    [[sim_ui.rd.randint(-5, 5) for i in range(3)]for j in range(20)],
    columns=['a', 'b', 'c'])
st.area_chart(chart_data)