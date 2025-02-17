weapons = {
    autoRifle,
    bow,
    handCannon,
    pulseRifle,
    scoutRifle,
    sidearm,
    submachineGun
}

autoRifle = {
    adaptiveAR,
    highImpactAR,
    lightweightAR,
    precisionAR,
    rapidFireAR,
    supportAR,
}

bow = {
    lightweightB,
    precisionB,
}

handCannon = {
    adaptiveHC,
    agressiveHC,
    heavyBurstHC,
    lightweightHC,
    precisionHC
}

pulseRifle = {
    adaptivePR,
    aggressiveBurstPR,
    BxR,
    heavyBurstPR,
    highImpactPR,
    lightweightPR,
    rapidFirePR
}

scoutRifle = {
    aggressiveSR,
    highImpactSR,
    lightweightSR,
    precisionSR,
    rapidFireSR
}

sidearm = {
    adaptiveS,
    adaptiveBurstS,
    heavyBurstS,
    lightweightS,
    precisionS,
    rapidFireS
}

submachineGun = {
    adaptiveSG,
    aggressiveSG,
    lightweightSG,
    precisionSG
}

class weapon():
    def __init__(self, rpm, hsd, bsd, burst, burstRPM = 0):
       self.rpm = rpm
       self.hsd = hsd
       self.bsd = bsd
       self.burst = burst
       self.burstRPM = burstRPM