import os
import urllib.request
from fnmatch import fnmatch

def download_hosts_file(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return ""

def extract_hostnames(content):
    hostnames = []
    for line in content.splitlines():
        if not line.strip() or line.startswith(("#", "!", "@", "?", "-", "<", ".", ":", "/")) and "$" not in line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            hostnames.append(parts[1])
    return hostnames

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def main():
    # Step 1
    with open('lists.txt') as lists_file:
        urls = [line.strip() for line in lists_file if line.strip()]

    temp_hosts_file = "temp_hosts_file_combined.txt"
    temp_hostnames_file = "temp_hostnames.txt"
    ignore_list_file = "ignorelist.txt"
    local_file = "local_file.txt"

    combined_hosts_content = ""

    # Step 2 & 3
    for url in urls:
        hosts_content = download_hosts_file(url)
        combined_hosts_content += hosts_content

    write_to_file(temp_hosts_file, combined_hosts_content)

    # Step 4 & 5
    hostnames = extract_hostnames(combined_hosts_content)
    write_to_file(temp_hostnames_file, '\n'.join(hostnames))

    # Step 6
    unique_hostnames = list(set(hostnames))

    # Step 7
    with open(ignore_list_file) as ignore_file:
        ignore_list = [line.strip() for line in ignore_file if line.strip()]

    for pattern in ignore_list:
        unique_hostnames = [h for h in unique_hostnames if not fnmatch(h, pattern)]

    # Step 8
    unique_hostnames.sort()

    # Step 9 & 10
    with open(local_file, 'w') as local_file:
        for i in range(0, len(unique_hostnames), 1):
            line = '0.0.0.0 ' + ' '.join(unique_hostnames[i:i+1])
            local_file.write(line + '\n')

if __name__ == "__main__":
    main()
