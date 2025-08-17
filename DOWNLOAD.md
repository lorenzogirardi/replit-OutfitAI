# Download e Utilizzo - AI Fashion Stylist

## 📦 Come Scaricare il Progetto

### Opzione 1: Download ZIP
1. Vai alla pagina del progetto
2. Clicca "Download ZIP" 
3. Estrai il file in una cartella
4. Segui le istruzioni di installazione

### Opzione 2: Git Clone
```bash
git clone [repository-url]
cd ai-fashion-stylist
```

## 🐳 Utilizzo con Docker (Raccomandato)

### Installazione Rapida
```bash
# 1. Posizionati nella cartella del progetto
cd ai-fashion-stylist

# 2. Avvia con Docker Compose
docker-compose up -d

# 3. Apri il browser
http://localhost:5000
```

### Gestione Container
```bash
# Visualizza log
docker-compose logs -f

# Ferma l'applicazione
docker-compose down

# Riavvia
docker-compose restart

# Aggiorna l'immagine
docker-compose pull && docker-compose up -d
```

## 🛠️ Installazione Locale (Senza Docker)

### Prerequisiti
- Python 3.11+
- pip package manager

### Installazione
```bash
# 1. Crea ambiente virtuale
python -m venv venv

# 2. Attiva ambiente virtuale
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Installa dipendenze
pip install streamlit opencv-python scikit-learn matplotlib numpy pandas Pillow

# 4. Avvia l'applicazione
streamlit run app.py --server.port 5000
```

## 📁 Struttura del Progetto Scaricato

```
ai-fashion-stylist/
├── app.py                    # Applicazione principale
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Orchestrazione Docker
├── SETUP.md                 # Guida configurazione
├── DOWNLOAD.md              # Questa guida
├── replit.md                # Documentazione tecnica
├── .streamlit/
│   └── config.toml          # Configurazione Streamlit
├── utils/                   # Moduli AI e processing
│   ├── clip_analyzer.py     # Sistema AI avanzato
│   ├── style_matcher.py     # Algoritmo abbinamenti
│   ├── image_processing.py  # Elaborazione immagini
│   ├── color_analysis.py    # Analisi colori
│   ├── outfit_matcher.py    # Matching outfit
│   └── image_loader.py      # Gestione immagini
├── data/
│   └── sample_clothing.py   # Dati di esempio
└── images/                  # Le tue immagini
    ├── products/            # Prodotti singoli
    │   ├── shirts/
    │   ├── pants/
    │   ├── shoes/
    │   ├── jackets/
    │   └── accessories/
    ├── style_references/     # Riferimenti di stile
    └── looks/               # Look da ricostruire
```

## 🎨 Aggiungere le Tue Immagini

### 1. Prodotti Singoli (images/products/)
- **shirts/**: Camicie, polo, t-shirt
- **pants/**: Pantaloni, jeans, shorts
- **shoes/**: Scarpe di ogni tipo
- **jackets/**: Giacche, blazer, cardigan  
- **accessories/**: Cinture, orologi, borse

### 2. Riferimenti di Stile (images/style_references/)
- Outfit completi ben abbinati
- Esempi di stili che vuoi emulare
- Combinazioni di colori preferite

### 3. Look da Ricostruire (images/looks/)
- Immagini di outfit che vuoi ricreare
- Foto di ispirazione fashion
- Look trovati online o sui social

## 🔧 Risoluzione Problemi

### L'applicazione non si avvia
```bash
# Verifica che Docker sia in esecuzione
docker --version

# Controlla la porta 5000
netstat -an | grep 5000

# Visualizza i log
docker-compose logs fashion-stylist
```

### Immagini non vengono caricate
- Verifica che le immagini siano in formato JPG, PNG o JPEG
- Controlla che siano nelle cartelle corrette
- Riavvia l'applicazione dopo aver aggiunto nuove immagini

### Performance lente
- Riduci la dimensione delle immagini (max 800x600px)
- Limita il numero di immagini per categoria (max 30)
- Usa il formato JPEG per immagini più leggere

## 📋 Checklist Post-Download

- [ ] Docker installato e funzionante
- [ ] Progetto scaricato ed estratto
- [ ] Porta 5000 disponibile
- [ ] Immagini aggiunte nelle cartelle corrette
- [ ] Applicazione avviata con `docker-compose up -d`
- [ ] Browser aperto su `http://localhost:5000`
- [ ] Test di upload e analisi completato

## 🆘 Supporto

Se incontri problemi:
1. Verifica la checklist sopra
2. Controlla i log con `docker-compose logs`
3. Riavvia con `docker-compose restart`
4. Per problemi persistenti, ricrea il container:
   ```bash
   docker-compose down
   docker-compose up -d --force-recreate
   ```

## 🔄 Aggiornamenti

Per aggiornare il progetto:
```bash
# 1. Scarica la nuova versione
git pull  # o re-download del ZIP

# 2. Ricostruisci il container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```