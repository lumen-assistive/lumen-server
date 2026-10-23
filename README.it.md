# lumen-server

Italiano | [English](README.md)

Il backend opzionale per [Lumen](https://github.com/lumen-assistive):
associazione dei dispositivi dei caregiver, sincronizzazione cifrata
end-to-end e metadati dei pacchetti di modelli. FastAPI + PostgreSQL +
Docker Compose.

Le funzioni essenziali di Lumen funzionano interamente offline; questo
server esiste solo per le funzioni che richiedono un coordinamento tra
dispositivi (il telefono di un caregiver e quello della persona che
assiste) o tra un dispositivo e un futuro punto di distribuzione dei
modelli. Non vede mai dati personali in chiaro: voci di calendario,
stato giornaliero e registrazioni simili vengono cifrate sul
dispositivo prima del caricamento e qui vengono salvate come blob
opachi.

## Stato attuale

- Associazione dispositivi: `POST /api/v1/pairing` crea un account
  caregiver e un dispositivo associato, restituendo un token.
- Sincronizzazione cifrata: `POST /api/v1/blobs` e `GET /api/v1/blobs`
  salvano e recuperano payload opachi cifrati dal client, organizzati
  per categoria (ad esempio `daily-status`, `calendar`). Il server non
  può decifrarli.
- Metadati dei modelli: `GET /api/v1/models` restituisce il catalogo
  dei pacchetti di modelli. Parte vuoto: nessun modello è ancora stato
  convertito, misurato o verificato a livello di licenza. Questo
  endpoint non serve mai i file binari dei modelli.

Non ancora in ambito: notifiche push verso i dispositivi dei caregiver,
account multi-dispositivo oltre al flusso di associazione sopra
descritto, e il catalogo reale dei modelli (popolato quando esisterà
`lumen-models`).

## Esecuzione in locale

```
docker compose up --build
```

Avvia l'API su `http://localhost:8000` e un database PostgreSQL.
Applica le migrazioni una volta avviati i container:

```
docker compose exec app alembic upgrade head
```

`GET /health` è il controllo di attività.

## Sviluppo

Vedi [CONTRIBUTING.md](CONTRIBUTING.md) per il flusso di lavoro completo
(in inglese, come tutto il codice e la documentazione tecnica del
progetto).

## Licenza

Apache License 2.0, vedi [LICENSE](LICENSE).
