import argparse, json, os

GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}

 
def citeste_linii(cale):
	with open(cale, encoding="utf-8") as f:
		linii = [ln.strip() for ln in f]
	return [ln for ln in linii if ln  and not ln.startswith('#')]

def nume(cale):
	return cale.rsplit("/", 1)[-1] 

def suid_constatari(cale):
	rez=[]
	cai = sorted(set(citeste_linii(cale)))
	for c in cai:
		if nume(c) in GTFO:
			risc = "mare"
		else:
			risc = "normal"
		fisa = {"cale": c, "nume": nume(c), "risc":risc}
		rez.append(fisa)
	return rez

def sudo_constatari(cale):
	out=[]
	for ln in citeste_linii(cale):
		user, drept = ln.split(" : ", 1)
		if "NOPASSWD" in drept:
			risc = "mare"
		else:
			risc = "normal"
		fisa = {"user": user.strip(), "drept": drept.strip(), "risc": risc}
		out.append(fisa)
	return out

def cron_constatari(cale):
	rez = []
	for ln in citeste_linii(cale):
		campuri = ln.split()
		user = campuri[5]
		comanda = " ".join(campuri[6:])
		fisa = {"user": user, "comanda": comanda}
		rez.append(fisa)
	return rez

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }


def main():
	p = argparse.ArgumentParser()
	p.add_argument("capturi")
	p.add_argument("--json", action="store_true")
	a = p.parse_args()
	raport = enumereaza(a.capturi)
	if a.json:
		print(json.dumps(raport, indent=2, ensure_ascii=False)); 
		return

	for categorie, lista in raport.items():
		mari = [c for c in lista if c.get("risc") == "mare"]
		print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

	useri_sudo = set()
	for c in raport["sudo"]:
		useri_sudo.add(c["user"])

	useri_cron = set()
	for c in raport["cron"]:
		useri_cron.add(c["user"]) 

	useri = useri_sudo | useri_cron
	print("Utilizatori implicati:", ", ".join(sorted(useri)))

	with open("enum.json", "w", encoding="utf-8") as f:
		json.dump(raport, f, indent=2, ensure_ascii=False)
		print("Raport salvat in enum.json")
 


if __name__ == "__main__":
    main()



