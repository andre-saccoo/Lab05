import flet as ft
#from flet.core import page
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    # Definisco il titolo della pagina, gli allineamenti, il tema si partenza, le dimensioni iniziali quando lanci il programma e
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width=800
    page.window.height = 800

    # --- ALERT ---
    # messaggio di allerta
    alert = AlertManager (page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    #inizializzo l'autonoleggio con il nome e il responsabile
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text( value=f"Responsabile: {autonoleggio.responsabile}", size=16, weight=ft.FontWeight.BOLD )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    input_marca = ft.TextField( label="marca", expand=True)    #width= dimensione fissa
    input_modello = ft.TextField( label="modello", expand=True)     #extend espande le caselle quando allarghi la schermata
    input_anno=ft.TextField( label="anno", expand=True)
    valore_output = ft.TextField(value="1", disabled=True, label="numero posti", width=70, border_color="blue")
    def decrementa(e):
         try:
            valore=valore_output.value
            # prendo il campo, controllo che la conversione vada a buon fine e che il contatore non vada sotto 1
            if int(valore) > 1:
                valore_output.value=str(int(valore)-1)
                valore_output.update()
         except Exception:
             valore_output.value = 1
             valore_output.update()
    def incrementa(e):
        # controllo con le eccezione che la conversione vada a buon fine
        try:
            valore=valore_output.value
            valore_output.value=str(int(valore)+1)
            valore_output.update()
        except Exception:
            valore_output.value = 1
            valore_output.update()
    bottone_meno = ft.IconButton(icon=ft.Icons.REMOVE, icon_color="blue", icon_size=24, on_click=decrementa)
    bottone_piu = ft.IconButton(icon=ft.Icons.ADD, icon_color="blue", icon_size=24, on_click=incrementa)
    contatore = ft.Row(controls=[bottone_meno, valore_output, bottone_piu], spacing=0, alignment=ft.MainAxisAlignment.CENTER)

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto, per gestire il contatore dei posti
    def aggiunta_da_schermata(e):
        marca=input_marca.value.strip()
        if not marca:
            alert.show_alert(f"Marca non valida!")
            return
        modello=input_modello.value.strip()
        if not modello:
            alert.show_alert(f"Modello non valido!")
            return
        try:
            anno=int(input_anno.value)
        except Exception:
            alert.show_alert(f"Anno non valido!")
            return
        try:
            posti=int(valore_output.value)
        except Exception:
            alert.show_alert(f"Numero posti non valido!")
            return

        try:
            autonoleggio.aggiungi_automobile(marca, modello, anno, posti)
        except Exception:
            alert.show_alert(f"Errore nell'aggiunta dell'auto!")

        input_marca.value=""
        input_marca.update()
        input_modello.value=""
        input_modello.update()
        input_anno.value=""
        input_anno.update()
        valore_output.value="1"
        valore_output.update()
        aggiorna_lista_auto()
    bottone=ft.ElevatedButton("Aggiungi",  on_click=aggiunta_da_schermata)

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)


    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=1, controls=[input_responsabile, pulsante_conferma_responsabile], alignment=ft.MainAxisAlignment.CENTER ),
        ft.Divider(),

        # Sezione 3
        ft.Text("Aggiungi nuova automobile", size=20),
        ft.Column(controls=[ft.Row(spacing=20, controls=[ input_marca, input_modello, input_anno, contatore, bottone], alignment=ft.MainAxisAlignment.CENTER,)]),

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
