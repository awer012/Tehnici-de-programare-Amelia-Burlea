from httptools import *


print("Apel search: ",search({"q": "python", "page": "2"}) )
print("Apel search_url: ", search_url({"q": "python", "page":"2"}))
print("Apel fetch_with_agent: ", fetch_with_agent("MyBot/1.0"))
print("Apel default_agent: ", default_agent())
print("Apel post_json: ", post_json({"name": "Ana", "age": 19,"tags": ["a", "b"]}))
print("Apel post_form: ", post_form({"user": "ana", "city":"Bălți"}))
print("Apel describe_status(200): ", describe_status(200))
print("Apel describe_status(404): ", describe_status(404))
print("Apel describe_status(503): ", describe_status(503))
print("Apel is_ok(204): ", is_ok(204))
print("Apel is_ok(500): ", is_ok(500))
print("Apel count_redirects(3): ", count_redirects(3))
print("Apel final_url(2): ", final_url(2))
print("Apel first_hop(3): ", first_hop(3))
print("Apel cookie_demo: ", cookie_demo("theme", "dark"))
print("Apel no_session_demo: ", no_session_demo("theme", "dark"))
print("Apel report('/get'): ", report("/get"))
print("Apel report('/redirect/2'): ", report("/get"))
print("Apel report('/delay/1'): ", report("/delay/1"))
print("Apel check_login: ", check_login("admin", "secret"))

