
# Icon für sehr gut Stickstoffdioxid (NO₂):	13 µg/m³
# Icon für keine Daten Feinstaub (PM₁₀):	-
# Icon für sehr gut Ozon (O₃):	57 µg/m³

# Die Geruchsschwelle für Ammoniak beträgt beim Menschen 1 - 5 mg/m³ (= 0,16-0,84 ppm). Hohe Konzentrationen um 100 ppm werden als so unangenehm empfunden, dass panikartige Reaktionen die Regel sind. Als Arbeitsplatzgrenzwert (AGW) gilt 14 mg/m³ (= 20 ppm).

# Bezeichnung	Grenzwerte Ammoniak
# Empfehlung Umweltbundesamt für Außenluft	< 1 ppm
# Grenzwert gemäß Tierschutz-Nutztierhaltungsverordnung (TierSchNutztV)	20 ppm
# Arbeitsplatzgrenzwert (AGW)	20 ppm
# ‍
def mapRange(vmin, vmax, steps):

    step = (vmax - vmin) / (steps - 1) # steps - 1 because vmin is fixed the first value
    vals = [0, vmin]
    for i in range(1023): # begin with 0
        vmin += step
        vals.append(vmin)

    print(len(vals), min(vals), max(vals))
    return vals
    
 # Mappingliste für CO erstellen Sensor-Range 1-100ppm
coMap = mapRange(vmin=1, vmax=100, steps=1024)

   # Mappingliste für NO2 erstellen Sensor-Range 0.05-10ppm
no2Map = mapRange(vmin=0.05, vmax=10, steps=1024)

# Mappingliste für NH3 erstellen Sensor-Range 1-500ppm
nh3Map = mapRange(vmin=1, vmax=500, steps=1024)
