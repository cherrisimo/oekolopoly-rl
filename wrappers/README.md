# Overview

### OekolopolyBox
*Klassenname: OekoBoxWrapper, `Action Wrapper`, `Box`*

Die Aktion wird vom Typ Box erzeugt. Dieser Typ stellt einen kontinuerlichen Raum dar und der Aktionsraum kann Werte von -1 bis 1 umfassen. Die Grenzwerte für jeden Aktionsteil sind in np.arrays gespeichert und an den Konstruktor beim Anlegen des Aktionsraums übergeben. Die Gesamtsumme der Aktion muss 1 nicht überschreiten. Es wird gemäß der vom Agenten gegebenen Aktion überprüft, ob Punkte für Produktion abgezogen werden sollen. Das Ergebnis wird in der Variable `reduce_produktion` gespeichert. Die Funktion `distribute1 ()` korrigiert die Vergabe der Aktionspunkte und somit das Entstehen von illegalen Zügen (z. B. mehr Aktionspunkte verteilen als es verfügbar gibt) wird vermieden. Die `distribute2 ()` Funktion folgt derselben Logik mit dem einzigen Unterschied, dass der Agent angeben kann, welcher Teil der verfügbaren Aktionspunkte er benutzen will und auf diese Weise sparen. `Distribute2 ()` wird jedoch noch nicht beim Experimenten eingesetzt. Die Aktion wird endlich diskretisiert und an die originale Ökolopoly Umgebung übergeben, was vor jedem Aufruf der `step()`-Funktion geschieht. 

### **OekolopolySimple**
*Klassenname: OekoEnvSimpleWrapper – `Action Wrapper`, `MultiDiscrete`*

Der Wrapper reduziert signifikant den Aktionsraum mit insgesamt 88 Aktionen verfügbar. Alle erlaubte Aktionen werden in einer Liste gespeichert. Der Agent wählt ein Element aus der Liste (bspw. entspricht das 75. dem String '210001') aus. In einer Schleife werden die zu vergebenden Punkte ausgerechnet. Dennoch wird geprüft, ob es noch Punkte zu verteilen sind, da es beim Runden der Zahlen floor () benutzt wird. Diese Funktion wandelt die gegebene Float-Zahl in die nächstliegende kleinere ganze Zahl um, was Punktverlust verursachen kann. Damit ist aber gesichert, dass es nie mehr Punkte verteilt werden, als es verfügbar gibt. Weiterhin sind die übrige Punkte utner diese Bereichen verteilt, die in der Zeichenkette mit keinem 0 belegt sind. Das letzte Zeichen 1 vom String '210001'  weist darauf hin, dass Punkte von Produktion abgezogen werden müssen. Sind demnächst die zulässigen Grenzwerte eines Bereichs überschritten, werden sie korrigiert. Am Ende wird die Aktion zurück zum Typ MultiDiscrete konvertiert und an die originale Umgebung übergeben.

### **OekolopolySimpleObsBox** 
*Klassenname: OekoSimpleObsWrapper – `Observation Wrapper`, `MultiDiscrete`*

Dieser Wrapper übersetzt den Zustandsraum in niedrig-mittel-hoch und damit ergeben sich insgesamt 6561 Zustände. Jeder Zustand soll Werte von 0 bis 2 umfangen. Um berechnet zu werden, welcher Wert der bestimmte Bereich annehmen soll, wird seiner aktuelle Wert durch den maximalen geteilt und mit 3 multipliziert. Zum Beispiel:
 ```python 
 obs[0] = floor ( 1 / 29 * 3)
 ```
 Sanierung ist der erste Bereich und wegen ihrem aktuellen Werte ist der niegrigste Klasse gleich 0. Auf deise Weise werden alle Bereiche aktualisiert. 
 Zusätzlich kann die Anzahl der Observations und der Klassen, nach deren sich jedes einzelne Observation teilt, durch die Variablen `obs_count` und `obs_split` eingestellt werden. Anschließend verfügt der Agent über den umgewandelten Zustandsraum.

### **OekolopolyBoxReward** 
*Klassenname: OekoRewardWrapper – `Reward Wrapper`*

Der Wrapper fügt einen Hilfsreward zum Environment hinzu. Die Belohnung hat zum Ziel, die Bereiche Produktion und Belohnung in mittleren Werten zu halten.

## Usage
Die Datei `wrappers.py` enthält die Wrappers für die Umgebung Ökolopoly und die Environments von RL Baselines Zoo3. Sie kann direkt anstelle der originalen im Ordner `utils` gesetzt werden. Instruktionen wie Wrappers zur Umgebung hinzugefügt werden können, sind im Haupt-[README](https://github.com/cherrisimo/oekolopoly-rl#usage) unter Punkt 2a enthalten.
