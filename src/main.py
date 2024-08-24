# -*- coding: utf-8 -*-
"""main.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1K6pLJxIwMUkXL1GLRByKkVB1KwT8_fiL
"""

!pip install pydub
!pip install faster_whisper

!pip freeze>requirements.txt

import os
import time
import warnings
from faster_whisper import WhisperModel
from pydub import AudioSegment
warnings.filterwarnings("ignore", category=UserWarning, module="huggingface_hub")


def extract_audio_from_videos(video_folder_path, audio_folder_path):
    """
    Extrae el audio de archivos MP4 en la carpeta especificada y los guarda en formato MP3.

    Args:
        video_folder_path (str): Ruta de la carpeta que contiene los archivos MP4.
        audio_folder_path (str): Ruta de la carpeta donde se guardarán los archivos MP3 extraídos.

    Returns:
        None
    """
    os.makedirs(audio_folder_path, exist_ok=True)
    mp4_files = [f for f in os.listdir(video_folder_path) if f.endswith('.mp4')]

    for mp4_file in mp4_files:
        video_file_path = os.path.join(video_folder_path, mp4_file)
        audio = AudioSegment.from_file(video_file_path, format="mp4")
        audio_output_path = os.path.join(audio_folder_path, f"{os.path.splitext(mp4_file)[0]}.mp3")
        audio.export(audio_output_path, format="mp3")

        print(f"Audio extraído y guardado exitosamente: {audio_output_path}")

    print("Proceso de extracción de audio completado.")

def transcribe_audio_files(audio_folder_path, model):
    """
    Transcribe archivos de audio MP3 en la carpeta especificada y guarda las transcripciones en archivos de texto.

    Args:
        audio_folder_path (str): Ruta de la carpeta que contiene los archivos MP3.
        model (WhisperModel): Instancia del modelo Whisper para realizar la transcripción.

    Returns:
        None
    """
    audio_files = [f for f in os.listdir(audio_folder_path) if f.endswith('.mp3')]


    for audio_file in audio_files:
        audio_file_path = os.path.join(audio_folder_path, audio_file)
        segments, meta = model.transcribe(audio_file_path, language="es", beam_size=5, best_of=5, patience=2)

        num_segments = len(segments)
        print(f"\nSegmentos generados para {audio_file}: {num_segments}")

        transcript_output_path = os.path.join(audio_folder_path, f"{os.path.splitext(audio_file)[0]}.txt")

        with open(transcript_output_path, "w") as file:
            for segment in segments:
                file.write(segment.text + "\n")

        print(meta)


def main():
    """
    Función principal que coordina la extracción de audio y la transcripción.

    Returns:
        None
    """
    video_folder_path = "/content/drive/MyDrive/MAESTRIA/4 SEMESTRE/Deep Learning/data/17082024/"
    audio_folder_path = "/content/drive/MyDrive/MAESTRIA/4 SEMESTRE/Deep Learning/data/audio/"

    start_time = time.time()

    extract_audio_from_videos(video_folder_path, audio_folder_path)
    model = WhisperModel("base", compute_type="float16")
    transcribe_audio_files(audio_folder_path, model)

    end_time = time.time()
    execution_time = end_time - start_time
    print("-"*30)
    print(f"\nProceso de transcripción completado en {execution_time:.2f} segundos.")

if __name__ == "__main__":
    main()