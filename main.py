
"""
Programma per analizzare log anonimizzati e estrarre informazioni statistiche.
L'obiettivo è leggere dei file di log e fare delle statistiche su utenti ed eventi.

Autore: Dario Cudia
Data: 15/11/2024
"""

# Importo le librerie necessarie
import json  # serve per leggere e scrivere file JSON

# Importo tutte le funzioni dal modulo Sottoprogrammi
from sottoprogrammi import (
    carica_log,
    estrai_utenti_unici,
    estrai_eventi_unici,
    conta_eventi,
    salva_risultati,
    analizza_log
)


def main():
    """
    Funzione principale che gestisce l'esecuzione del programma.
    
    Questa funzione viene chiamata quando si avvia il programma.
    Gestisce gli argomenti da linea di comando e coordina tutto.
    """
    # Ho messo dei valori di default per fare le prove più facilmente
    # Se non specifico i file, usa questi
    default_input = input("inserisci il path da cui prendere i log (default: test_data/test_simple.json): ") 
    default_output = input("inserisci il path dove salvare i risultati (default: risultati.json): ")
    
    # Controllo se è stato specificato un file di input
    if default_input != "":
        percorso_input = default_input
    else:
        # Se non c'è, uso il default
        default_input= "test_data/test_simple.json"
        percorso_input = default_input
        print(f"Nessun file di input specificato, uso ilanalizza default: '{default_input}'")
    
    # Controllo se è stato specificato un file di output
    if default_output != "":
        percorso_output = default_output
    else:
        # Se non c'è, uso il default
        default_output= "risultati.json"
        percorso_output = default_output
        print(f"Nessun file di output specificato, uso il default: '{default_output}'")
    
    # Eseguo l'analisi con gestione degli errori
    # Il try-except serve per catturare eventuali errori e gestirli bene
    try:
        # Chiamo la funzione principale che fa tutto il lavoro
        risultati = analizza_log(percorso_input, percorso_output)
        
        # Stampo un riepilogo dei risultati
        print("\n--- RIEPILOGO ---")
        print(f"   * Utenti unici: {len(risultati['utenti_unici'])}")
        print(f"   * Eventi unici: {len(risultati['eventi_unici'])}")
        # Sommo tutti i valori del dizionario conteggio_eventi per avere il totale
        print(f"   * Log totali analizzati: {sum(risultati['conteggio_eventi'].values())}")
        
    # Gestione degli errori specifici
    except FileNotFoundError as e:
        # Se il file non esiste
        print(f"\n[ERRORE] {e}")
        
    
    except json.JSONDecodeError as e:
        # Se il JSON non è valido
        print(f"\n[ERRORE] {e}")
    
    
    except Exception as e:
        # Per qualsiasi altro errore imprevisto
        print(f"\n[ERRORE] Errore inaspettato: {e}")
        


# Questa è la parte che fa partire il programma
if __name__ == "__main__":
    main()
