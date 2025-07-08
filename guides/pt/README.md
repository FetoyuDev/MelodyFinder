# MelodyFinder - Informações Úteis

### Este script permite que você:
1. Pesquise vídeos no YouTube.
2. Baixe os vídeos em MP3 ou MP4.
3. Encontre letras sincronizadas automaticamente.

### Instalação
1. Certifique-se de ter Python,`yt-dlp` e `ffmpeg` instalados.

## Linux
```bash
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install ffmpeg -y && pip3 install yt-dlp
```

## Windows
- Windows+X >> Prompt De Comando (Admin):
```batch
choco install ffmpeg && pip3 install yt-dlp
```

2. Configure o arquivo configs.json conforme necessário (Veja [guides/pt/configs-help.md](esse guia) para mais informações)
# Uso
### Execute o script
```bash
python init.py
```

3. Executando o script
# Pesquisa
### É aqui onde começa, escreva o que você está procurando

# Resultados
### Selecione o número de acordo com o resultado

# Conversão
### Aqui você escolhe se você quer baixar em mp3, ou em mp4

# Sincronização automático
### Após escolher a sua música, o script vai tentar se comunicar com a API
### Porém, as vezes pode falhar