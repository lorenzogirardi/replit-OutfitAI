# 🎨 AI Fashion Stylist

Un'applicazione web AI che analizza look di ispirazione e ricostruisce outfit simili utilizzando capi di abbigliamento disponibili.

## ✨ Caratteristiche Principali

- 🤖 **AI Avanzato**: Sistema intelligente per analisi semantica di stili e colori
- 🎯 **3 Modalità di Analisi**: AI Avanzato, Riferimenti di stile, Algoritmo base
- 📸 **Gestione Immagini**: Sistema a 3 livelli per prodotti, riferimenti e look utente
- 🎨 **Analisi Colori**: Estrazione automatica dei colori dominanti
- 👔 **Abbinamenti Intelligenti**: Matching basato su compatibilità di stile e colore
- 🚀 **Facile da Usare**: Interfaccia web intuitiva con Streamlit

## 🚀 Avvio Rapido con Docker

```bash
# 1. Scarica il progetto
git clone [repository-url]
cd ai-fashion-stylist

# 2. Avvia l'applicazione
docker-compose up -d

# 3. Apri il browser
http://localhost:5000
```

## 📁 Struttura Immagini

```
images/
├── products/           # 📦 Capi singoli per comporre outfit
│   ├── shirts/        # Camicie, polo, t-shirt
│   ├── pants/         # Pantaloni, jeans, shorts
│   ├── shoes/         # Scarpe di ogni tipo
│   ├── jackets/       # Giacche, blazer, cardigan
│   └── accessories/   # Cinture, orologi, borse
├── style_references/   # 🎨 Esempi di outfit ben abbinati
└── looks/             # 👤 Look da ricostruire
```

## 🎯 Come Funziona

1. **Carica** un'immagine di ispirazione
2. **L'AI analizza** colori, stili e caratteristiche
3. **Il sistema trova** i migliori abbinamenti dai tuoi capi
4. **Visualizza** l'outfit ricostruito con punteggi di confidenza

## 🛠️ Tecnologie

- **Frontend**: Streamlit
- **AI/ML**: Scikit-learn, OpenCV, TF-IDF
- **Computer Vision**: Analisi colori, rilevamento pattern, feature extraction
- **Containerizzazione**: Docker & Docker Compose

## 📖 Documentazione Completa

- [`DOWNLOAD.md`](DOWNLOAD.md) - Guida download e installazione
- [`SETUP.md`](SETUP.md) - Configurazione dettagliata
- [`replit.md`](replit.md) - Documentazione tecnica

## 🔧 Requisiti Sistema

- Docker e Docker Compose
- 2GB RAM
- Porta 5000 disponibile
- Supporto per immagini JPG/PNG

## 📝 Licenza

Progetto open source per scopi educativi e dimostrativi.

---

**Inizia subito**: `docker-compose up -d` e vai su `http://localhost:5000`!