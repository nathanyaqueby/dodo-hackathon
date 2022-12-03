import streamlit.components.v1 as components
import streamlit as st
from io import BytesIO
import os
import numpy as np


st.set_page_config(
    page_title="Algaeia - DODO Digital Ocean Hackathon",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/nathanyaqueby/dodo-hackathon',
        'Report a bug': "https://github.com/nathanyaqueby/dodo-hackathon",
        'About': "Our mission is simple. To help people with dementia remember daily objects and their loved ones,"
                 " DigiMemoir takes pictures of objects & people and stores the stories associated with them. "
                 "Whenever the person focuses on an object or person, the digital memory will start talking about it, "
                 "reminding the person of the history behind that object or person. Developed during the Roche"
                 " Dementia Hackathon Challenge by Team 4 (Women in AI and Robotics)."
    }
)

st.title('Algaeia')
st.markdown("Welcome to *_Algaeia_*! "
            "Check out our documentation on ([GitHub](https://github.com/nathanyaqueby/dodo-hackathon))")

# col1, col2, col3 = st.columns((1,1,2))
st.sidebar.image("algaeia.png", use_column_width=True)

with st.sidebar.form(key='Form1'):
    st.title("VR environment generator")

    Options = ["a-box","a-sphere","a-cylinder","a-plane","a-cone","a-torus-knot","a-ring","a-dodecahedron","a-icosahedron"]
    choose = st.selectbox("Pick a primitive:", Options)

    Options2 = ["ambient","point"]
    choose2 = st.selectbox("Adjust lighting:", Options2)

    Options3 = ["egypt","forest","goaland","yavapai","goldmine","threetowers","poison","arches"]
    choose3 = st.selectbox("Choose Environment:", Options3)

    Options4 = ["yes","no"]
    choose4 = st.radio("Add fog:", Options4)

    generator = st.form_submit_button('Generate environment ⚡')


def audiorec_demo_app():

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # Custom REACT-based component for recording client audio in browser
    build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
    # specify directory and initialize st_audiorec object functionality
    st_audiorec = components.declare_component("st_audiorec", path=build_dir)


    # STREAMLIT AUDIO RECORDER Instance
    val = st_audiorec()
    # web component returns arraybuffer from WAV-blob
    # st.write('Audio data received in the Python backend will appear below this message ...')

    if isinstance(val, dict):  # retrieve audio data
        with st.spinner('retrieving audio-recording...'):
            ind, val = zip(*val['arr'].items())
            ind = np.array(ind, dtype=int)  # convert to np array
            val = np.array(val)             # convert to np array
            sorted_ints = val[ind]
            stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
            wav_bytes = stream.read()

        # wav_bytes contains audio data in format to be further processed
        # display audio data as received on the Python side
        # st.audio(wav_bytes, format='audio/wav')

        return wav_bytes

def writeHelp1():
    st.write('Corresponding Code:')
    st.header("Generated Code:")
    st.write('<html><head>')
    st.write('<script src="https://aframe.io/releases/1.0.4/aframe.min.js"></script>')
    st.write('<script src="https://unpkg.com/aframe-environment-component@1.1.0/dist/aframe-environment-component.min.js"></script>')
    st.write('<script src="https://unpkg.com/aframe-event-set-component@4.2.1/dist/aframe-event-set-component.min.js"></script>')
    st.write('</head><body>')
    st.write('<a-scene>')
    
    
def writeHelp2():
    st.write('</a-scene>')
    st.write('</body></html>') 


if __name__ == '__main__':

    if generator:

        fog = '<a-scene fog="type: exponential; color: #AAA"></a-scene>'

        if choose == "a-box":
            if choose4 == "yes":
                components.html('<html><head><script src="https://aframe.io/releases/1.0.4/aframe.min.js"></script><script src="https://unpkg.com/aframe-environment-component@1.1.0/dist/aframe-environment-component.min.js"></script><script src="https://unpkg.com/aframe-event-set-component@4.2.1/dist/aframe-event-set-component.min.js"></script></head><body><a-scene><a-box position="-1 0.5 -3" rotation="0 0 0" color="#4CC3D9" sound: url(river.mp3); autoplay: true></a-box><a-light type='+choose2+' color="red" position="0 5 0"></a-light> <a-entity environment="preset: '+choose3+'; groundColor: #445; grid: cross">'+fog+'</a-entity></a-scene></body></html>',height=600)
            else:
                components.html('<html><head><script src="https://aframe.io/releases/1.0.4/aframe.min.js"></script><script src="https://unpkg.com/aframe-environment-component@1.1.0/dist/aframe-environment-component.min.js"></script><script src="https://unpkg.com/aframe-event-set-component@4.2.1/dist/aframe-event-set-component.min.js"></script></head><body><a-scene><a-box position="-1 0.5 -3" rotation="0 0 0" color="#4CC3D9" sound: url(river.mp3); autoplay: true></a-box><a-light type='+choose2+' color="red" position="0 5 0"></a-light> <a-entity environment="preset: '+choose3+'; groundColor: #445; grid: cross"></a-entity></a-scene></body></html>', height=600)
            # writeHelp1()
            # st.write('<a-box position="-1 0.5 -3" rotation="0 0 0" color="#4CC3D9"></a-box>')
            # st.write('<a-light type='+choose2+' color="red" position="0 5 0"></a-light>')
            # st.write('<a-entity environment="preset: '+choose3+'; groundColor: #445; grid: cross"></a-entity>')
            # if choose4 == "yes":
            #     st.write(fog)
            # writeHelp2()
    
    audio_file = audiorec_demo_app()