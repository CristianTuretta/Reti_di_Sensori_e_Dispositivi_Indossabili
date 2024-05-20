# Linux
Per prima cosa installare le dipendenze necessarie per il corretto funzionamento del progetto.
Si raccomanda che per prima cosa bisogna installare le dipendenze della libreria `bluepy` che viene
utilizzata per la comunicazione con i dispositivi BLE.
```bash
sudo apt-get install python-pip libglib2.0-dev
```

Potreste avere bisogno di installare anche:
```bash
apt-get update && apt-get install -y bluez dbus sudo libglib2.0-dev libcap2-bin
```

Attivare il virtualenv del progetto.
```bash
source <VENV-NAME>/bin/activate
```

Successivamente installare le dipendenze del progetto.
```bash
pip install -r requirements_linux.txt
```
La libreria `bluepy` richiede i permessi di root per poter essere eseguita, quindi per essere facilitati.
```bash
 sudo setcap cap_net_raw+e  <PATH>/bluepy-helper
 sudo setcap cap_net_admin+eip  <PATH>/bluepy-helper
```
dove `<PATH>` è il percorso dove si trova `bluepy-helper`. Per trovare il percorso esatto si può utilizzare lo script 
seguente:
```bash
python utility/find_helper.py
```
A questo punto si può eseguire il codice, ad esempio andando nella cartella `Lab_05/Linux/` ed eseguendo il file 
`lab_05_main.py`.

# MacOS
Per prima cosa installare le dipendenze necessarie per il corretto funzionamento del progetto.
Per prima aprire il terminale ed attivare il virtualenv del progetto.
```bash
source <VENV-NAME>/bin/activate
```
a questo punto installare le dipendenze del progetto:
```bash
pip install -r requirements_macOS.txt
```

Successivamente si può eseguire il codice, ad esempio andando nella cartella `Lab_05/MacOS/` ed eseguendo il file.
