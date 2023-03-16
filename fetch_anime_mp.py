import os
import requests
import re
from multiprocessing import Pool, cpu_count
import subprocess
import argparse
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


# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Add an argument named "bangumi", "episodes", "season"
parser.add_argument('--bangumi', help='Specify the number of the bangumi')
parser.add_argument('--episodes', help='Specify the number of the episodes')
parser.add_argument('--season', help='Specify the number of the season')
parser.add_argument('--output-dir', help='Specify the output directory(without final slash!)')
parser.add_argument('--threads', help='Specify the threads parallelly')
# Parse the command-line arguments
args = parser.parse_args()

# Access the value of the "bangumi" argument
if args.bangumi:
    print('The specified bangumi is:', args.bangumi)
else:
    print('No bangumi was specified')

def download_file(url, file_path):
    print(f"Downloading {url}")
    r = requests.get(url, headers=headers, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def download_files(files):
    pool = Pool(int(args.threads))  # Use all available CPU cores
    for url, file_path in files:
        pool.apply_async(download_file, args=(url, file_path))
    pool.close()
    pool.join()

if __name__ == '__main__':
    

    files = []
    for i in range(1, int(args.episodes)):
        url = f"https://vpx06.myself-bbs.com/vpx/{args.bangumi}/{str(i).zfill(3)}_v01/720p.m3u8"
        response = requests.get(url, headers=headers)
        filenames = [line.strip() for line in response.text.split('\n') if line.endswith('.ts')]
        numbers = [int(re.findall(r'\d+', filename)[0]) for filename in filenames]
        max_number = max(numbers)
        for j in range(0, max_number):
            # parts of each episode
            file_name = f"{str(i).zfill(3)}_v01/720p_{str(j).zfill(3)}.ts"
            directory = f"{args.output_dir}/{str(i).zfill(3)}_v01"
            os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
            file_path = os.path.join(directory, f"720p_{str(j).zfill(3)}.ts")
            url = f"https://vpx08.myself-bbs.com/vpx/{args.bangumi}/{file_name}"
            files.append((url, file_path))
    download_files(files)



    # Merge the .ts files into individual .mp4 files
    directory = args.output_dir
    output_file_prefix = f"s{args.season}e"
    for i in range(1, int(args.episodes)):
        ts_files = ""
        url = f"https://vpx06.myself-bbs.com/vpx/{args.bangumi}/{str(i).zfill(3)}_v01/720p.m3u8"
        response = requests.get(url, headers=headers)
        filenames = [line.strip() for line in response.text.split('\n') if line.endswith('.ts')]
        numbers = [int(re.findall(r'\d+', filename)[0]) for filename in filenames]
        max_number = max(numbers)
        for j in range(0, max_number):
            ts_files += f"{directory}/{str(i).zfill(3)}_v01/720p_{str(j).zfill(3)}.ts|"
        ts_files = ts_files[:-1]  # Remove the last pipe symbol
        output_file = f"{output_file_prefix}{i}.mp4"
        command = f"ffmpeg -i \"concat:{ts_files}\" -c copy {directory}/{output_file}"
        subprocess.call(command, shell=True)

    
    # Remove the .ts files and folders
    for i in range(1, int(args.episodes)):
        url = f"https://vpx06.myself-bbs.com/vpx/{args.bangumi}/{str(i).zfill(3)}_v01/720p.m3u8"
        response = requests.get(url, headers=headers)
        filenames = [line.strip() for line in response.text.split('\n') if line.endswith('.ts')]
        numbers = [int(re.findall(r'\d+', filename)[0]) for filename in filenames]
        max_number = max(numbers)
        for j in range(0, max_number):
            file_path = f"{directory}/{str(i).zfill(3)}_v01/720p_{str(j).zfill(3)}.ts"
            os.remove(file_path)
            folder_path = f"{directory}/{str(i).zfill(3)}_v01/"
            os.rmdir(folder_path)
