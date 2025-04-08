# TCVD-PRACT1

> CODE OWNER: Alexandre Sánchez, Miguel Aloy

Repositori per a la pràctica 1 de **Tipologia i Cicle de Vida de les Dades** del *Màster Universitari en Ciència de Dades* de la **Universitat Oberta de Catalunya (UOC)**.

## 🧠 Descripció

Aquest projecte desenvolupa un web scraper utilitzant **Python** i **Selenium** per extreure ofertes de treball del portal [Glassdoor.es](https://www.glassdoor.es), focalitzant-se en professions de l'àmbit de la ciència de dades (com *Data Scientist*, *Data Analyst*, *Machine Learning Engineer*, etc.) amb ubicació a Espanya (modificable al conjunt desitjat).

L'script simula la navegació humana per evitar la detecció com a bot, automatitza l'inici de sessió, escriu les cerques, fa scroll i clica el botó *"Más empleos"* per carregar totes les ofertes disponibles. Finalment, emmagatzema les dades obtingudes en format `.csv`.

## 📦 Contingut

- `scraper.py`: script principal amb tota la lògica del crawler.
- `datasets/glassdoor_jobs.csv`: fitxer CSV generat amb els resultats.
- `README.md`: aquest document.
- `requirements.txt`: llibreries necessàries per executar el projecte.
- `resources/chromedriver-linux64/chromedriver`: ChromeDriver necessari per Selenium.

## 🔧 Requisits

- Python ≥ 3.8
- Chrome + ChromeDriver compatible
- Llibreries:
  - `selenium`
  - `fake_useragent`

Instal·lació de dependències:

```bash
pip install -r requirements.txt
```

## ⚙️ Execució

1. Introdueix les teves credencials de Glassdoor a l’script (`EMAIL`, `PASSWORD`) o inputeles per CLI.
2. A la primera part de l'script `source/scraper.py` es troben les diferents opcions de configuració. Es poden modificar per afegir o treure feines, localitzacions o modificar el driver de chrome si la versió utilitzada és diferent:
```python

# Set up ChromeDriver path (Modify this for your system)
CHROMEDRIVER_PATH = "resources/chromedriver-linux64/chromedriver"

# Job titles to search
JOB_TITLES = [
    "Data Scientist", "Data Engineer", "Data Analyst", "Machine Learning Engineer",
    "AI Engineer", "Business Intelligence Analyst", "Big Data Engineer",
    "NLP Engineer", "Data Architect"
]

LOCATIONS = ['España']
```  
3. Executa el script:

```bash
python source/scraper.py
```

3. El resultat es desa en `datasets/glassdoor_jobs.csv`.

## :scroll: Dataset generat

El DOI del dataset generat és [Data related job offers in Glassdoor (2025)](https://doi.org/10.5281/zenodo.15170537)

## 🛡️ Consideracions ètiques i legals

Aquest projecte **només s’utilitza amb finalitats acadèmiques** dins l’assignatura TCVD. Assegura’t de revisar els termes d’ús i el fitxer [`robots.txt`](https://www.glassdoor.es/robots.txt) de Glassdoor abans d’utilitzar el codi fora d’aquest context.

## 📄 Llicència

Aquest treball està protegit sota la llicència **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

> Pots compartir i adaptar el contingut amb atribució, però **no per a ús comercial**.

Més informació: [https://creativecommons.org/licenses/by-nc/4.0/](https://creativecommons.org/licenses/by-nc/4.0/)
