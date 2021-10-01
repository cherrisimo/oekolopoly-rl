# Overview

### OekolopolyBox
* (OekoBoxWrapper)– `Action Wrapper`, `Box`

Die Aktion wird zunächst vom Typ Box generiert. Dieser Typ stellt einen kontinuerlichen Raum dar und der Aktionsraum kann Werte von -1 bis 1 umfassen. Die Grenzwerte für jeden Aktionsteil sind in np.arrays gespeichert und an den Konstruktor beim Anlegen des Aktionsraums übergeben. Die Funktion distribute1 () korriegiert die Vergabe der Aktionspunkte und somit das Entstehen von illegalen Zügen (z. B. mehr Aktionspunkte verteilen als es verfügbar gibt) wird vermieden. Die Aktion wird endlich diskretisiert und an die originale Ökolopoly Umgebung übergeben, was vor jedem Aufruf der step()-Funktion geschieht. Die distribute2 () Funktion folgt derselben Logik mit dem einzigen Unterschied, dass der Agent angeben kann, welcher Teil der verfügbaren Aktionspunkte er benutzen will und auf diese Weise sparen. Distribute2 () wird jedoch noch nicht beim Experimenten eingesetzt. 

### **OekolopolySimple**
* (OekoEnvSimpleWrapper) – `Action Wrapper`, `MultiDiscrete`

Der Wrapper reduziert signifikant den Aktionsraum. Alle erlaubte Aktionen werden in einer Liste gespeichert. Der Agent wählt ein Element aus der Liste (bspw. entspricht das 75. dem String '210001') aus. In einer Schleife werden die zu vergebenden Punkte ausgerechnet. Dennoch wird geprüft, ob es noch Punkte zu verteilen sind, da es beim Runden der Zahlen floor () benutzt wird. Die übrige Punkte sind an den Bereichen verteilt, die im String mit keinem 0 belegt sind. Das letzte Zeichen 1 vom String '210001'  weist darauf hin, dass die Punkte von Produktion abgezogen werden müssen. Seien die zulässigen Grenzwerte jedes Bereichs überschritten, werden sie korrigiert. Am Ende wird die Aktion zurück zum Typ MultiDiscrete konvertiert und an die originale Umgebung übergeben.

### **OekolopolySimpleObsBox** (OekoSimpleObsWrapper)– `Observation Wrapper`, `MultiDiscrete`

Dieser Wrapper übersetzt den Zustandsraum in niedrig-mittel-hoch und damit ergeben sich insgesamt 6561 Zustände. Jeder Zustand soll Werte 0 bis 2 umfangen. Anschließend verfügt der Agent über den umgewandelten Zustandsraum.

### **OekolopolyBoxReward** (OekoRewardWrapper) – `Reward Wrapper`

Der Wrapper fügt einen Hilfsreward zum Environment hinzu.

## Usage
Die Datei `wrappers.py` enthält die Wrappers für die Umgebung Ökolopoly und die Environments von RL Baselines Zoo3. Diese kann direkt anstelle der originalen im Ordner `utils` gesetzt werden. 
