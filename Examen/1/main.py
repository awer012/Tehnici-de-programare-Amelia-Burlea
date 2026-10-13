from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check
from checker import SITES

print(build_url("example.com", "login"))
print(build_url("example.com", "/login"))
print(is_https("https://example.com"))
print(is_https("http://example.com"))

show_response(SITES[0])
show_response(SITES[9])

print(check_site(SITES[0]))
print(check_site(SITES[9]))

scan_sites()

print(check_headers(SITES[10]))
print(check_headers(SITES[9]))

print(retry_check(SITES[6]))
print(retry_check(SITES[7]))
