from arsenal.privesc.enum import citeste_linii, nume, GTFO

def cai(fisier):
	return set(citeste_linii(fisier))


baza = cai("arsenal/privesc/start/baza_suid.txt")
acum = cai("arsenal/privesc/start/suid.txt")
print("baza:", len(baza), " acum:", len(acum))


noi = acum - baza
print(len(noi), "SUID noi fata de sistemul curat")
for c in sorted(noi):
    print(" ", c)

risc = {}
for c in noi:
	if nume(c) in GTFO:
		risc[nume(c)] = "mare"
	else:
		risc[nume(c)] = "normal"

periculoase = []
for c in sorted(noi):
	if nume(c) in GTFO:
		periculoase.append(c)

print("periculoase NOI:", periculoase)
