import math

health = 230
dmg = 0
hsd = 42.61
bsd = 23.00
rpm = 327.27

burst = True #is burst weapon?
rpb = 2 #rounds per burst
burstRPM = 900

precision_instrument = False
enhanced_pi = False
pi_multi = 0.04167 #damage multiplier for Precision Instrument - 1
epi_multi = 0.05 #damage multiplier for enhanced Precision Instrument - 1
if enhanced_pi:
    multi = epi_multi
else:
    multi = pi_multi

if not precision_instrument:
    shots = 0

    while dmg <= health:
        dmg += hsd
        shots += 1

    headshots = shots
    bodyshots = 0

    while dmg > health:
        dmg = dmg + bsd - hsd
        headshots -= 1
        bodyshots += 1

    headshots += 1
    bodyshots -= 1

else:
    shots = 0
    pi_count = 0

    while dmg <= health:
        if pi_count == 0:
            dmg += hsd
        else:
            dmg += hsd * (1 + multi * pi_count)
        shots += 1
        pi_count += 1

    headshots = shots
    bodyshots = 0
    pi_count = 0

    while dmg > health:
        if pi_count == 0:
            dmg = dmg + bsd - hsd
        else:
            dmg = dmg + bsd - (hsd * (1 + multi * pi_count))

        headshots -= 1
        bodyshots += 1
        pi_count += 1

    headshots += 1
    bodyshots -= 1
if not burst:
    ttk = round((shots - 1) / (rpm / 60), 2)
if burst:
    nBurst = math.ceil(shots / rpb) #number of bursts
    leftover = remainder(shots, rpb)
    if leftover == 0:
        ttk = round((((nBurst - 1) * rpb) / rpm + (rpb - 1) / burstRPM) * 60, 3)
    else:
        ttk = round((((nBurst - 1) * rpb) / rpm + (leftover - 1) / burstRPM) * 60, 3)
print(f"It would take {ttk} seconds to kill in {headshots} headshots and {bodyshots} bodyshots")