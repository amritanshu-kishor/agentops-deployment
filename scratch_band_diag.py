"""Fetch Band swagger page with auth and extract JSON spec if present."""
import httpx
import asyncio

BASE_URL = "https://app.band.ai/api/v1"
API_KEY = "band_a_1781418110_A8Tg0aJ4vNcT-Uh_TsBaLSObt2b4IBh4"

async def main():
    hdrs = {"Authorization": f"Bearer {API_KEY}"}
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
        # Try swagger with auth
        r = await c.get(f"{BASE_URL}/swagger", headers=hdrs)
        print(f"Swagger with Bearer: {r.status_code}, {len(r.text)} bytes")
        with open("band_swagger_auth.html", "w", encoding="utf-8") as f:
            f.write(r.text)
        print("Saved to band_swagger_auth.html")
        
        # Try to find open_api spec linked from swagger page
        if "swagger-initializer.js" in r.text or "url:" in r.text:
            # Extract the spec URL
            import re
            urls = re.findall(r'url["\s:]*["\']([^"\']+)["\']', r.text)
            print(f"Found spec URLs: {urls}")
            for url in urls:
                if url.startswith("/"):
                    url = "https://app.band.ai" + url
                if "json" in url or "yaml" in url or "spec" in url:
                    try:
                        r2 = await c.get(url, headers=hdrs)
                        print(f"  Spec {url}: {r2.status_code} ({len(r2.text)} bytes)")
                        if r2.status_code == 200:
                            with open("band_openapi_spec.json", "w", encoding="utf-8") as f:
                                f.write(r2.text)
                            print("  Saved spec!")
                    except Exception as e:
                        print(f"  Error: {e}")

asyncio.run(main())
