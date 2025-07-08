import os  
import json  
import requests  
import subprocess  
import sys  
import tkinter as tk  
from tkinter import filedialog, messagebox
import pygame
import time
import difflib

sys.path.insert(0, './')  
from languages_manager import languages_manager

class LogRedirector:
    def __init__(self, write_callback):
        self.write_callback = write_callback
    def write(self, msg):
        if msg.strip():
            self.write_callback(msg)
    def flush(self):
        pass

class MelodyFinderGUI:  
    def __init__(self):  
        self.window = tk.Tk()  
        self.window.title("MelodyFinder - By @FetoyuDev | Dev Build 2.0")
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config = self.carregar_configuracoes()
        self.is_dark = self.config.get("theme", "light") == "dark"

        # PanedWindow para redimensionar áreas
        self.paned_main = tk.PanedWindow(self.window, orient=tk.VERTICAL, sashrelief=tk.RAISED, bg="#000000", sashwidth=6)
        self.paned_main.pack(fill=tk.BOTH, expand=True)

        # Frame superior: busca e lista de músicas
        self.frame_top = tk.Frame(self.paned_main, bg="#000000")
        self.frame_musica_atual = tk.Frame(self.frame_top)
        self.frame_botoes = tk.Frame(self.frame_musica_atual)
        self.frame_fila_musicas = tk.Frame(self.frame_top)
        self.label_musica_atual = tk.Label(self.frame_musica_atual, text="Procurar:")
        self.label_musica_atual.pack(side=tk.LEFT)
        self.entry_busca = tk.Entry(self.frame_musica_atual)
        self.entry_busca.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # Botões ao lado da barra de pesquisa
        self.button_baixar_musica = tk.Button(self.frame_botoes, text="Baixar Música", command=self.baixar_musica)
        self.button_baixar_musica.pack(side=tk.LEFT, padx=2)
        self.button_baixar_video = tk.Button(self.frame_botoes, text="Baixar Vídeo", command=self.baixar_video)
        self.button_baixar_video.pack(side=tk.LEFT, padx=2)
        self.button_buscar_letras = tk.Button(self.frame_botoes, text="Buscar Letras", command=self.buscar_letras)
        self.button_buscar_letras.pack(side=tk.LEFT, padx=2)
        self.button_tema = tk.Button(self.frame_botoes, text="🌙", command=self.toggle_theme)
        self.button_tema.pack(side=tk.LEFT, padx=2)
        self.button_logs = tk.Button(self.frame_botoes, text="Logs", command=self.abrir_logs)
        self.button_logs.pack(side=tk.LEFT, padx=2)
        self.frame_botoes.pack(side=tk.LEFT)
        self.frame_musica_atual.pack(fill=tk.X)
        self.frame_fila_musicas.pack(fill=tk.BOTH, expand=True)
        # Listbox de músicas
        self.listbox_fila_musicas = tk.Listbox(self.frame_fila_musicas)
        self.listbox_fila_musicas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox_fila_musicas.bind('<Double-1>', self.on_listbox_double_click)
        # Scroll na lista de músicas
        self.scroll_musicas = tk.Scrollbar(self.frame_fila_musicas)
        self.listbox_fila_musicas.config(yscrollcommand=self.scroll_musicas.set)
        self.scroll_musicas.config(command=self.listbox_fila_musicas.yview)
        self.scroll_musicas.pack(side=tk.RIGHT, fill=tk.Y)
        # Adiciona frame_top ao paned_main
        self.paned_main.add(self.frame_top)

        # Frame inferior: player e letras
        self.frame_bottom = tk.Frame(self.paned_main, bg="#000000")
        self.paned_main.add(self.frame_bottom)
        # Paned horizontal para player e letras sincronizadas
        self.paned_player_letras = tk.PanedWindow(self.frame_bottom, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg="#000000", sashwidth=6)
        self.paned_player_letras.pack(fill=tk.BOTH, expand=True)
        # Player
        self.frame_player = tk.Frame(self.paned_player_letras)
        self.label_song_name = tk.Label(self.frame_player, text="Arquivo: -")
        self.label_song_name.pack(side=tk.LEFT, padx=5)
        self.label_time = tk.Label(self.frame_player, text="00:00 / 00:00")
        self.label_time.pack(side=tk.LEFT, padx=5)
        self.label_remaining = tk.Label(self.frame_player, text="Restante: 00:00")
        self.label_remaining.pack(side=tk.LEFT, padx=5)
        self.seek_var = tk.DoubleVar()
        self.seek_bar = tk.Scale(self.frame_player, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.seek_var, showvalue=0, length=200, command=self.on_seek, troughcolor='#1db954', sliderrelief=tk.FLAT)
        self.seek_bar.pack(side=tk.LEFT, padx=5)
        self.button_prev = tk.Button(self.frame_player, text='⏮', command=self.prev_song)
        self.button_prev.pack(side=tk.LEFT, padx=2)
        self.button_play = tk.Button(self.frame_player, text='▶️', command=self.play_pause)
        self.button_play.pack(side=tk.LEFT, padx=2)
        self.button_stop = tk.Button(self.frame_player, text='⏹', command=self.stop_song)
        self.button_stop.pack(side=tk.LEFT, padx=2)
        self.button_next = tk.Button(self.frame_player, text='⏭', command=self.next_song)
        self.button_next.pack(side=tk.LEFT, padx=2)
        self.button_repeat = tk.Button(self.frame_player, text='🔁', command=self.toggle_repeat)
        self.button_repeat.pack(side=tk.LEFT, padx=2)
        self.button_random = tk.Button(self.frame_player, text='🔀', command=self.toggle_random)
        self.button_random.pack(side=tk.LEFT, padx=2)
        # Letras sincronizadas
        self.frame_letras_sync = tk.Frame(self.paned_player_letras, bg="#000000")
        self.text_letras_sync = tk.Text(self.frame_letras_sync, height=8, bg="#000000", fg="#00FF00", insertbackground="#00FF00")
        self.text_letras_sync.pack(fill=tk.BOTH, expand=True)
        self.scroll_letras = tk.Scrollbar(self.frame_letras_sync)
        self.scroll_letras.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_letras_sync.config(yscrollcommand=self.scroll_letras.set)
        self.scroll_letras.config(command=self.text_letras_sync.yview)
        # Adiciona player e letras ao paned horizontal
        self.paned_player_letras.add(self.frame_player)
        self.paned_player_letras.add(self.frame_letras_sync)

        # Redireciona stdout e stderr para o log
        sys.stdout = LogRedirector(self.add_log)
        sys.stderr = LogRedirector(self.add_log)

        self.logs = []
        self.log_window = None
        self.log_text_widget = None

        # Inicialização do player de áudio e variáveis de estado
        pygame.mixer.init()
        self.current_song_path = None
        self.is_playing = False
        self.is_paused = False
        self.repeat_mode = 'none'  # 'none', 'song', 'queue'
        self.random_on = False
        self.song_list = []
        self.song_index = 0
        self.song_length = 0
        self.update_seek = True
        self.play_start_time = 0
        self.paused_time = 0
        self.last_pos = 0

        # Aplicar o tema salvo corretamente
        self.toggle_theme(force=True)
        self.update_player_ui()  # Chama o loop de atualização

    def carregar_configuracoes(self):  
        script_dir = os.path.dirname(os.path.abspath(__file__))  
        config_file = os.path.join(script_dir, "configs.json")  
        try:  
            with open(config_file, "r") as file:  
                return json.load(file)  
        except FileNotFoundError:  
            messagebox.showerror("Erro", "Arquivo de configuração não encontrado")  
            sys.exit(1)  
        except json.JSONDecodeError:  
            messagebox.showerror("Erro", "Erro ao carregar o arquivo de configuração")  
            sys.exit(1)

    def salvar_tema_config(self):
        config_file = os.path.join(self.base_dir, "configs.json")
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
        except Exception:
            config = {}
        config["theme"] = "dark" if self.is_dark else "light"
        try:
            with open(config_file, "w") as f:
                json.dump(config, f, indent=4)
        except Exception:
            pass

    def set_theme(self):
        if self.is_dark:
            bg = "#000000"
            fg = "#FFFFFF"
            entry_bg = "#222222"
            select_bg = "#222222"
        else:
            bg = "#F0F0F0"
            fg = "#000000"
            entry_bg = "#FFFFFF"
            select_bg = "#D0D0D0"
        self.window.configure(bg=bg)
        self.frame_letras_sync.configure(bg=bg)
        self.text_letras_sync.configure(bg=entry_bg, fg=fg, insertbackground=fg)
        # O resto dos widgets será atualizado em toggle_theme

    def toggle_theme(self, force=False):
        if not force:
            self.is_dark = not self.is_dark
            self.salvar_tema_config()
        bg = "#000000" if self.is_dark else "#F0F0F0"
        fg = "#FFFFFF" if self.is_dark else "#000000"
        entry_bg = "#222222" if self.is_dark else "#FFFFFF"
        select_bg = "#222222" if self.is_dark else "#D0D0D0"
        self.window.configure(bg=bg)
        for widget in [self.frame_musica_atual, self.frame_botoes, self.frame_fila_musicas]:
            widget.configure(bg=bg)
        self.frame_letras_sync.configure(bg=bg)
        self.text_letras_sync.configure(bg=entry_bg, fg=fg, insertbackground=fg)
        self.label_musica_atual.configure(bg=bg, fg=fg)
        self.entry_busca.configure(bg=entry_bg, fg=fg, insertbackground=fg)
        self.button_baixar_musica.configure(bg=bg, fg=fg, activebackground=select_bg)
        self.button_baixar_video.configure(bg=bg, fg=fg, activebackground=select_bg)
        self.button_buscar_letras.configure(bg=bg, fg=fg, activebackground=select_bg)
        self.button_tema.configure(bg=bg, fg=fg, activebackground=select_bg)
        self.listbox_fila_musicas.configure(bg=entry_bg, fg=fg, selectbackground=select_bg)
        self.button_tema.configure(text="☀️" if self.is_dark else "🌙")

    def listar_musicas_baixadas(self):
        # Lista todos os arquivos mp3 na pasta de downloads
        mp3_dir = os.path.join(self.base_dir, self.config.get("paths", {}).get("mp3", "downloads/mp3"))
        if not os.path.exists(mp3_dir):
            return []
        return [os.path.join(mp3_dir, f) for f in os.listdir(mp3_dir) if f.lower().endswith('.mp3')]

    def atualizar_fila_musicas(self):
        self.song_list = self.listar_musicas_baixadas()
        self.listbox_fila_musicas.delete(0, tk.END)
        for path in self.song_list:
            self.listbox_fila_musicas.insert(tk.END, os.path.basename(path))

    def baixar_musica(self):  
        # Buscar música no YouTube  
        query = self.entry_busca.get().strip()
        if not query:
            messagebox.showerror("Erro", "Digite o nome da música para buscar.")
            return
        videos = self.pesquisar_videos_youtube(self.config["api_key"], self.config["language"], query)
        if videos:
            self.videos_encontrados = videos
            self.popup_resultados_youtube(videos)
        else:
            messagebox.showerror("Erro", "Nenhum vídeo encontrado.")

    def popup_resultados_youtube(self, videos):
        popup = tk.Toplevel(self.window)
        popup.title("Resultados do YouTube")
        listbox = tk.Listbox(popup, width=60)
        for v in videos:
            listbox.insert(tk.END, f"{v['title']} - {v['channel']}")
        listbox.pack(fill=tk.BOTH, expand=True)
        def baixar_selecionado():
            idx = listbox.curselection()
            if not idx:
                return
            video = videos[idx[0]]
            self.baixar_video_ou_audio(video['url'], video['title'], self.config, modo_video=False)
            popup.destroy()
            self.atualizar_fila_musicas()
            messagebox.showinfo("Sucesso", f"Música '{video['title']}' baixada!")
        btn = tk.Button(popup, text="Baixar Selecionado", command=baixar_selecionado)
        btn.pack(pady=5)

    def baixar_video(self):
        selection = self.listbox_fila_musicas.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um vídeo na lista para baixar.")
            return
        idx = selection[0]
        video = self.videos_encontrados[idx]
        self.baixar_video_ou_audio(video['url'], video['title'], self.config, modo_video=True)
        messagebox.showinfo("Sucesso", f"Vídeo '{video['title']}' baixado!")

    def pesquisar_videos_youtube(self, api_key, idioma, query):  
        SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"  
        params = {  
            "part": "snippet",  
            "q": query,  
            "type": "video",  
            "maxResults": 5,  
            "key": api_key,  
        }  
        response = requests.get(SEARCH_URL, params=params)  
        if response.status_code == 200:  
            data = response.json()  
            videos = []  
            for idx, item in enumerate(data['items'], start=1):  
                video_title = item['snippet']['title']  
                channel_title = item['snippet']['channelTitle']  
                video_id = item['id']['videoId']  
                video_url = f"https://youtube.com/watch?v={video_id}"  
                videos.append({"id": idx, "title": video_title, "channel": channel_title, "url": video_url})  
            return videos
        return []

    def baixar_video_ou_audio(self, url, video_title, config, modo_video=False):  
        # Usar os diretórios do configs.json corretamente
        paths = config.get("paths", {})
        temp_dir = os.path.join(self.base_dir, paths.get("temp", "downloads/temp"))
        mp3_dir = os.path.join(self.base_dir, paths.get("mp3", "downloads/mp3"))
        mp4_dir = os.path.join(self.base_dir, paths.get("mp4", "downloads/mp4"))
        os.makedirs(temp_dir, exist_ok=True)  
        os.makedirs(mp3_dir, exist_ok=True)  
        os.makedirs(mp4_dir, exist_ok=True)  
        if modo_video:
            subprocess.run([  
                "yt-dlp",  
                "-f", "bestvideo+bestaudio",  
                "--merge-output-format", "mp4",  
                "-o", os.path.join(mp4_dir, "%(title)s.%(ext)s"),  
                url  
            ])
        else:
            subprocess.run([  
                "yt-dlp",  
                "-f", "bestaudio",  
                "--extract-audio",  
                "--audio-format", "mp3",  
                "--audio-quality", "0",  
                "-o", os.path.join(temp_dir, "%(title)s.%(ext)s"),  
                url  
            ])  
            mp3_files = [f for f in os.listdir(temp_dir) if f.endswith(".mp3")]  
            for file in mp3_files:  
                os.rename(os.path.join(temp_dir, file), os.path.join(mp3_dir, file))  

    def buscar_letras(self):  
        # Busca letras usando o texto da barra de busca, não o resultado selecionado
        busca = self.entry_busca.get().strip()
        if not busca or " - " not in busca:
            messagebox.showerror("Erro", "Digite na barra de busca no formato: Artista - Música")
            return
        artista, musica = busca.split(" - ", 1)
        musica = musica.strip().lower().replace(' ', '+')
        artista = artista.strip().lower().replace(' ', '+')
        url = f'https://lrclib.net/api/get?artist_name={artista}&track_name={musica}'
        response = requests.get(url)
        if response.status_code == 200:
            try:
                letra = response.json()
                if "syncedLyrics" in letra:
                    self.text_letras_sync.delete(1.0, tk.END)
                    self.text_letras_sync.insert(tk.END, letra["syncedLyrics"])
                else:
                    messagebox.showerror("Erro", "Não foi possível encontrar letras para essa música")
            except ValueError:
                messagebox.showerror("Erro", "Erro ao interpretar a resposta da API como JSON")
        else:
            messagebox.showerror("Erro", f"Erro na requisição. Código HTTP: {response.status_code}")

    def on_listbox_double_click(self, event):
        selection = self.listbox_fila_musicas.curselection()
        if selection:
            idx = selection[0]
            self.song_index = idx
            self.load_song(self.song_list[self.song_index])
            self.play_pause()

    def on_seek(self, value):
        if self.is_playing or self.is_paused:
            try:
                pygame.mixer.music.play(start=float(value))
                self.last_pos = float(value)
                self.play_start_time = time.time() - float(value)
                if self.is_paused:
                    pygame.mixer.music.pause()
            except Exception:
                pass

    def play_pause(self):
        if not self.song_list:
            self.atualizar_fila_musicas()
        if not self.song_list:
            return
        if not self.is_playing:
            if not self.current_song_path:
                self.song_index = 0
                self.load_song(self.song_list[self.song_index])
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.button_play.config(text='⏸️')
            self.play_start_time = time.time() - self.last_pos
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.button_play.config(text='⏸️')
            self.play_start_time = time.time() - self.last_pos
        else:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.button_play.config(text='▶️')
            self.last_pos = self.get_current_pos()

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.button_play.config(text='▶️')
        self.seek_var.set(0)
        self.label_time.config(text="00:00 / 00:00")
        self.label_remaining.config(text="Restante: 00:00")
        self.last_pos = 0

    def next_song(self):
        if not self.song_list:
            return
        self.song_index = (self.song_index + 1) % len(self.song_list)
        self.load_song(self.song_list[self.song_index])
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False
        self.button_play.config(text='⏸️')

    def prev_song(self):
        if not self.song_list:
            return
        self.song_index = (self.song_index - 1) % len(self.song_list)
        self.load_song(self.song_list[self.song_index])
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False
        self.button_play.config(text='⏸️')

    def toggle_repeat(self):
        if self.repeat_mode == 'none':
            self.repeat_mode = 'song'
            self.button_repeat.config(text='🔂')
        elif self.repeat_mode == 'song':
            self.repeat_mode = 'queue'
            self.button_repeat.config(text='🔁')
        else:
            self.repeat_mode = 'none'
            self.button_repeat.config(text='🔁')

    def toggle_random(self):
        self.random_on = not self.random_on
        self.button_random.config(relief=tk.SUNKEN if self.random_on else tk.RAISED)

    def load_song(self, path):
        self.current_song_path = path
        pygame.mixer.music.load(path)
        self.song_length = pygame.mixer.Sound(path).get_length()
        self.label_song_name.config(text=f"Arquivo: {os.path.basename(path)}")
        self.seek_bar.config(to=int(self.song_length))
        self.seek_var.set(0)
        self.label_time.config(text=f"00:00 / {self.format_time(self.song_length)}")
        self.label_remaining.config(text=f"Restante: {self.format_time(self.song_length)}")
        self.last_pos = 0
        self.letra_sincronizada = self.buscar_letra_sincronizada(path)
        self.letras_lidas = self.parse_letra_sincronizada(self.letra_sincronizada) if self.letra_sincronizada else []
        self.text_letras_sync.delete(1.0, tk.END)
        if self.letra_sincronizada:
            self.text_letras_sync.insert(tk.END, self.letra_sincronizada)
        else:
            self.text_letras_sync.insert(tk.END, "Letra sincronizada não encontrada.")

    def buscar_letra_sincronizada(self, song_path):
        lyrics_dir = os.path.join(self.base_dir, self.config.get("paths", {}).get("lyrics", "lyrics"))
        if not os.path.exists(lyrics_dir):
            return None
        song_name = os.path.splitext(os.path.basename(song_path))[0].lower()
        arquivos = [f for f in os.listdir(lyrics_dir) if f.endswith('.txt')]
        if not arquivos:
            return None
        # Similaridade de nomes
        melhor = difflib.get_close_matches(song_name, [os.path.splitext(f)[0].lower() for f in arquivos], n=1, cutoff=0.5)
        if melhor:
            idx = [os.path.splitext(f)[0].lower() for f in arquivos].index(melhor[0])
            letra_path = os.path.join(lyrics_dir, arquivos[idx])
            with open(letra_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def parse_letra_sincronizada(self, letra):
        # Retorna lista de tuplas (segundo, texto)
        import re
        linhas = letra.splitlines()
        result = []
        for linha in linhas:
            match = re.match(r'\[(\d+):(\d+)(?:\.(\d+))?\](.*)', linha)
            if match:
                m, s, ms, texto = match.groups()
                tempo = int(m)*60 + int(s)
                if ms:
                    tempo += int(ms)/100
                result.append((tempo, texto.strip()))
        return result

    def update_player_ui(self):
        # Atualiza tempo e seek
        if self.is_playing or self.is_paused:
            pos = self.get_current_pos()
            if pos > self.song_length:
                pos = self.song_length
            self.seek_var.set(pos)
            self.label_time.config(text=f"{self.format_time(pos)} / {self.format_time(self.song_length)}")
            self.label_remaining.config(text=f"Restante: {self.format_time(self.song_length - pos)}")
        # Atualiza letra sincronizada
        if hasattr(self, 'letras_lidas') and self.letras_lidas:
            pos = self.get_current_pos()
            atual = ''
            for i, (t, texto) in enumerate(self.letras_lidas):
                if pos >= t:
                    atual = texto
            self.text_letras_sync.delete(1.0, tk.END)
            self.text_letras_sync.insert(tk.END, atual)
        self.window.after(500, self.update_player_ui)

    def get_current_pos(self):
        if self.is_playing and not self.is_paused:
            return time.time() - self.play_start_time
        else:
            return self.last_pos

    def format_time(self, seconds):
        seconds = int(seconds)
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"

    def add_log(self, msg):
        self.logs.append(msg)
        if self.log_text_widget:
            self.log_text_widget.insert(tk.END, msg)
            self.log_text_widget.see(tk.END)

    def abrir_logs(self):
        if self.log_window and tk.Toplevel.winfo_exists(self.log_window):
            self.log_window.lift()
            return
        self.log_window = tk.Toplevel(self.window)
        self.log_window.title("Logs do Programa")
        self.log_text_widget = tk.Text(self.log_window, height=20, width=80, bg="#111", fg="#0f0")
        self.log_text_widget.pack(fill=tk.BOTH, expand=True)
        for log in self.logs:
            self.log_text_widget.insert(tk.END, log)
        self.log_text_widget.see(tk.END)
        self.log_window.protocol("WM_DELETE_WINDOW", self.fechar_logs)

    def fechar_logs(self):
        self.log_window.destroy()
        self.log_window = None
        self.log_text_widget = None

    # Chame atualizar_fila_musicas ao iniciar
    def run(self):
        self.atualizar_fila_musicas()
        self.window.mainloop()

if __name__ == "__main__":  
    gui = MelodyFinderGUI()  
    gui.run()