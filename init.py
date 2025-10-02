
import os
import json
import requests
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import time
import threading
import shutil

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

        # videos_encontrados guardará resultados da última busca (se houver)
        self.videos_encontrados = []

        # Aplicar o tema salvo corretamente
        self.toggle_theme(force=True)
        self.atualizar_fila_musicas()
        # Inicia loop de atualização do player (UI)
        self.window.after(500, self.update_player_ui)

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
        query = self.entry_busca.get().strip()
        if not query:
            messagebox.showerror("Erro", "Digite o nome da música para buscar.")
            return
        # pesquisar no YouTube (usa chave do configs.json)
        videos = self.pesquisar_videos_youtube(self.config.get("api_key", ""), self.config.get("language", ""), query)
        if videos:
            self.videos_encontrados = videos
            self.popup_resultados_youtube(videos)
        else:
            messagebox.showerror("Erro", "Nenhum vídeo encontrado ou erro na pesquisa. Cheque sua API Key e conexão.")

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
                messagebox.showwarning("Atenção", "Selecione um item para baixar.")
                return
            video = videos[idx[0]]
            # roda o download em thread para não travar a UI
            threading.Thread(target=self._baixar_em_thread, args=(video['url'], video['title'], False, popup), daemon=True).start()

        btn = tk.Button(popup, text="Baixar Selecionado", command=baixar_selecionado)
        btn.pack(pady=5)

    def baixar_video(self):
        # botão "Baixar Vídeo" da UI principal: baixa a seleção da lista local (se for um vídeo)
        selection = self.listbox_fila_musicas.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um item na lista de músicas (baixadas) para baixar o vídeo correspondente.")
            return
        idx = selection[0]
        if idx < 0 or idx >= len(self.videos_encontrados):
            messagebox.showerror("Erro", "Não há informações do vídeo correspondente. Faça a busca novamente e baixe a partir dos resultados.")
            return
        video = self.videos_encontrados[idx]
        threading.Thread(target=self._baixar_em_thread, args=(video['url'], video['title'], True, None), daemon=True).start()

    def pesquisar_videos_youtube(self, api_key, idioma, query):
        SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 8,
            "key": api_key,
        }
        try:
            response = requests.get(SEARCH_URL, params=params, timeout=10)
        except Exception as e:
            print(f"Erro na requisição de busca: {e}")
            return []
        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                return []
            videos = []
            for idx, item in enumerate(data.get('items', [])):
                video_title = item['snippet']['title']
                channel_title = item['snippet']['channelTitle']
                video_id = item['id'].get('videoId')
                if not video_id:
                    continue
                video_url = f"https://youtube.com/watch?v={video_id}"
                videos.append({"id": idx+1, "title": video_title, "channel": channel_title, "url": video_url})
            return videos
        else:
            print("YouTube API retornou status:", response.status_code, response.text)
        return []

    def _baixar_em_thread(self, url, video_title, modo_video=False, popup=None):
        """Wrapper para executar baixar_video_ou_audio em thread e informar o usuário."""
        try:
            self.add_log(f"Iniciando download: {video_title} ({'vídeo' if modo_video else 'áudio'})\n")
            success = self.baixar_video_ou_audio(url, video_title, self.config, modo_video=modo_video)
            if success:
                self.add_log("Download finalizado com sucesso.\n")
                # atualizar a lista de músicas baixadas na UI (chamar via after)
                self.window.after(200, self.atualizar_fila_musicas)
                if popup:
                    try:
                        popup.destroy()
                    except Exception:
                        pass
                messagebox.showinfo("Sucesso", f"{'Vídeo' if modo_video else 'Música'} '{video_title}' baixado!")
            else:
                messagebox.showerror("Erro", f"Falha ao baixar '{video_title}'. Confira os logs.")
        except Exception as e:
            self.add_log(f"Erro no thread de download: {e}\n")
            messagebox.showerror("Erro", f"Erro ao baixar: {e}")

    def baixar_video_ou_audio(self, url, video_title, config, modo_video=False):
        # retorna True/False se o download ocorreu OK
        paths = config.get("paths", {})
        temp_dir = os.path.join(self.base_dir, paths.get("temp", "downloads/temp"))
        mp3_dir = os.path.join(self.base_dir, paths.get("mp3", "downloads/mp3"))
        mp4_dir = os.path.join(self.base_dir, paths.get("mp4", "downloads/mp4"))
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(mp3_dir, exist_ok=True)
        os.makedirs(mp4_dir, exist_ok=True)

        # Verifica se yt-dlp está disponível
        try:
            subprocess.run(["yt-dlp", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except Exception as e:
            self.add_log("Erro: yt-dlp não encontrado. Instale 'yt-dlp' e tente novamente.\n")
            return False

        try:
            if modo_video:
                cmd = [
                    "yt-dlp",
                    "-f", "bestvideo+bestaudio",
                    "--merge-output-format", "mp4",
                    "-o", os.path.join(mp4_dir, "%(title)s.%(ext)s"),
                    url
                ]
                proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if proc.returncode != 0:
                    self.add_log(f"yt-dlp erro (vídeo): {proc.stderr}\n")
                    return False
                return True
            else:
                # Baixar áudio para temp e converter para mp3
                cmd = [
                    "yt-dlp",
                    "-f", "bestaudio",
                    "--extract-audio",
                    "--audio-format", "mp3",
                    "--audio-quality", "0",
                    "-o", os.path.join(temp_dir, "%(title)s.%(ext)s"),
                    url
                ]
                proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if proc.returncode != 0:
                    self.add_log(f"yt-dlp erro (áudio): {proc.stderr}\n")
                    return False
                # Mover mp3(s) do temp para mp3_dir
                mp3_files = [f for f in os.listdir(temp_dir) if f.lower().endswith(".mp3")]
                if not mp3_files:
                    self.add_log("Nenhum arquivo .mp3 gerado pelo yt-dlp.\n")
                    return False
                for file in mp3_files:
                    src = os.path.join(temp_dir, file)
                    dst = os.path.join(mp3_dir, file)
                    try:
                        shutil.move(src, dst)
                    except Exception as e:
                        self.add_log(f"Erro movendo arquivo {file}: {e}\n")
                        try:
                            # tentativa alternativa: copiar e remover
                            shutil.copy2(src, dst)
                            os.remove(src)
                        except Exception as e2:
                            self.add_log(f"Falha ao mover/copy {file}: {e2}\n")
                            return False
                return True
        except Exception as e:
            self.add_log(f"Erro no download: {e}\n")
            return False

    def buscar_letras(self):
        busca = self.entry_busca.get().strip()
        if not busca or " - " not in busca:
            messagebox.showerror("Erro", "Digite na barra de busca no formato: Artista - Música")
            return
        artista, musica = busca.split(" - ", 1)
        musica = musica.strip().lower().replace(' ', '+')
        artista = artista.strip().lower().replace(' ', '+')
        url = f'https://lrclib.net/api/get?artist_name={artista}&track_name={musica}'
        try:
            response = requests.get(url, timeout=10)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na requisição: {e}")
            return
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
                # pygame.mixer.music.play(start=...) só funciona em algumas plataformas; aqui tentamos set_pos se possível
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
        try:
            self.current_song_path = path
            pygame.mixer.music.load(path)
            self.song_length = pygame.mixer.Sound(path).get_length()
            self.label_song_name.config(text=f"Arquivo: {os.path.basename(path)}")
            self.seek_bar.config(to=int(self.song_length))
            self.seek_var.set(0)
            self.label_time.config(text=f"00:00 / {self.format_time(self.song_length)}")
        except Exception as e:
            self.add_log(f"Erro carregando música: {e}\n")

    def format_time(self, seconds):
        try:
            seconds = int(seconds)
            m = seconds // 60
            s = seconds % 60
            return f"{m:02d}:{s:02d}"
        except Exception:
            return "00:00"

    def get_current_pos(self):
        # estimativa baseada em play_start_time e paused_time
        if not self.is_playing:
            return self.last_pos
        try:
            if self.is_paused:
                return self.last_pos
            return time.time() - self.play_start_time
        except Exception:
            return 0

    def update_player_ui(self):
        # Atualiza barra de progresso e labels
        try:
            if self.is_playing and not self.is_paused:
                pos = self.get_current_pos()
                if pos < 0:
                    pos = 0
                if self.song_length:
                    if pos >= self.song_length - 0.5:
                        # fim da faixa
                        if self.repeat_mode == 'song':
                            self.load_song(self.current_song_path)
                            pygame.mixer.music.play()
                        else:
                            self.next_song()
                    else:
                        self.seek_var.set(pos)
                        self.label_time.config(text=f"{self.format_time(pos)} / {self.format_time(self.song_length)}")
                        remaining = max(0, int(self.song_length - pos))
                        self.label_remaining.config(text=f"Restante: {self.format_time(remaining)}")
            # agenda próxima atualização
        except Exception as e:
            self.add_log(f"Erro update UI: {e}\n")
        self.window.after(500, self.update_player_ui)

    def abrir_logs(self):
        if self.log_window and tk.Toplevel.winfo_exists(self.log_window):
            self.log_window.lift()
            return
        self.log_window = tk.Toplevel(self.window)
        self.log_window.title("Logs")
        self.log_text_widget = tk.Text(self.log_window, height=20, width=80)
        self.log_text_widget.pack(fill=tk.BOTH, expand=True)
        self.log_text_widget.insert(tk.END, "".join(self.logs))

    def add_log(self, msg):
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S] ")
        self.logs.append(timestamp + msg)
        # manter apenas últimos 2000 linhas para não explodir a memória
        if len(self.logs) > 2000:
            self.logs = self.logs[-2000:]
        if self.log_text_widget:
            try:
                self.log_text_widget.insert(tk.END, timestamp + msg)
                self.log_text_widget.see(tk.END)
            except Exception:
                pass

def main():
    app = MelodyFinderGUI()
    app.window.mainloop()

if __name__ == "__main__":
    main()