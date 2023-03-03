import os
import openai
import time
from io import BytesIO
from gtts import gTTS
from streamlit.web import cli as stcli
from streamlit import runtime
import streamlit as st
from dotenv import load_dotenv
import streamlit.components.v1 as components
from streamlit_audio_recorder.st_custom_components import st_audiorec
from scipy.io.wavfile import write
import wavio as wv
import whisper
def main():
    openai.api_key = st.secrets['OPEN_AI_KEY']
    st.set_page_config(layout="centered")
    title='<p style="font-family:Algerian; color:Red; align:center; font-size: 42px;">MediFix<p>'
    st.markdown(title,unsafe_allow_html=True)
    st.markdown("Hi, I'm MediFix, powered with AI.\nI'm here to help you with your health issues.\nI can help you with your symptoms and tell you the preventive measures to take.\nI can listen to you and I can also read your symptoms.\nSo, let's get started.")
    inp=st.selectbox("Which input form would you like", ['Text', 'Voice'])
    form = st.form(key="user_settings")
    if inp=="Text":
        with form:
            kw = st.text_input("",placeholder="Enter the symptoms ",key = "en_keyword")
            submit = form.form_submit_button("Generate the preventive measures")
            if submit:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", 
                    messages=[{"role": "user", "content": "What are the preventive measures for symptoms "+kw+" ?"}]
                )
                res=response.choices[0].message["content"]          
                myobj = gTTS(text=res,lang='en', slow=False, tld="co.uk")
                mp3_play=BytesIO()
                myobj.write_to_fp(mp3_play)
                st.audio(mp3_play,format="audio/mp3")
                st.markdown(f"Please take the following precautions ")
                st.write(myobj.text)
    else :
        model=whisper.load_model("base")
        rec=st.button("Record the symptoms")
        text=""
        if rec:
            wav_audio_data = st_audiorec()
            time.sleep(10)
            if wav_audio_data is not None:
                # display audio data as received on the backend
                text=model.transcribe(st.audio(wav_audio_data, format='audio/wav'))

        
        submit = st.button("Generate the preventive measures")
        if submit:
                response = openai.Completion.create(
                model="text-davinci-003",
                prompt="What are the preventive measures for symptoms "+text+" ?",
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
                res=response["choices"][0]["text"]
                myobj = gTTS(text=res,lang='en', slow=False, tld="co.uk")
                mp3_play=BytesIO()
                myobj.write_to_fp(mp3_play)
                st.audio(mp3_play,format="audio/mp3")
                st.markdown(f"Please take the following precautions ")
                st.write(myobj.text)
   
if __name__ == "__main__":
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
