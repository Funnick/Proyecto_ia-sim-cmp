import streamlit as st
import os, random as rd
from Evolution_UI import view
import matplotlib.pyplot as plt
from Evolution_Frame import evolution as evo
import pandas as pd
import numpy as np

st.title("Evolution")
st.header("This is a simulation")

def compile(code):
    return 1

code = st.text_area("Write your code here")
if st.button(label="Compile"):
    compile(code)
    st.success("Compile!")

filename = st.text_input('Enter a file path:')
try:
    with open(filename) as input:
        st.code(input.read())
except FileNotFoundError:
    st.error('File not found.')
    
st.write('You selected `%s`' % filename)



st.sidebar.header("Ajustes de la simulacion")

days = int(st.sidebar.text_input("Dias",value=30))
nage = int(st.sidebar.text_input("Agentes",value=5))
wmap = int(st.sidebar.text_input("Largo del mapa",value=10))
hmap = int(st.sidebar.text_input("Ancho del mapa",value=10))
food = int(st.sidebar.text_input("Comida",value=10))

chck = st.checkbox("View Simulation")
if st.button("Run"):
    s = evo.Simulator()
    s.create_world(wmap, hmap)
    if chck:
        view.pygame.init()
        v = view.View(s.world)
        v.start_simulation(days)
    for i in range(nage):
        s.add_agent_to_simulation(evo.agent.Agent(-1, - 1, 100, evo.agent.gene.Gene(5, 0.5, 0.5)))

    ndays = []
    sense = [0]*11
    current_sense = 0
    for i in range(days):
        s.world.add_food(rd.randint(0,food))
        if chck: v.simulate_one_round()
        s.simulate_one_round()
        
        ndays.append(len(s.agents))

    chart_data = pd.DataFrame(
        [count for count in ndays],
        columns=['agents'])
    st.area_chart(chart_data)

    for j in s.agents:
        sense[j.sense_gene.value] += 1
    sense_data = pd.DataFrame(
        [i for i in sense],
        columns=['sense'])
    st.bar_chart(sense_data)
