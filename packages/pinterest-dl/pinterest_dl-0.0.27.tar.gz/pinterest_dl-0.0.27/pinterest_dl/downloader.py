import concurrent.futures
from pathlib import Path
from typing import Literal

import requests
from tqdm import tqdm


def fetch(url: str, response_format: Literal["json", "text"] = "text"):
    if isinstance(url, str):
        req = requests.get(url)
        req.raise_for_status()
        if response_format == "json":
            return req.json()
        elif response_format == "text":
            return req.text
    else:
        print("URL must be a string.")


def download(url: str, output_dir, chunk_size=2048):
    if isinstance(url, str):
        req = requests.get(url)
        req.raise_for_status()

        filename = Path(url).name
        outfile = Path.joinpath(Path(output_dir), filename)
        # create directory if not exist
        outfile.parent.mkdir(parents=True, exist_ok=True)
        with open(outfile, "wb") as payload:
            for chunk in req.iter_content(chunk_size):
                payload.write(chunk)
        return outfile
    else:
        print("URL must be a string.")


def download_with_fallback(url: str, output_dir, fallback_url, chunk_size=2048):
    try:
        return download(url, output_dir, chunk_size)
    except requests.exceptions.HTTPError:
        return download(fallback_url, output_dir, chunk_size)


def download_concurrent(urls: list, output_dir, chunk_size=2048, verbose=False):
    results = [None] * len(urls)  # Initialize a list to hold the results in order
    with concurrent.futures.ThreadPoolExecutor() as executor, tqdm(
        total=len(urls), desc="Downloading"
    ) as pbar:
        futures = {
            executor.submit(download, url, output_dir, chunk_size): idx
            for idx, url in enumerate(urls)
        }
        for future in concurrent.futures.as_completed(futures):
            result_index = futures[future]  # Get the original index for the result
            outfile = future.result()
            results[result_index] = outfile  # Place the result in the corresponding position
            pbar.update(1)
    return results


def download_concurrent_with_fallback(
    urls: list, output_dir, fallback_urls, chunk_size=2048, verbose=False
):
    results = [None] * len(urls)  # Initialize a list to hold the results in order
    with concurrent.futures.ThreadPoolExecutor() as executor, tqdm(
        total=len(urls), desc="Downloading"
    ) as pbar:
        futures = {
            executor.submit(download_with_fallback, url, output_dir, fallback_url, chunk_size): idx
            for idx, (url, fallback_url) in enumerate(zip(urls, fallback_urls))
        }
        for future in concurrent.futures.as_completed(futures):
            result_index = futures[future]  # Get the original index for the result
            outfile = future.result()
            results[result_index] = outfile  # Place the result in the corresponding position
            pbar.update(1)
    return results
