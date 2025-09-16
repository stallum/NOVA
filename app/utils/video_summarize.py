import re
import os
from pytubefix import YouTube
import ffmpeg

class YoutubeDownloader:
    def baixarVideo(self, link):
        try:
            if link != '/back':
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
            else:
                return '/back'
        except Exception as e:
            print(f"Erro ao baixar vídeo: {e}")
            return None
    
    def audio(self, video_path, title): 
        try:
            print("transformando video em audio...")

            # title = re.sub(f'.mp4', '', video_path)

            output_path = '_audios'
            audio_path = f'{output_path}/{title}'
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                print(f'Pasta criada: {output_path}')

            ffmpeg.input(video_path).output(audio_path, format='wav').run()
            print(f"sucesso na conversão do audio em {output_path}")

        except Exception as e:
            print(f"Erro ao transformar o video em audio: {e}")
            return None
    

if __name__ == '__main__':
    yt = YoutubeDownloader()
    link = 'https://youtu.be/VmRynpqImic?si=PPFEso3FWf_NMNT6'
    path, title = yt.baixarVideo(link)
    yt.audio(path, title)