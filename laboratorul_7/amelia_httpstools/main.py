from httptools import *

def main():
        results =[]
        for path in PATHS:
                info = report(path)
                info["path"] = path
                results.append(info)
        ok_pages = [p for p in results if p["status"] == 200]
        ok_pages.sort(key = lambda p: p["seconds"], reverse = True)
        for p in ok_pages:
                print(f"{p['path']} -> {p['status']}, {p['seconds']} secunde")
        print(f"Reusite: {len(ok_pages)} | Esuate: {len(results) - len(ok_pages)}")

if __name__ == "__main__":
	main()
