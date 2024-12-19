#import torch
from flask import Flask, request, render_template, jsonify
import main as m
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import asyncio, sys
from langchain_core.messages import HumanMessage
from agents.build_agents import build 
from IPython.display import Image

app = Flask(__name__)
system = build()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
async def chat():
    user_message = request.form['user_input']
    
    print(user_message)
    """
    Executa o sistema com uma query e retorna a resposta.
    """
    
    if len(sys.argv) < 2:
        print("Erro.")
    query = " ".join(user_message)
    config = {"configurable": {"thread_id": "1"}}

    response = ""
    inputs = {"messages": [HumanMessage(content=query)]}
    async for chunk in system.astream(inputs, config, stream_mode="values"):
        response += chunk["messages"][-1].pretty_print()
    
    return jsonify({"response": response})

@app.route("/voice-to-text", methods=["POST"])
def voice_to_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    audio_file = request.files['file']

    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    audio_seg = AudioSegment.from_file(audio_file)
    wav_io = BytesIO()
    audio_seg.export(wav_io, format='wav')
    wav_io.seek(0)

    r = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_dt = r.record(source)
    try:
        txt = r.recognize_google(audio_dt, language="pt-BR")
        print(f"Transcrição: {txt}")
        return jsonify({"transcription": txt}), 200
    except sr.UnknownValueError:
        return jsonify({"error": "Não foi possível entender o áudio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Erro ao tentar usar o serviço de reconhecimento de fala: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)