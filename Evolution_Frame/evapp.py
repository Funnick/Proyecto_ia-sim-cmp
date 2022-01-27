import streamlit as st
import os, random as rd
import matplotlib.pyplot as plt
import evolution as evo, gene
import pandas as pd
import numpy as np

st.title("Evolution")
st.header("This is a simulation")



st.sidebar.header("Ajustes de la simulacion")

days = int(st.sidebar.text_input("Dias",value=30))
nage = int(st.sidebar.text_input("Agentes",value=5))
wmap = int(st.sidebar.text_input("Largo del mapa",value=10))
hmap = int(st.sidebar.text_input("Ancho del mapa",value=10))
food = int(st.sidebar.text_input("Comida",value=10))

if st.button("Run"):
    s = evo.Simulator()
    s.create_world(wmap, hmap, trees=0)
    for i in range(nage):
        s.add_agent_to_simulation(evo.agent.Agent(-1, - 1, 100, 
                                                  gene.Gene(5, 0.5, 0.8),
                                                  gene.Gene(5, 0.5, 0.8),
                                                  gene.Gene(5, 0.5, 0.8)))

    ndays = []
    sense = [0]*11
    current_sense = 0
    ndays.append(len(s.agents))
    for i in range(days):
        s.world.add_food(food)
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
