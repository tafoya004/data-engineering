import aiohttp
import zipfile
import os

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

if not os.path.isdir("downloads"):
    os.makedirs("downloads")

async def main():
    async with aiohttp.ClientSession() as session:
        for uri in download_uris:
            zip_filename = os.path.basename(uri)
            zip_path = os.path.join("downloads", zip_filename)

            try:
                async with session.get(uri) as response:
                    if response.status == 200:
                        with open(zip_path, 'wb') as f:
                            f.write(await response.read())
                        print(f"Downloaded {zip_filename}", flush=True)
                    else:
                        print(f"Failed to download {zip_filename}: HTTP {response.status}", flush=True)
                        continue
            except Exception as e:
                print(f"Error downloading {zip_filename}: {e}", flush=True)
                continue

            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall("downloads")
                print(f"Extracted {zip_filename}", flush=True)
            except Exception as e:
                print(f"Error extracting {zip_filename}: {e}", flush=True)
                continue

            try:
                os.remove(zip_path)
                print(f"Removed {zip_filename}", flush=True)
            except Exception as e:
                print(f"Error removing {zip_filename}: {e}", flush=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
