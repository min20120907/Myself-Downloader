import os
import requests
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
    directory = "/home/e677/Videos"
    file_path = os.path.join(directory, file_name)

    # Download the file
    url = f"https://vpx08.myself-bbs.com/vpx/43563/{file_name}"
    print(f"Downloading {url}")
    r = requests.get(url, headers=headers, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    # Convert the file to mp4
    print(f"Converting {file_path} to mp4")
    os.system(f"ffmpeg -i {file_path} -c:v copy -c:a copy {os.path.splitext(file_path)[0]}.mp4")

    # Remove the original ts file
    os.remove(file_path)

if __name__ == '__main__':
    file_names = []
    for i in range(1, 14):
        for j in range(0, 146):
            file_name = f"720p_{str(j).zfill(3)}.ts"
            file_names.append(f"s{i}e{j+1}.mp4")
            download_and_convert(file_name)

    # Create a pool of worker processes to download and convert the files
    with multiprocessing.Pool(os.cpu_count()) as pool:
        pool.map(download_and_convert, file_names)

    # Rename and move the output files to the destination directory
    directory = "/home/e677/Videos/"
    output_file_prefix = "s1e"
    for i in range(1, 14):
        input_file = f"{output_file_prefix}{i}_0001.mp4"
        output_file = f"{output_file_prefix}{i}.mp4"
        os.rename(input_file, f"{directory}{output_file}")
