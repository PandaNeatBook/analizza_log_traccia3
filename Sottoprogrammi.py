
"""
Programma che detiene tutti i sottoprogrammi essenziali al funzionamento al programma principale.

Autore: Dario Cudia
Data: 15/11/2024
"""

import json
from utilities.griglia_di_liste_RO import Tabella2D_RO

def carica_log(percorso_file):
    """
    Questa funzione carica i log da un file JSON.
    
    Parametri:
        percorso_file (str): il percorso del file JSON che contiene i log
    
    Ritorna:
        list: una lista con tutti i log caricati dal file
    
    Solleva eccezioni:
        FileNotFoundError: se il file non esiste
        json.JSONDecodeError: se il file non è un JSON valido
    """
    # Provo ad aprire il file
    try:
        # Apro il file in modalità lettura ('r') 
        with open(percorso_file, 'r') as file:
            # Carico il contenuto JSON del file
            logs = json.load(file)
        
        # Validazione: controllo che sia una lista
        if not isinstance(logs, list):
            raise ValueError("Il file JSON non contiene una lista di log.")
        
        # Validazione: controllo che non sia vuota
        if not logs:
            raise ValueError("Il file JSON è vuoto.")
        
        # Stampo un messaggio di conferma per capire che è andato tutto bene
        print(f"[OK] Caricati {len(logs)} log da '{percorso_file}'")
        
        # Ritorno la lista dei log
        return logs
    
    # Se il file non esiste, sollevo un'eccezione
    except FileNotFoundError:
        raise FileNotFoundError(f"Errore: il file '{percorso_file}' non esiste.")
    
    # Se il file non è un JSON valido, sollevo un'eccezione
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Errore: il file non è un JSON valido.", e.doc, e.pos)


def estrai_utenti_unici(tabella_log):
    """
    Estrae la lista degli utenti unici dai log.
    
    Questa funzione prende la colonna degli utenti e trova 
    tutti gli utenti diversi (senza ripetizioni).
    
    Parametri:
        tabella_log (Tabella2D_RO): la tabella con i log
    
    Ritorna:
        list: lista ordinata degli utenti unici
    """
    # Estraggo la colonna 1 (quella degli utenti)
    # Le colonne partono da 0, quindi colonna 1 è la seconda colonna
    colonna_utenti = tabella_log.get_colonna(1)
    
    # Uso set() per eliminare i duplicati e poi sorted() per ordinare
    utenti_unici = sorted(set(colonna_utenti))
    
    # Stampo quanti utenti unici ho trovato
    print(f"[OK] Trovati {len(utenti_unici)} utenti unici")
    
    # Ritorno la lista
    return utenti_unici


def estrai_eventi_unici(tabella_log):
    """
    Estrae la lista degli eventi unici dai log.
    
    Funziona come estrai_utenti_unici ma per gli eventi.
    Gli eventi stanno nella colonna 4.
    
    Parametri:
        tabella_log (Tabella2D_RO): la tabella con i log
    
    Ritorna:
        list: lista ordinata degli eventi unici
    """
    # Prendo la colonna 4 che contiene gli eventi
    colonna_eventi = tabella_log.get_colonna(4)
    
    # Stessa cosa di prima: set() per eliminare duplicati e sorted() per ordinare
    eventi_unici = sorted(set(colonna_eventi))
    
    # Stampo il risultato
    print(f"[OK] Trovati {len(eventi_unici)} eventi unici")
    
    return eventi_unici


def conta_eventi(tabella_log):
    """
    Conta quante volte compare ogni evento nei log.
    
    Questa funzione conta le occorrenze di ogni tipo di evento.
    Per esempio se "login" compare 5 volte, avrò {"login": 5}.
    
    Parametri:
        tabella_log (Tabella2D_RO): la tabella con i log
    
    Ritorna:
        dict: un dizionario dove la chiave è l'evento e il valore è il numero di volte che compare
    """
    # Prendo la colonna 4 che contiene tutti gli eventi
    colonna_eventi = tabella_log.get_colonna(4)
    
    # Creo un dizionario vuoto per tenere il conteggio
    conteggio = {}
    
    # Scorro tutti gli eventi uno per uno
    for evento in colonna_eventi:
        # Se l'evento è già nel dizionario, incremento il contatore
        if evento in conteggio:
            conteggio[evento] += 1
        # Altrimenti lo aggiungo con valore 1
        else:
            conteggio[evento] = 1
    
    # Stampo un messaggio di conferma
    print(f"[OK] Conteggio eventi completato")
    
    # Ritorno il dizionario con tutti i conteggi
    return conteggio


def salva_risultati(risultati, percorso_file):
    """
    Salva i risultati dell'analisi in un file JSON.
    
    Prende il dizionario con i risultati e lo scrive in un file JSON.
    Uso indent=3 per rendere il file più leggibile.
    
    Parametri:
        risultati (dict): dizionario con i risultati da salvare
        percorso_file (str): dove salvare il file
    
    Solleva eccezioni:
        IOError: se non riesce a scrivere il file
    """
    # Provo a scrivere il file
    try:
        # Apro il file in modalità scrittura ('w')
        with open(percorso_file, 'w') as file:
            # Scrivo il JSON con indentazione per renderlo leggibile
            # ensure_ascii=False serve per mantenere i caratteri accentati
            json.dump(risultati, file, indent=3, ensure_ascii=False)
        
        # Stampo conferma
        print(f"[OK] Risultati salvati in '{percorso_file}'")
    
    # Se c'è un errore nella scrittura, lo segnalo
    except OSError as e:
        raise OSError(f"Errore: impossibile scrivere il file '{percorso_file}': {e}")


def analizza_log(percorso_input, percorso_output):
    """
    Funzione principale che coordina l'analisi dei log.
    
    Questa è la funzione più importante, quella che chiama tutte le altre.
    Fa tutto il processo: carica i dati, li analizza e salva i risultati.
    
    Parametri:
        percorso_input (str): file di input con i log
        percorso_output (str): dove salvare i risultati
    
    Ritorna:
        dict: dizionario con i risultati dell'analisi
    """
    # Stampo un banner per far vedere che il programma è partito
    print("\n" + "="*60)
    print("ANALISI LOG - AVVIO")
    print("="*60 + "\n")
    
    # PASSO 1: Carico i log dal file JSON
    logs = carica_log(percorso_input)
    
    # PASSO 2: Creo la tabella 2D
    tabella_log = Tabella2D_RO(logs)
    
    # Prendo le dimensioni della tabella (righe e colonne)
    righe, colonne = tabella_log.size()
    print(f"[OK] Tabella creata: {righe} righe x {colonne} colonne\n")
    
    # PASSO 3: Estraggo tutte le informazioni che mi servono
    # Chiamo le varie funzioni che ho definito prima
    utenti_unici = estrai_utenti_unici(tabella_log)
    eventi_unici = estrai_eventi_unici(tabella_log)
    conteggio_eventi = conta_eventi(tabella_log)
    
    # PASSO 4: Metto tutto insieme in un dizionario
    risultati = {
        "utenti_unici": utenti_unici,
        "eventi_unici": eventi_unici,
        "conteggio_eventi": conteggio_eventi
    }
    
    # PASSO 5: Salvo i risultati nel file di output
    salva_risultati(risultati, percorso_output)
    
    # Stampo un altro banner per far vedere che ho finito
    print("\n" + "="*60)
    print("ANALISI COMPLETATA CON SUCCESSO!")
    print("="*60 + "\n")
    
    # Ritorno i risultati (così posso anche usarli in altre parti del programma)
    return risultati