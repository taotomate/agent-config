# Everything HTTP Server API Reference

## Endpoint

```
GET http://127.0.0.1/?search=<query>
```

Configurable in Everything Options → HTTP Server. Default port: 80.

## Auth

If enabled in Everything Options:
```python
import base64
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {"Authorization": f"Basic {credentials}"}
```

## Response Format (HTML)

```html
<p class="numresults">5 results</p>
<table>
  <tr class="trdata1">
    <td class="folder"><a href="/path">name</a></td>
    <td class="pathdata"><a href="/dir">C:\dir</a></td>
    <td class="sizedata">1.2 MB</td>
    <td class="modifieddata">6/24/2026 2:00 PM</td>
  </tr>
  <tr class="trdata2">
    <td class="file"><a href="/path">file.py</a></td>
    ...
  </tr>
</table>
```

## Full Working Script

```python
import urllib.request, base64, urllib.parse, re

def search_everything(pattern, username="user", password="", port=80):
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    headers = {"Authorization": f"Basic {credentials}"}
    url = f"http://127.0.0.1:{port}/?search={urllib.parse.quote(pattern)}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
    
    # Count
    count_match = re.search(r'<p class="numresults">(\d+) results</p>', html)
    count = int(count_match.group(1)) if count_match else 0
    
    # Results
    results = []
    for row in re.finditer(r'<tr class="trdata\d">(.*?)</tr>', html, re.DOTALL):
        name = re.search(r'<td class="(?:folder|file)">.*?>([^<]+)<', row.group(1))
        path = re.search(r'<td class="pathdata">.*?>([^<]+)<', row.group(1))
        if name and path:
            results.append({"name": name.group(1), "path": path.group(1)})
    
    return count, results
```

## Error Handling

| HTTP Code | Meaning | Action |
|---|---|---|
| 200 | OK | Parse HTML |
| 401 | Unauthorized | Ask user for password, or try without auth |
| Connection refused | HTTP server not running | Enable in Everything Options, or fall back to `find` |
