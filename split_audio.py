from pydub import AudioSegment
import os

def convert_to_16k(sample_rate, audio_data):
    if sample_rate != 16000:
        audio_data = audio_data.set_frame_rate(16000)
    return audio_data

def split_audio(input_path, output_path, chunk_duration=238):
    audio = AudioSegment.from_file(input_path)

    # Converting to 16khz
    audio = convert_to_16k(audio.frame_rate, audio)

    start_time = 0
    end_time = chunk_duration * 1000

    while end_time <= len(audio):
        chunk = audio[start_time:end_time]
        
        #The filename is the time in the original video
        filename = f"{start_time//1000}_{end_time//1000}_{os.path.basename(input_path)}"

        chunk.export(os.path.join(output_path, filename), format="wav")

        #Updating time for the next chunk
        start_time = end_time
        end_time += chunk_duration * 1000

    print("END")

input_audio_file = "data/audio/full_input/WCF_2002/WCF_2002.wav"
output_directory = "data/audio/splitted_input/WCF_2002"

split_audio(input_audio_file, output_directory)
