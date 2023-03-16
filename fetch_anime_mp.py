import os
import requests
import subprocess
import multiprocessing

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ja-JP,ja;q=0.9,zh-TW;q=0.8,zh;q=0.7,en-DE;q=0.6,en;q=0.5,de-DE;q=0.4,de;q=0.3,en-US;q=0.2',
    'origin': 'https://v.myself-bbs.com',
    'referer': 'https://v.myself-bbs.com/',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

def download_and_convert(file_name):
    url = f"https://vpx08.myself-bbs.com/vpx/43563/{file_name}" # Please change 43563 to your target anime
    print(f"Downloading {url}")
    r = requests.get(url, headers=headers, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    output_file = file_name.replace(".ts", ".mp4")
    command = f"ffmpeg -i {file_name} -c copy {output_file}"
    subprocess.call(command, shell=True)
    os.remove(file_name)

if __name__ == "__main__":
    # Create a list of file names to download and convert
    file_names = []
    for i in range(1, 14):
        for j in range(0, 4):
            file_name = f"{str(i).zfill(3)}_v01/720p_{str(j).zfill(3)}.ts"
            file_names.append(file_name)

    # Create a pool of worker processes to download and convert the files
    with multiprocessing.Pool() as pool:
        pool.map(download_and_convert, file_names)

    # Rename and move the output files to the destination directory
    directory = "/home/e677/Videos/"
    output_file_prefix = "s1e"
    for i in range(1, 14):
        input_file = f"{output_file_prefix}{i}_0001.mp4"
        output_file = f"{output_file_prefix}{i}.mp4"
        os.rename(input_file, f"{directory}{output_file}")
