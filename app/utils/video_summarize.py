import re
import os
from dotenv import load_dotenv
load_dotenv()

from pytubefix import YouTube
import ffmpeg # type: ignore
from openai import OpenAI
import whisper

class YoutubeSummarize:
    def __init__(self):
        self.client = OpenAI()

    def baixarVideo(self, link):
        try:
                print(f'Baixando vídeo do link: {link}')
                yt = YouTube(link)
                titulo = yt.title
                video_audio = yt.streams.get_audio_only()

                output_path = '_videos'
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                    print(f'Pasta criada: {output_path}')
                
                title = re.sub(r'[<>:"/\\|?*]', '', titulo)
                title = title.replace("'", "")
                title = title.strip().replace(' ', '_')
                title = f'{title}.mp4'
                video_path = video_audio.download(output_path, title)
                print(f"Baixado vídeo '{titulo}' para '{video_path}'")
                return video_path, title
        except Exception as e:
            print(f"Erro ao baixar vídeo: {e}")
            return None
    
    def audio(self, video_path, title):
        try:
            print("transformando video em audio...")
            
            audio_title = title.replace('.mp4', '.wav')
            output_path = '_audios'
            audio_path = os.path.join(output_path, audio_title)
            
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                print(f'Pasta criada: {output_path}')

            ffmpeg.input(video_path).output(audio_path, format='wav').run()
            print(f"sucesso na conversão do audio em {output_path}")
            return audio_path

        except Exception as e:
            print(f"Erro ao transformar o video em audio: {e}")
            return None
    
    def transcrever_audio(self, audio_path: str) -> str:
        """
        Transcreve o áudio de um arquivo usando a API da OpenAI (Whisper).
        :param audio_path: O caminho para o arquivo de áudio.
        :return: O texto transcrito.
        """
        model = whisper.load_model("turbo")

        try:
            print(f"Transcrevendo o áudio de: {audio_path}")
            transcription = model.transcribe(audio_path)
            print("Transcrição concluída com sucesso.")
            # O Whisper retorna um dict, então acessa o campo 'text'
            if isinstance(transcription, dict):
                return transcription.get('text', '')
            elif hasattr(transcription, 'text'):
                return transcription.text
            else:
                return str(transcription)
        except Exception as e:
            print(f"Erro ao transcrever o áudio: {e}")
            return ""

if __name__ == '__main__':
    yt = YoutubeSummarize()
    link = 'https://youtu.be/7j60jaMapJ0?si=Q2CcYP2uVFzbfFfo'
    path, title = yt.baixarVideo(link)
    if path and title:
        audio_path = yt.audio(path, title)
        if audio_path:
            texto_transcrito = yt.transcrever_audio(audio_path)
            print("\n--- TEXTO TRANSCRITO ---\n")
            print(texto_transcrito)