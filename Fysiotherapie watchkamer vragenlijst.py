import tkinter as tk
import matplotlib.pyplot as plt
from tkinter.font import Font

# Lijst voor pijnlijke activiteiten
pijnlijke_activiteiten = []

# Functie om pijnlijke activiteiten toe te voegen
def vul_pijnlijke_activiteiten_in():
    # ... (vorige code blijft hetzelfde)

    # Update de grafiek
    update_grafiek()

# Functie om de grafiek bij te werken
def update_grafiek():
    activiteiten = [activiteit[0] for activiteit in pijnlijke_activiteiten]
    pijnscores = [activiteit[1] for activiteit in pijnlijke_activiteiten]

    plt.figure(figsize=(8, 6))
    plt.plot(activiteiten, pijnscores, marker='o')
    plt.xlabel('Activiteit', fontsize=20)  # Vergrote lettergrootte
    plt.ylabel('Pijnscore', fontsize=20)  # Vergrote lettergrootte
    plt.title('Verloop van pijnscores', fontsize=32)  # Vergrote lettergrootte
    plt.xticks(rotation=45, fontsize=24)
    plt.yticks(fontsize=24)
    plt.tight_layout()
    plt.show()

# ... (overige code blijft hetzelfde)

# Lijst om de ingevulde gegevens van de patiënt op te slaan
pijnlijke_activiteiten = []

# Functie om pijnlijke activiteiten in te vullen
def vul_pijnlijke_activiteiten_in():
    activiteit = entry_activiteit.get()
    if activiteit != "":
        pijn_score = scale_pijn.get()
        type_pijn = var_type_pijn.get()
        ontstaan_klachten = entry_ontstaan_klachten.get()
        locatie_klachten = entry_locatie_klachten.get()
        vermindering_klachten = entry_vermindering_klachten.get()
        verergering_klachten = entry_verergering_klachten.get()
        duur_klachten = entry_duur_klachten.get()
        uitstralende_klachten = var_uitstralende_klachten.get()
        pijnlijke_activiteiten.append(
            (activiteit, pijn_score, type_pijn, ontstaan_klachten, locatie_klachten, vermindering_klachten,
             verergering_klachten, duur_klachten, uitstralende_klachten))
        # Wis de ingevulde waarden na het toevoegen
        entry_activiteit.delete(0, tk.END)
        scale_pijn.set(0)
        var_type_pijn.set("Zeurende pijn")
        entry_ontstaan_klachten.delete(0, tk.END)
        entry_locatie_klachten.delete(0, tk.END)
        entry_vermindering_klachten.delete(0, tk.END)
        entry_verergering_klachten.delete(0, tk.END)
        entry_duur_klachten.delete(0, tk.END)
        var_uitstralende_klachten.set(0)

# Functie om een samenvatting te genereren en conclusies te trekken
def genereer_samenvatting():
    if not pijnlijke_activiteiten:
        label_samenvatting["text"] = "Voeg pijnlijke activiteiten toe om een samenvatting te genereren."
        return

    # Sorteer de activiteiten op basis van pijnscore (hoogste eerst)
    pijnlijke_activiteiten.sort(key=lambda x: x[1], reverse=True)

    # Krijg de meest en minst pijnlijke activiteit
    meest_pijnlijke_activiteit = pijnlijke_activiteiten[0]
    minst_pijnlijke_activiteit = pijnlijke_activiteiten[-1]

    # Genereer de samenvatting
    samenvatting = f"Tijdens de activiteit '{meest_pijnlijke_activiteit[0]}' ervaart u de meeste pijn.\n"
    samenvatting += f"Deze activiteit veroorzaakt {meest_pijnlijke_activiteit[2]} pijn van niveau {meest_pijnlijke_activiteit[1]}/10.\n"
    samenvatting += f"De klachten zijn ontstaan {meest_pijnlijke_activiteit[3]} en bevinden zich in {meest_pijnlijke_activiteit[4]}.\n"
    samenvatting += f"De pijnklachten verminderen met {meest_pijnlijke_activiteit[5]} en verergeren met {meest_pijnlijke_activiteit[6]}.\n"
    samenvatting += f"De klachten duren al {meest_pijnlijke_activiteit[7]}.\n"
    if meest_pijnlijke_activiteit[8] == 1:
        samenvatting += "U ervaart ook uitstralende klachten.\n"

    label_samenvatting["text"] = samenvatting


# Creëer het hoofdvenster
root = tk.Tk()
root.title("Pijnregistratie")

# Maak een aangepast lettertype met vergrote grootte
font = Font(size=20)

# Invoer van pijnlijke activiteiten
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label_activiteit = tk.Label(frame_input, text="Vul in welke activiteit(en) het meeste pijn doet/doen:", font=font)
label_activiteit.grid(row=0, column=0, padx=10)
entry_activiteit = tk.Entry(frame_input, width=20, font=font)
entry_activiteit.grid(row=0, column=1, padx=10)

label_pijn = tk.Label(frame_input, text="Pijnscore (0 = geen pijn, 10 = verschikkelijk veel pijn):", font=font)
label_pijn.grid(row=1, column=0, padx=10)
scale_pijn = tk.Scale(frame_input, from_=0, to=10, orient=tk.HORIZONTAL, length=200, font=font)
scale_pijn.grid(row=1, column=1, padx=10)

label_type_pijn = tk.Label(frame_input, text="Type pijn:", font=font)
label_type_pijn.grid(row=2, column=0, padx=10)
var_type_pijn = tk.StringVar(value="Zeurende pijn")
radio_zeurende_pijn = tk.Radiobutton(frame_input, text="Zeurende pijn", variable=var_type_pijn, value="Zeurende pijn", font=font)
radio_zeurende_pijn.grid(row=2, column=1, padx=10, sticky="w")
radio_stekende_pijn = tk.Radiobutton(frame_input, text="Stekende pijn", variable=var_type_pijn, value="Stekende pijn", font=font)
radio_stekende_pijn.grid(row=3, column=1, padx=10, sticky="w")
radio_scherpe_pijn = tk.Radiobutton(frame_input, text="Scherpe pijn", variable=var_type_pijn, value="Scherpe pijn", font=font)
radio_scherpe_pijn.grid(row=4, column=1, padx=10, sticky="w")

label_ontstaan_klachten = tk.Label(frame_input, text="Ontstaan klachten:", font=font)
label_ontstaan_klachten.grid(row=5, column=0, padx=10)
entry_ontstaan_klachten = tk.Entry(frame_input, width=20, font=font)
entry_ontstaan_klachten.grid(row=5, column=1, padx=10)

label_locatie_klachten = tk.Label(frame_input, text="Locatie klachten:", font=font)
label_locatie_klachten.grid(row=6, column=0, padx=10)
entry_locatie_klachten = tk.Entry(frame_input, width=20, font=font)
entry_locatie_klachten.grid(row=6, column=1, padx=10)

label_vermindering_klachten = tk.Label(frame_input, text="Vermindering klachten:", font=font)
label_vermindering_klachten.grid(row=7, column=0, padx=10)
entry_vermindering_klachten = tk.Entry(frame_input, width=20, font=font)
entry_vermindering_klachten.grid(row=7, column=1, padx=10)

label_verergering_klachten = tk.Label(frame_input, text="Verergering klachten:", font=font)
label_verergering_klachten.grid(row=8, column=0, padx=10)
entry_verergering_klachten = tk.Entry(frame_input, width=20, font=font)
entry_verergering_klachten.grid(row=8, column=1, padx=10)

label_duur_klachten = tk.Label(frame_input, text="Duur klachten:", font=font)
label_duur_klachten.grid(row=9, column=0, padx=10)
entry_duur_klachten = tk.Entry(frame_input, width=20, font=font)
entry_duur_klachten.grid(row=9, column=1, padx=10)

label_uitstralende_klachten = tk.Label(frame_input, text="Uitstralende klachten:", font=font)
label_uitstralende_klachten.grid(row=10, column=0, padx=10)
var_uitstralende_klachten = tk.IntVar(value=0)
check_uitstralende_klachten = tk.Checkbutton(frame_input, variable=var_uitstralende_klachten, font=font)
check_uitstralende_klachten.grid(row=10, column=1, padx=10, sticky="w")

button_toevoegen = tk.Button(root, text="Toevoegen", command=vul_pijnlijke_activiteiten_in, font=font)
button_toevoegen.pack(pady=5)

# Samenvatting van pijnlijke activiteiten
frame_samenvatting = tk.Frame(root)
frame_samenvatting.pack(pady=10)

label_samenvatting = tk.Label(frame_samenvatting, text="Voeg pijnlijke activiteiten toe om een samenvatting te genereren.", font=font)
label_samenvatting.pack()

button_samenvatting = tk.Button(root, text="Genereer samenvatting", command=genereer_samenvatting, font=font)
button_samenvatting.pack(pady=5)

# Functie om de conclusie te kopiëren
def kopieer_conclusie():
    samenvatting = label_samenvatting["text"]
    root.clipboard_clear()
    root.clipboard_append(samenvatting)

button_kopieer_conclusie = tk.Button(root, text="Kopieer conclusie", command=kopieer_conclusie, font=font)
button_kopieer_conclusie.pack(pady=5)

import smtplib

# Functie om samenvatting naar e-mail te sturen
def stuur_naar_mail():
    # E-mailinstellingen (vervang met je eigen gegevens)
    smtp_server = "smtp.example.com"
    smtp_port = 587
    sender_email = "your_email@example.com"
    receiver_email = "DavidvDommelen@hotmail.com"
    password = "Coolbed123"

    # Samenvatting ophalen
    samenvatting = label_samenvatting["text"]

    # Verbind met de SMTP-server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, password)

    # Stuur e-mail
    subject = "Pijnregistratie Samenvatting"
    message = f"Subject: {subject}\n\n{samenvatting}"
    server.sendmail(sender_email, receiver_email, message)

    # Afsluiten van de SMTP-server
    server.quit()

button_mail = tk.Button(root, text="Stuur naar mail", command=stuur_naar_mail, font=font)
button_mail.pack(pady=5)

# Functie om het formulier te verversen
def ververs_formulier():
    # Wis de ingevulde waarden
    entry_activiteit.delete(0, tk.END)
    scale_pijn.set(0)
    var_type_pijn.set("Zeurende pijn")
    entry_ontstaan_klachten.delete(0, tk.END)
    entry_locatie_klachten.delete(0, tk.END)
    entry_vermindering_klachten.delete(0, tk.END)
    entry_verergering_klachten.delete(0, tk.END)
    entry_duur_klachten.delete(0, tk.END)
    var_uitstralende_klachten.set(0)
    # Wis de samenvatting
    label_samenvatting["text"] = "Voeg pijnlijke activiteiten toe om een samenvatting te genereren."

button_ververs = tk.Button(root, text="Ververs", command=ververs_formulier, font=font)
button_ververs.pack(pady=5)


# Start de GUI
root.mainloop()
