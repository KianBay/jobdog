import os
import sys
from urllib.parse import urlparse
from jobdog.http_client import create_default_client


def download_listing(url: str) -> None:
    client = create_default_client(timeout=60)

    try:
        response = client.get(url)
        response.raise_for_status()

        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        path = parsed_url.path.strip("/").replace("/", "_")

        os.makedirs("html_samples", exist_ok=True)

        filename = f"{hostname}_{path}.html"
        filepath = os.path.join("html_samples", filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"HTML content saved successfully to {filepath}")
    except Exception as e:
        print(f"Error fetching the job listing: {str(e)}")
    finally:
        client.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_listing_response.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    download_listing(url)
