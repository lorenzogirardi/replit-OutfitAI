# Setup Guide - AI Fashion Stylist

## 🚀 Installazione Rapida con Docker

### Prerequisiti
- Docker e Docker Compose installati sul tuo sistema
- Almeno 2GB di RAM disponibili
- Porta 5000 libera

### Metodo 1: Docker Compose (Raccomandato)

```bash
# 1. Scarica il progetto
git clone [repository-url]
cd ai-fashion-stylist

# 2. Avvia l'applicazione
docker-compose up -d

# 3. Apri il browser
http://localhost:5000
```

### Metodo 2: Docker Build Manuale

```bash
# 1. Build dell'immagine
docker build -t ai-fashion-stylist .

# 2. Esegui il container
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/images:/app/images \
  --name fashion-stylist \
  ai-fashion-stylist

# 3. Accedi all'app
http://localhost:5000
```

### Fermare l'Applicazione

```bash
# Con Docker Compose
docker-compose down

# Con Docker manuale
docker stop fashion-stylist
docker rm fashion-stylist
```

## 📥 Download del Progetto

Per scaricare e utilizzare il progetto:

## Organizzazione delle Immagini

### 1. Struttura delle Cartelle

Il sistema utilizza **3 tipi di immagini** organizzate in cartelle specifiche:

```
images/
├── products/              # 📦 PRODOTTI SINGOLI (per comporre outfit)
│   ├── shirts/           # Camicie, polo, t-shirt
│   ├── pants/            # Pantaloni, jeans, shorts  
│   ├── shoes/            # Scarpe di ogni tipo
│   ├── jackets/          # Giacche, blazer, cardigan
│   └── accessories/      # Cinture, orologi, cravatte, occhiali
├── style_references/      # 🎨 RIFERIMENTI DI STILE (per guidare abbinamenti)
└── looks/                # 👤 LOOK UTENTE (immagini da ricostruire)
```

### 2. I Tre Tipi di Immagini Spiegati

#### 📦 **Prodotti Singoli** (`images/products/`)
- **Scopo**: Singoli capi di abbigliamento che l'AI usa per comporre gli outfit
- **Contenuto**: Foto di camicie, pantaloni, scarpe, giacche, accessori
- **Utilizzo**: L'AI seleziona da questi per ricreare l'outfit finale

#### 🎨 **Riferimenti di Stile** (`images/style_references/`)  
- **Scopo**: Esempi di outfit ben abbinati che insegnano all'AI le regole di stile
- **Contenuto**: Look completi che mostrano buoni abbinamenti di colori e stili
- **Utilizzo**: L'AI studia questi per capire come abbinare correttamente i capi

#### 👤 **Look Utente** (`images/looks/`)
- **Scopo**: Immagini caricate dall'utente che vuole ricostruire
- **Contenuto**: Foto di outfit che l'utente trova interessanti
- **Utilizzo**: L'AI analizza questi e li ricostruisce usando i prodotti singoli

### 2. Come Nominare i File

Il sistema riconosce automaticamente colori e stili dai nomi dei file:

#### Esempi di Nomi per Colori:
- `black_dress_shirt.jpg` → Camicia elegante nera
- `white_polo.png` → Polo bianca
- `blue_jeans.jpg` → Jeans blu
- `brown_leather_shoes.jpeg` → Scarpe in pelle marrone

#### Esempi di Nomi per Stili:
- `formal_black_suit.jpg` → Abito formale nero
- `casual_white_tshirt.png` → T-shirt casual bianca
- `business_gray_pants.jpg` → Pantaloni business grigi
- `sporty_blue_shorts.jpeg` → Shorts sportivi blu

### 3. Colori Riconosciuti
- **Base**: black, white, gray, brown, beige
- **Primari**: red, blue, green, yellow
- **Secondari**: navy, pink, purple, orange
- **Speciali**: olive, maroon, teal, silver, gold

### 4. Stili Riconosciuti
- **formal**: Abiti eleganti, cravatte, scarpe oxford
- **business**: Abbigliamento da ufficio
- **casual**: Vestiti informali, jeans, t-shirt
- **sporty**: Abbigliamento sportivo e atletico
- **trendy**: Capi alla moda e moderni
- **elegant**: Stile raffinato e sofisticato
- **classic**: Stile classico e senza tempo

### 5. Formati Supportati
- JPG, JPEG, PNG
- Risoluzione minima consigliata: 300x300 pixel
- Per le scarpe: 300x200 pixel
- Per i look completi: 400x600 pixel

### 6. Primi Passi

1. **Crea le cartelle**: L'app può creare automaticamente la struttura
2. **Aggiungi le immagini**: Carica i tuoi indumenti nelle cartelle appropriate
3. **Nomina correttamente**: Usa nomi descrittivi con colore e stile
4. **Testa il sistema**: Carica un look di ispirazione e vedi la ricostruzione

### 7. Consigli per Migliori Risultati

#### Per gli Indumenti:
- Usa sfondi neutri (bianco o grigio)
- Assicurati che l'indumento sia ben visibile
- Evita ombre eccessive
- Una foto per indumento

#### Per i Look di Ispirazione:
- Figure complete (testa-piedi)
- Buona illuminazione
- Colori ben definiti
- Stili chiari e riconoscibili

### 8. Risoluzione Problemi

**Le immagini non si caricano:**
- Verifica che i file siano nei formati supportati
- Controlla che i nomi non contengano caratteri speciali
- Assicurati che le cartelle esistano

**L'AI non trova buone corrispondenze:**
- Aggiungi più varietà di indumenti
- Usa nomi di file più descrittivi
- Verifica che i colori siano ben visibili nelle foto

**Prestazioni lente:**
- Riduci la dimensione delle immagini se troppo grandi
- Limita il numero di immagini per categoria (max 20-30)

## Come Funziona il Sistema

### Flusso di Lavoro Completo:

1. **Preparazione**:
   - Aggiungi i tuoi prodotti singoli in `images/products/`
   - Carica riferimenti di stile in `images/style_references/`
   - Opzionalmente, salva look da ricostruire in `images/looks/`

2. **Analisi dell'Immagine**:
   - L'utente carica un'immagine (upload diretto o da cartella looks)
   - L'AI estrae colori dominanti e caratteristiche di stile
   - Il sistema identifica il riferimento di stile più simile

3. **Ricostruzione Intelligente**:
   - L'AI cerca nei prodotti singoli quelli più compatibili
   - Applica le regole apprese dai riferimenti di stile  
   - Calcola punteggi di corrispondenza per ogni capo

4. **Risultato**:
   - Mostra l'outfit ricostruito con i migliori abbinamenti
   - Indica quale riferimento di stile ha guidato la scelta
   - Fornisce punteggi di confidenza per ogni capo

### Modalità di Utilizzo:

- **🔍 Con Riferimenti di Stile** (consigliato): Usa i template per abbinamenti più accurati
- **⚡ Algoritmo Base**: Matching semplificato senza riferimenti di stile