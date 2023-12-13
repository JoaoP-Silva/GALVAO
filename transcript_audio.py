#imports
import os
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

input_dir = "data/audio/splitted_input/WCF_2002"
output_dir = "data/transcriptions/WCF_2002"

# Wav2Vec pretrained model
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")



for filename in os.listdir(input_dir):

    audio_path = os.path.join(input_dir, filename)

    audio, _ = librosa.load(audio_path, sr = 16000)

    input_values = tokenizer(audio, return_tensors = "pt").input_values
    logits = model(input_values).logits
    prediction = torch.argmax(logits, dim = -1)

    transcription = tokenizer.batch_decode(prediction)[0]

    # Save transcription to TXT file
    txt_filename = f"{filename.split('.')[0]}.txt"
    txt_filepath = os.path.join(output_dir, txt_filename)

    with open(txt_filepath, 'w') as txt_file:
        txt_file.write(transcription)