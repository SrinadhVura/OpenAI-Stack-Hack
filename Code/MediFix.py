import os
import openai
from io import BytesIO
from gtts import gTTS
from streamlit.web import cli as stcli
from streamlit import runtime
import streamlit as st
from dotenv import load_dotenv
def main():
    title='<p style="font-family:Algerian; color:Red; align:center; font-size: 42px;">MediFix<p>'
    st.markdown(title,unsafe_allow_html=True)
    form = st.form(key="user_settings")
    with form:
# openai.api_key = os.getenv("OPENAI_API_KEY")
        symps='<p style="font-family:Brush Script MT; color:Yellow; font-size: 32px;">Symptoms</p>'
        # record=Button(canvas, text='Record',font="Times 15 bold", command=record)
        # canvas.create_window(150, 50, window=record, height=25, width=100)
        # model = whisper.load_model("base")
        # text = model.transcribe("recorded.wav")
        st.markdown(symps,unsafe_allow_html=True)

        kw = st.text_input("",placeholder="Enter the symptoms ",key = "en_keyword")
        openai.api_key = "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"
        submit = form.form_submit_button("Generate the preventive measures")
        if submit:
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt="What are the preventive measures for symptoms "+kw+" ?",
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
