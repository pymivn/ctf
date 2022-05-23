# How The Columns Have Turned

```
score: 300
solved: xx/xx
difficulty: easy
tags: crypto, column cipher
```

## Problem
[code](./columns.py)
[secret](./columns_secret.txt)
The code get the secret, transpose it (rows to columns), then move them around based on the key digits.

## Got the flag
As we know the key, solving this by reversing the flow:

```py
def unflatten(ct):
    r = []
    for i in range(0, len(ct), len(ct)//15):
        r.append(ct[i:i+len(ct)//15])
    return r
def decrypt(ct, key):
    ct = unflatten(ct)
    ct = [i[::-1] for i in ct]
    pt = []
    derived_key = deriveKey(key)
    width = len(key)
    for i in range(width):
        pt.append(ct[derived_key[i]-1])
    return transpose(pt)

key = "729513912306026"
for message in SUPER_SECRET_MESSAGES:
    pt = (decrypt(message, key))
    for line in pt:
        print("".join(line), end="")
```

Output
```
THELOCATIONOFTHECONVOYDANTEISDETERMINEDTOBEONTHETHIRDPLANETAFTERVINYRYOUCANUSELIGHTSPEEDAFTERTHEDELIVERYSTHECARGOISSAFEWENEEDTOMOVEFASTCAUSETHERADARSAREPICKINGUPSUSPICIOUSACTIVITYAROUNDTHETRAJECTORYOFTHEPLANETABECAREFULSKOLIWHENYOUARRIVEATTHEPALACEOFSCIONSAYTHECODEPHRASETOGETINHTBTHELCGISVULNERABLEWENEEDTOCHANGEITDONTFORGETTOCHANGETHEDARKFUELOFTHESPACESHIPWEDONTWANTANYUNPLEASANTSURPRISESTOHAPPENTHISSERIOUSMISSIONPOPOIFYOUMESSUPAGAINILLSENDYOUTOTHEANDROIDGRAVEYARDTOSUFFERFROMTHECONSTANTTERMINATIONOFYOURKINDAFINALWARNING
```

We got the flag `HTB{THELCGISVULNERABLEWENEEDTOCHANGEIT}`
