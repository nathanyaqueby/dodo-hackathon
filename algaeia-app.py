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
        'About': "An immersive digital speculative underwater museum. "
        "The project focuses on anthropogenic noise pollution affecting the underwater life, "
        "by analyzing selected data produced by maritime traffic in the Pacific ocean."

        "The project is presented as a work in progress developed during the DODO Hackathon: "
        "it would like to be an invitation for visitors to dive into a speculative underwater museum, "
        "where it is possible to approach the artifacts and listen to noise produced by ships crossing the Pacific Ocean."

        "In this digital environment, the objects represent both visualization and sonification of selected data by the dataset "
        "Pacific Sound (https://doi.org/10.1109/OCEANS.2016.7761363.)."

        "The project would like to raise reflections about anthropogenic activities affecting aquatic environments, "
        "creating awareness about noise pollution, often inaudible to humans, an attempt to make more visible and hearable its "
        "impact of non-human species. Developed by Team Algaeia (Sara Rutz, Nathanya Queby Satrani, Indiara Di Benedetto)."
    }
)

# st.title('Algaeia')
st.markdown("Welcome to *_Algaeia_*! Generate a VR world using the sidebar (left) and explore the soundscape with your arrow keys. "
            "Read more about our project on [GitHub](https://github.com/nathanyaqueby/dodo-hackathon)")

# col1, col2, col3 = st.columns((1,1,2))
st.sidebar.image(os.path.join("images", "algaeia.png"), use_column_width=True)

st.markdown(
    """
<style>
.streamlit-expanderHeader {
    font-size: x-large;
}
</style>
""",
    unsafe_allow_html=True,
)

with st.sidebar.form(key='Form1'):
    st.title("🌏 VR world generator")

    Options = ["a-box","a-sphere","a-cylinder","a-plane","a-cone","a-torus-knot","a-ring","a-dodecahedron","a-icosahedron"]
    choose = st.selectbox("Pick a primitive:", Options)

    Options2 = ["ambient","point"]
    choose2 = st.selectbox("Adjust lighting:", Options2)

    Options3 = ["egypt","forest","goaland","yavapai","goldmine","threetowers","poison","arches"]
    choose3 = st.selectbox("Choose Environment:", Options3)

    Options4 = ["yes","no"]
    choose4 = st.radio("Add fog:", Options4)

    generator = st.form_submit_button('Generate environment ⚡')



#####################
## VR & Soundscape ##
#####################

def audiorec_demo_app():

    with st.sidebar.form(key='Form2'):
        st.title("🎧 Soundscape generator")

        parent_dir = os.path.dirname(os.path.abspath(__file__))
        # Custom REACT-based component for recording client audio in browser
        build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
        # specify directory and initialize st_audiorec object functionality
        st_audiorec = components.declare_component("st_audiorec", path=build_dir)

        wav_bytes = 0
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
        
        audiorec = st.form_submit_button('Create soundscape ⚡')

        return wav_bytes, audiorec


###############
## Dashboard ##
###############

js1 = os.path.join("js", "webxr.js")
js2 = os.path.join("js", "joystick.js")
js3 = os.path.join("js", "camera-cube-env.js")

if __name__ == '__main__':

    if generator:

        with st.spinner('Loading...'):

            fog = '<a-scene fog="type: exponential; color: #064273"></a-scene>'

            audio_file = "hckthn1_sessione.wav"
            cube_path = os.path.join("assets", "Cube.008.gltf")
            prop_path = os.path.join("assets", "propeller.gltf")

            
            if choose4 == "yes":
                components.html('<html><head><script src="https://aframe.io/releases/1.0.4/aframe.min.js"></script>'
                                '<script src="https://cdn.jsdelivr.net/gh/donmccurdy/aframe-extras@v6.1.1/dist/aframe-extras.min.js"></script>'
                                '<script src="https://unpkg.com/aframe-sprite-particles-component@^0.5.0/aframe-sprite-particles-component.js"></script>'
                                '<script src="https://cdn.jsdelivr.net/gh/donmccurdy/aframe-extras@v6.1.0/dist/aframe-extras.min.js"></script>'
                                '<script src="https://unpkg.com/aframe-environment-component@1.1.0/dist/aframe-environment-component.min.js"></script>'
                                '<script src="https://unpkg.com/aframe-event-set-component@4.2.1/dist/aframe-event-set-component.min.js"></script>'
                                '<script type="text/javascript" src="js/webxr.js"></script>'
                                '<script type="text/javascript" src="js/joystick.js"></script>'
                                '<script type="text/javascript" src="js/camera-cube-env.js"></script>'
                                '</head><body><audio controls autoplay><source src="hckthn1_sessione.wav" type="audio/wav">Your browser does not support the audio element.</audio>'
                                '<a-scene shadow="type: basic; autoUpdate: false;">'

                                # asset management system
                                '<a-assets>'
                                    # '<a-asset-item id="Cube.008" src="./assets/Cube.008.gltf"></a-asset-item>'
                                    # '<a-asset-item id="propeller" src="./assets/propeller.gltf"></a-asset-item>'
                                    # '<a-asset-item id="bottle" src="./assets/bottle.gltf"></a-asset-item>'
                                    '<audio id="background" src="https://cdn.aframe.io/basic-guide/audio/backgroundnoise.wav"></audio>'
                                '</a-assets>'

                                # '<a-assets>'
                                #     '<a-asset-item id="Cube.008" src="'+cube_path+'"></a-asset-item>'
                                #     '<a-asset-item id="propeller" src="'+prop_path+'"></a-asset-item>'
                                # '</a-assets>'

                                # '<a-grid src="custom-image.png"></a-grid>'

                                '<a-ocean color="#0000FF" width="100" depth="50" density="15" speed="1"></a-ocean>'

                                # '<a-tube path="5 0 5, 5 0 -5, -5 0 -5" radius="0.5" material="color: red"></a-tube>'

                                # '<a-hexgrid src="hexmap.json" material="color: #47BF92"></a-hexgrid>'
                                '<'+choose+' position="-1 0.5 -3" rotation="0 0 0" color="#4CC3D9" sound="src: #background; autoplay: true; loop: true; volume: 3"></'+choose+'>'
                                '<'+choose+' position="-5 0.5 -3" rotation="0 0 0" color="#4CC3D9" sound="src: #background; autoplay: true; loop: true; volume: 3"></'+choose+'>'
                                '<'+choose+' position="-9 0.5 -6" rotation="0 0 0" color="#4CC3D9" sound="src: #background; autoplay: true; loop: true; volume: 3"></'+choose+'>'

                                
                                # '<a-entity id="#Cube.008" gltf-model="#Cube.008" scale="2 2 2" position="-0.6772575974464417 1.07643868774175644 1.007191523909568787" visible="true" shadow="cast: false"></a-entity>'
                                # '<a-entity id="#propeller" gltf-model="#propeller" scale="1 1 1" position="-10.6772575974464417 0.07643868774175644 0.007191523909568787" visible="true" shadow="cast: false" animation-mixer=""></a-entity>'
                                # '<a-entity id="#Cube.008"  gltf-model="#Cube.008" scale="3.5 3.5 3.5" position="-0.6772575974464417 1.07643868774175644 1.007191523909568787" visible="true" shadow="cast: false" ></a-entity>'
                                # '<a-entity id="#propeller"  gltf-model="#propeller" scale="1 1 1" position="-10.6772575974464417 0.07643868774175644 0.007191523909568787" visible="true" shadow="cast: false" animation-mixer ></a-entity>'
                                # '<a-entity id="#bottle"  gltf-model="#bottle" scale="1.5 1.5 1.5" position="-0.6772575974464417 1.07643868774175644 8.007191523909568787" visible="true" shadow="cast: false" ></a-entity>'

                                # new or additional entities
                                '<a-entity position="0 0 5"><a-camera><a-cursor></a-cursor></a-camera></a-entity>'

                                # '<a-sound src="#waves" autoplay="true"></a-sound>'
                                # '<a-sound src="#background" autoplay="true"></a-sound>'

                                '<a-light type='+choose2+' color="red" position="0 5 0"></a-light> '
                                '<a-entity light="intensity: 1.0; castShadow: false; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2" position="1.36586 7.17965 1"></a-entity>'
                                #'<a-entity light="type: ambient; intensity: 1.0"></a-entity>'
                                '<a-entity environment="preset: '+choose3+'; groundColor: #445; grid: cross" sound="src: hckthn1_sessione.wav; autoplay: true; loop: true">'+fog+'</a-entity>'
                                '</a-scene></body></html>', height=600)
            else:
                components.html('<html><head><script src="https://aframe.io/releases/1.0.4/aframe.min.js"></script>'
                                # '<script src="https://cdn.jsdelivr.net/gh/donmccurdy/aframe-extras@v6.1.1/dist/aframe-extras.min.js"></script>'
                                '<script src="https://unpkg.com/aframe-sprite-particles-component@^0.5.0/aframe-sprite-particles-component.js"></script>'
                                '<script src="https://cdn.jsdelivr.net/gh/donmccurdy/aframe-extras@v6.1.0/dist/aframe-extras.min.js"></script>'
                                '<script src="https://unpkg.com/aframe-environment-component@1.1.0/dist/aframe-environment-component.min.js"></script>'
                                '<script src="https://unpkg.com/aframe-event-set-component@4.2.1/dist/aframe-event-set-component.min.js"></script>'
                                '</head><body><a-scene>'

                                # asset management system ###########################################################################################
                                '<a-assets>'
                                    '<a-asset-item id="Cube.008" src="'+cube_path+'"></a-asset-item>'
                                    '<a-asset-item id="propeller" src="'+prop_path+'"></a-asset-item>'
                                    '<audio id="waves" src="hckthn1_sessione.wav" preload="auto"></audio>'
                                    '<audio id="background" src="https://cdn.aframe.io/basic-guide/audio/backgroundnoise.wav"></audio>'
                                '</a-assets>'

                                '<'+choose+' position="-1 0.5 -3" rotation="0 0 0" color="#4CC3D9" sound="src: #background; autoplay: true; loop: true; volume: 2"></'+choose+'>'
                                '<'+choose+' position="-5 0.5 -3" rotation="0 0 0" color="#4CC3D9" sound="src: #background; autoplay: true; loop: true; volume: 2"></'+choose+'>'
                                '<'+choose+' position="-9 0.5 -6" rotation="0 0 0" color="#4CC3D9" sound="src: #background; autoplay: true; loop: true; volume: 2"></'+choose+'>'

                                # new or additional entities #########################################################################################
                                '<a-entity position="0 0 5"><a-camera><a-cursor></a-cursor></a-camera></a-entity>'
                                '<a-sound src="#waves" autoplay="true"></a-sound>'
                                '<a-entity id="#Cube.008" gltf-model="#Cube.008" scale="2 2 2" position="-0.6772575974464417 1.07643868774175644 1.007191523909568787" visible="true" shadow="cast: false"></a-entity>'
                                '<a-entity id="#propeller" gltf-model="#propeller" scale="1 1 1" position="-10.6772575974464417 0.07643868774175644 0.007191523909568787" visible="true" shadow="cast: false" animation-mixer=""></a-entity>'

                                '<a-light type='+choose2+' color="red" position="0 5 0"></a-light> '
                                '<a-entity environment="preset: '+choose3+'; groundColor: #445; grid: cross" sound="src: '+audio_file+'; autoplay: true"></a-entity>'
                                '</a-scene></body></html>', height=700)
    
        audio_file, audiorec = audiorec_demo_app()
    
    else:

        components.html('<embed src="https://www.sararutz.ch/DODO/index.html" style="width: 100%; height: 800%">')

        # components.html(f'''
        #             <!doctype html>
        #             <html lang="en">
        #                 <!-- Generated automatically by AFRAME Exporter for Blender - https://silverslade.itch.io/a-frame-blender-exporter -->
        #                 <head>
        #                     <title>DODO Hackathon</title>
        #                     <link rel="icon" type="image/png" href="favicon.ico"/>
        #                     <meta name="description" content="3D Application">
        #                     <meta charset="utf-8">
        #                     <meta http-equiv="X-UA-Compatible" content="IE=edge">
        #                     <meta name="viewport" content="width=device-width, initial-scale=1">
        #                     <script src="https://aframe.io/releases/1.0.4/aframe.min.js"></script>
        #                     <script src="https://unpkg.com/aframe-sprite-particles-component@^0.5.0/aframe-sprite-particles-component.js"></script>
        #                     <script src="https://cdn.jsdelivr.net/gh/donmccurdy/aframe-extras@v6.1.0/dist/aframe-extras.min.js"></script>
        #                     <script type="text/javascript" src="{js1}"></script>
        #                     <script type="text/javascript" src="{js2}"></script>
        #                     <script type="text/javascript" src="{js3}"></script>
                            
        #                     <link rel="stylesheet" type="text/css" href="style.css">
        #                 </head>
        #                 <body onload="init();">
        #                     <a-scene   shadow="type: basic; autoUpdate: false;">
        #                         <a-entity position="0 2.25 -15" particle-system="preset: dust; particleCount: 10000"></a-entity>
        #                         <!-- Assets -->
        #                         <a-assets>
        #                             <a-asset-item id="Cube.008" src="./assets/Cube.008.gltf"></a-asset-item>
        #                             <a-asset-item id="propeller" src="./assets/propeller.gltf"></a-asset-item>
        #                             <a-asset-item id="bottle" src="./assets/bottle.gltf"></a-asset-item>
        #                         </a-assets>

        #                         <!-- Entities -->
                                
        #                         <a-entity id="#Cube.008"  gltf-model="#Cube.008" scale="3.5 3.5 3.5" position="-0.6772575974464417 1.07643868774175644 1.007191523909568787" visible="true" shadow="cast: false" ></a-entity>
        #                         <a-entity id="#propeller"  gltf-model="#propeller" scale="1 1 1" position="-10.6772575974464417 0.07643868774175644 0.007191523909568787" visible="true" shadow="cast: false" animation-mixer ></a-entity>
        #                         <a-entity id="#bottle"  gltf-model="#bottle" scale="1.5 1.5 1.5" position="-0.6772575974464417 1.07643868774175644 8.007191523909568787" visible="true" shadow="cast: false" ></a-entity>

        #                         <!-- Camera -->
        #                         <a-entity id="player" 
        #                             position="0 -0.2 0" 
        #                             movement-controls="speed: 0.10000000149011612;">
        #                             <a-entity id="camera" 
        #                                 camera="near: 0.001" 
        #                                 position="0 1.7000000476837158 0" 
        #                                 look-controls="pointerLockEnabled: true">
        #                                     <a-entity id="cursor" cursor="fuse: false;" animation__click="property: scale; startEvents: click; easing: easeInCubic; dur: 50; from: 	0.1 0.1 0.1; to: 1 1 1"
        #                                         position="0 0 -0.1"
        #                                         geometry="primitive: circle; radius: 0.001;"
        #                                         material="color: #CCC; shader: flat;"
        #                                         >
        #                                     </a-entity>
        #                             </a-entity>
        #                                 <a-entity id="leftHand" oculus-touch-controls="hand: left" vive-controls="hand: left"></a-entity>
        #                                 <a-entity id="rightHand" laser-controls oculus-touch-controls="hand: right" vive-controls="hand: right" ></a-entity>
        #                         </a-entity>

        #                         <!-- Lights -->
        #                         <a-entity light="intensity: 1.0; castShadow: false; shadowBias: -0.001; shadowCameraFar: 501.02; shadowCameraBottom: 12; shadowCameraFov: 101.79; shadowCameraNear: 0; shadowCameraTop: -5; shadowCameraRight: 10; shadowCameraLeft: -10; shadowRadius: 2" position="1.36586 7.17965 1"></a-entity>
        #                         <a-entity light="type: ambient; intensity: 1.0"></a-entity>

        #                         <!-- Sky -->
        #                         <a-sky color= 	#0000FF ></a-sky>
        #                     </a-scene>
        #                 </body>
        #             </html>
        #             <!-- Generated automatically by AFRAME Exporter for Blender - https://silverslade.itch.io/a-frame-blender-exporter -->
        #             ''')
    
    with st.expander("🌊 An immersive digital speculative underwater museum"):
        st.markdown("The project focuses on anthropogenic noise pollution affecting the underwater life by analyzing selected data produced by maritime traffic in the Pacific ocean.")
        
        st.markdown("The project is presented as a work in progress developed during the DODO Hackathon: it would like to be an invitation for visitors to dive into a speculative underwater museum, where it is possible to approach the artifacts and listen to noise produced by ships crossing the Pacific Ocean.")

        st.image(os.path.join("images", "screen-satellite.jpg"))

        st.markdown("In this digital environment, the objects represent both visualization and sonification of selected data by the dataset Pacific Sound (https://doi.org/10.1109/OCEANS.2016.7761363).")

        st.markdown("The project would like to raise reflections about anthropogenic activities affecting aquatic environments, creating awareness about noise pollution, often inaudible to humans, an attempt to make more visible and hearable its impact of non-human species.")