# Guida alla Configurazione - MelodyFinder

Questa guida spiega come configurare il file `configs.json` per personalizzare il comportamento di MelodyFinder.

## Struttura del File di Configurazione

Il file `configs.json` contiene le seguenti impostazioni:

### Chiave API
- **Tipo**: Stringa
- **Descrizione**: La chiave API per YouTube Data API v3.
- **Come ottenerla**:
  1. Vai su [Google Cloud Console](https://console.cloud.google.com/).
  2. Crea un nuovo progetto o selezionane uno esistente.
  3. Abilita l'API YouTube Data v3.
  4. Crea delle credenziali (chiave API).
  5. Copia la chiave API e incollala qui.
- **Esempio**: `"AIzaSyB..."`
- **Nota**: Mantieni questa chiave sicura e non condividerla.

### Lingue
- **Tipo**: Stringa
- **Descrizione**: La lingua dell'interfaccia.
- **Valori possibili**: `"en"` (inglese),  `"es"` (spagnolo), `"it"` (italiano), `"pt"` (portoghese)
- **Esempio**: `"it"`

### Percorsi
- **Tipo**: Oggetto
- **Descrizione**: Percorsi delle cartelle per i file scaricati e temporanei.
- **Sottocampi**:
  - `temp`: Cartella per i file temporanei durante il download.
  - `mp3`: Cartella per i file MP3 scaricati.
  - `mp4`: Cartella per i file MP4 scaricati.
  - `lyrics`: Cartella per i file di testo delle canzoni.
- **Esempio**:
  ```json
  {
    "temp": "downloads/temp",
    "mp3": "downloads/mp3",
    "mp4": "downloads/mp4",
    "lyrics": "lyrics"
  }
  ```
- **Nota**: I percorsi sono relativi alla directory di esecuzione dello script. Assicurati che le cartelle esistano o che lo script possa crearle.

### Temi
- **Tipo**: Stringa
- **Descrizione**: Il tema dell'interfaccia.
- **Valori possibili**: `"dark"`, `"light"`
- **Esempio**: `"dark"`

## Esempio Completo di Configurazione

```json
{
    "api_key": "INSERT_YOUR_YOUTUBE_DATA_API_KEY_HERE",
    "language": "it",
    "paths": {
        "temp": "downloads/temp",
        "mp3": "downloads/mp3",
        "mp4": "downloads/mp4",
        "lyrics": "lyrics"
    },
    "theme": "dark"
}
```

## Note Importanti
- Modifica il file `configs.json` con un editor di testo.
- Riavvia lo script dopo aver apportato modifiche per applicare le nuove impostazioni.
- Se riscontri problemi, verifica che la sintassi JSON sia corretta (usa uno strumento di validazione JSON online).
- Per la sicurezza, non commettere il file `configs.json` con la chiave API reale in un repository pubblico.
