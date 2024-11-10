# -*- coding: utf-8 -*-
"""Привет!\nВ этой библиотеке Вы увидете некоторые функции [бота Флореста](https://t.me/postbotflorestbot).\nМои социальные сети: [тык](https://taplink.cc/florestone4185)"""

class Cripto():
    """Класс со списком криптовалют, которые доступны для функции `crypto_price`.\nBITKOIN, USDT, DOGECOIN, HAMSTERCOIN"""
    BITKOIN = 'bitcoin'
    USDT = 'tether'
    DOGE = 'dogecoin'
    HMSTR = 'hamster'

class FunctionsObject:
    def __init__(self, proxies: dict = {}, html_headers: dict = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36', 'Accept-Language': 'ru-RU'}, google_api_key: str = "", ):
        """Привет. Именно в данном классе находятся ВСЕ функции бота. Давай я объясню смысл параметров?\nproxies: прокси, которые используются при HTTPS запросах к сайтам.\nhtml_headers: заголовки HTTPS запросов.\ngoogle_api_key: апи ключ гугла. Получить его можно [здесь](https://console.google.com/)"""
        print(f'Объект класса был успешно запущен.')
        self.proxies = proxies
        self.headers = html_headers
        self.google_key = google_api_key
    def generate_image(self, prompt: str) -> bytes:
        from MukeshAPI import api
        """Данная функция генерирует говно-картинки с помощью пиратской нейросети.\nprompt: запрос, по которому надо сгенерировать изображение."""
        return api.ai_image(prompt)
    def ai(self, prompt: str) -> str:
        """Обычный чат-гпт. Бесплатный.\nprompt: что тебе нужно от нейросетки."""
        from g4f.client import Client
        from g4f.Provider import Liaobots

        return Client().chat.completions.create([{"role":"user", "content":prompt}], 'gpt-3.5-turbo', Liaobots).choices[0].message.content
    def deanon(self, ip: str) -> list:
        """Деанончик по IP.\nВы сами принимаете на себя ответственность за использование данной функции.\nip: дай айпи, тварюка."""
        import requests
        r = requests.get(f'http://ip-api.com/json/{ip}?lang=ru', proxies=self.proxies, headers=self.headers).json()
        results = []
        for key, value in r.items():
            results.append(f'{key.title()}: {value}')
        return results
    def download_video(self, url: str):
        """Данная функция качает видео с YouTube с помощью URL.\nurl: ссылка на видео."""
        from pytubefix import YouTube

        yt_obj = YouTube(url, proxies=self.proxies)

        if yt_obj.age_restricted:
            return 'На видео наложены возрастные ограничения.'    
        else:
            import io

            buffer = io.BytesIO()

            yt_obj.streams.get_lowest_resolution().stream_to_buffer(buffer)

            return buffer.getvalue()
    def search_videos(self, query: str):
        """Функция для поиска видео по запросу и дальнейшего его закачивания.\nquery: запрос, по которому надо искать видео."""
        from pytubefix import Search

        search = Search(query, proxies=self.proxies)
        videos = search.videos

        if len(videos) == 0:
            return 'Видео по запросу не существует.'
        else:
            video = videos[0]
            if video.age_restricted:
                return 'На видео, которое мы нашли первым присутствуют возрастные ограничение. Его скачивание невозможно.'  
            else:
                import io

                buffer = io.BytesIO()

                video.streams.get_lowest_resolution().stream_to_buffer(buffer)

                return buffer.getvalue()
    def create_demotivator(self, top_text: str, bottom_text: str, photo: bytes, font: str):
        """Создайте демотиватор с помощью данной фичи!\ntop_text: верхний текст.\nbottom_text: нижний текст.\nphoto: ваша фотография в bytes.\nfont: ваш шрифт. Пример: `times.ttf`."""
        import io
        image = io.BytesIO(photo)
        from PIL import Image, ImageOps, ImageDraw, ImageFont
        img = Image.new('RGB', (1280, 1024), color='black')
        img_border = Image.new('RGB', (1060, 720), color='#000000')
        border = ImageOps.expand(img_border, border=2, fill='#ffffff')
        user_img = Image.open(image).convert("RGBA").resize((1050, 710))
        (width, height) = user_img.size
        img.paste(border, (111, 96))
        img.paste(user_img, (118, 103))
        drawer = ImageDraw.Draw(img)
        font_1 = ImageFont.truetype(font=font, size=80, encoding='UTF-8')
        text_width = font_1.getlength(top_text)

        while text_width >= (width + 250) - 20:
            font_1 = ImageFont.truetype(font=font, size=80, encoding='UTF-8')
            text_width = font_1.getlength(top_text)
            top_size -= 1

        font_2 = ImageFont.truetype(font=font, size=60, encoding='UTF-8')
        text_width = font_2.getlength(bottom_text)

        while text_width >= (width + 250) - 20:
            font_2 = ImageFont.truetype(font=font, size=60, encoding='UTF-8')
            text_width = font_2.getlength(bottom_text)
            bottom_size -= 1

        size_1 = drawer.textlength(top_text, font=font_1)
        size_2 = drawer.textlength(bottom_text, font=font_2)

        drawer.text(((1280 - size_1) / 2, 840), top_text, fill='white', font=font_1)
        drawer.text(((1280 - size_2) / 2, 930), bottom_text, fill='white', font=font_2)

        result_here = io.BytesIO()

        img.save(result_here, 'JPEG')
    
        del drawer

        return result_here.getvalue()
    def photo_make_black(self, photo: bytes):
        """Сделать фото черно-белым.\nphoto: фото в `bytes`."""
        import io
        from PIL import Image
        your_photo = io.BytesIO(photo)

        image = Image.open(your_photo)
        new_image = image.convert('L')
        buffer = io.BytesIO()
        new_image.save(buffer, 'JPEG')
        return buffer.getvalue()
    def check_weather(self, city: str):
        """Проверить погоду в каком-либо городе.\ncity: город, или населенный пункт."""
        import requests
        from bs4 import BeautifulSoup

        r = requests.get(f'https://www.google.ru/search?q=погода+в+{city}', proxies=self.proxies, headers=self.headers)
        if r.status_code != 200:
            return 'Ошибка. Не получилось получить доступ к Google.'
        else:
            try:
                soup = BeautifulSoup(r.text, 'html.parser')
                temperature = soup.select("#wob_tm")[0].getText()
                title = soup.select("#wob_dc")[0].getText()
                humidity = soup.select("#wob_hm")[0].getText()
                time = soup.select("#wob_dts")[0].getText()
                wind = soup.select("#wob_ws")[0].getText()
                veroyatnost = soup.select("#wob_pp")[0].getText()
                return {"temp":temperature, "opisanie":title, 'humidity':humidity, 'time':time, 'wind':wind, 'veroyatnost':veroyatnost}
            except:
                return "Не был найден населенный пункт."
    def create_qr(self, content: str):
        """Создать QR код.\ncontent: что будет нести в себе qr. ссылка, текст..."""
        import qrcode
        import io
        
        buffer = io.BytesIO()
        qr = qrcode.make(content)
        qr.save(buffer, scale=10)
        return buffer.getvalue()
    def get_charts(self):
        """Узнать чарты Я.Музыки."""
        import requests
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,fi;q=0.6,nb;q=0.5,is;q=0.4,pt;q=0.3,ro;q=0.2,it;q=0.1,de;q=0.1',
            'Connection': 'keep-alive',
            'Referer': 'https://music.yandex.ru/chart',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'X-Current-UID': '403036463',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Retpath-Y': 'https://music.yandex.ru/chart',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        params = {
            'what': 'chart',
            'lang': 'ru',
            'external-domain': 'music.yandex.ru',
            'overembed': 'false',
            'ncrnd': '0.23800355071570123',
        }
        result = []
        response = requests.get('https://music.yandex.ru/handlers/main.jsx', params=params, headers=headers, proxies=self.proxies)
        chart = response.json()['chartPositions']
        for track in chart[:10]:
            position = track['track']['chart']['position']
            title = track['track']['title']
            author = track['track']['artists'][0]['name']
            result.append(f"№{position}: {author} - {title}")
        return f'Чарты Яндекс Музыки на данный момент🔥\n🥇{result[0]}\n🥈{result[1]}\n🥉{result[2]}\n{result[3]}\n{result[4]}\n{result[5]}\n{result[6]}\n{result[7]}\n{result[8]}\n{result[9]}'
    def generate_password(self, symbols: int = 15):
        """Сгенерировать пароль.\nsymbols: количество символов в пароле."""
        import string
        import random

        symbols_ascii = list(string.ascii_letters + string.digits)

        random.shuffle(symbols_ascii)

        return ''.join(symbols_ascii[:symbols])
    def text_to_speech(self, text: str, lang: str = 'ru'):
        """Из текста в речь на Python.\ntext: текст для озвучки.\nlang: язык для озвучки. По умолчанию, **русский**."""
        import gtts
        import io

        buffer = io.BytesIO()
        engine = gtts.gTTS(text, lang=lang)
        engine.write_to_fp(buffer)
        return buffer.getvalue()
    def information_about_yt_channel(self, url: str):
        """Узнать информацию о YouTube канале на Python.\nurl: ссылка на канал."""
        if not self.google_key:
            return 'Для использования данной функции нужно указать параметр `google_key` в конструктор класса.'
        else:
            from googleapiclient.discovery import build
            from pytubefix import Channel
            channel = Channel(url, proxies=self.proxies).channel_id
            youtube = build('youtube', 'v3', developerKey=self.google_key)
            request = youtube.channels().list(part='snippet,statistics', id=channel.channel_id)
            response = request.execute()
            return {"url_of_ava":response["items"][0]["snippet"]["thumbnails"]["high"]["url"], "channel_name":response["items"][0]["snippet"]["title"], 'channel_nickname':response["items"][0]["snippet"]["customUrl"], 'country':response["items"][0]["snippet"]["country"], 'total_views':response["items"][0]["statistics"]["viewCount"], 'total_subs':response["items"][0]["statistics"]["subscriberCount"]}
    def crypto_price(self, crypto: str, currency: str = 'rub'):
        """Цена криптовалют.\ncrypto: крипта, которую нужно узнать. Для этого воспользуйтесь константами из класса `Cripto`.\ncurrency: валюта, в которой нужно получить результат. Доступно: `rub`, `usd` и `eur`."""
        import requests
        r = requests.get('https://api.coingecko.com/api/v3/simple/price', params={"ids":crypto, 'vs_currencies':currency}, proxies=self.proxies, headers=self.headers).json()
        if r == {}:
            return "Неправильная валюта, или криптовалюта."
        else:
            try:
                return r[crypto][currency]
            except:
                return "Произошла ошибка. Возможно, были преодолены лимиты API."
    def password_check(self, nickname: str) -> int:
        """Поиск сливов паролей по нику.\nnickname: ник для поиска.\nВозвращает `int`."""
        import requests
        req = requests.get(f'https://api.proxynova.com/comb?query={nickname}&start=0&limit=15', headers=self.headers, proxies=self.proxies)
        if req.status_code == 200:
            return req.json()['count']
    def search_proxies(self) -> list:
        """Данная функция ищет общедоступные HTTP(s) прокси без имени пользователя и пароля для входа."""
        import requests
        from bs4 import BeautifulSoup
        response = requests.get("https://free-proxy-list.net/", headers=self.headers, proxies=self.proxies)
        soup = BeautifulSoup(response.content, 'html.parser')
        proxies_from_site = soup.textarea.text.split('\n')[3:-1]

        normisy = []
        for proxy in proxies_from_site[:100]:
            try:
                req = requests.get(f'http://ip-api.com/json/google.ru?lang=ru', headers=self.headers, proxies={"http":f"http://{proxy}", "https":f'http://{proxy}'}, timeout=3.5)
                if req.status_code == 200:
                    normisy.append(proxy)
                else:
                    pass
            except:
                pass

        return normisy