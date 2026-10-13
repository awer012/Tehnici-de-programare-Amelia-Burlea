import requests
from urllib.parse import urljoin
TIMEOUT = 5

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
	"""Returnează o adresă completă, de exemplu https://example.com/login."""
	return urljoin("https://" + host, path) 

def is_https(url):
	"""Returnează True dacă adresa începe cu https://, altfel False."""
	if url.startswith("http:"):
		return True
	else: return False


def show_response(url):
	"""Trimite un GET la url și afișează statusul și Content-Type."""
	r = requests.get(url, timeout=TIMEOUT)
	content_type = r.headers["Content-Type"]
	print(r.status_code, content_type)
	return r.status_code, content_type

def check_site(url):
	"""Returnează un dicționar cu: status, content_type, length, server."""
	try:
		r = requests.get(url, timeout=5)
	return {
	"status": r.status_code,
	"content_type": r.headers.get("Content-Type", "unknown").split(";")[0],
	"length": len(r.content),
	"server": r.headers.get("Server", "unknown"),
	}
	except requests.exceptions.RequestException as e:
		return {"status": None, "error": str(e)}
	except Exception as e:
		return {"status": None, "error": str(e)}



def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    for url in SITES:
        results.append(check_site(url))

    ok = []
    for r in results:
        if r["status"] == 200:
            ok.append(r)

    ok.sort(key=get_length, reverse=True)

    for r in ok:
        print(f'{r["url"]} -> {r["status"]}, {r["length"]} octeți')

    print(f"Reușite: {len(ok)} | Eșuate: {len(results) - len(ok)}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        return {"status": None, "error": type(e).__name__}

    present = []
    missing = []
    for name in SECURITY_HEADERS:
        if name in r.headers:
            present.append(name)
        else:
            missing.append(name)

    score = len(present) * 100 // len(SECURITY_HEADERS)
    return {"present": present, "missing": missing, "score": score}


def retry_check(url, attempts=3):
	"""Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
	status = None
	error = None
	made = 0

	for _ in range(attempts):
		made += 1
		try:
        		r = requests.get(url, timeout=TIMEOUT)
		except requests.exceptions.RequestException as e:
			error = type(e).__name__
			continue

		status = r.status_code
		if status < 500:
			break

	result = {"status": status, "attempts": made}
	if status is None:
		result["error"] = error
		return result
