from flask import Flask, render_template, request, redirect, url_for
import yt_dlp

app = Flask(__name__, static_url_path='/static')

class Yt():
    def __init__(self):
        self.ydl_opts = {
            'format': 'best',  
            'outtmpl': 'output/%(title)s.%(ext)s',  
        }
        self.ydl_optss = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'output/%(title)s.%(ext)s',
        }

    def download_audio(self, link):
        with yt_dlp.YoutubeDL(self.ydl_optss) as ydl:
            result = ydl.extract_info(link, download=True)
            return result

    def download_video(self, link):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            result = ydl.extract_info(link, download=True)
            return result

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            link = request.form['link']
            option = request.form['option']
            youtube = Yt()

            if option == '1':
                result = youtube.download_video(link)
            elif option == '2':
                result = youtube.download_audio(link)
            else:
                return "Opção inválida"

            if 'entries' in result:
                entries = result['entries']
            else:
                entries = [result]

            return render_template('result.html', entries=entries)

        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
