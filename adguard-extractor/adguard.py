import os
import urllib.request
import re
from fnmatch import fnmatch

# Function to download and process hosts files
def download_and_process_hosts(url):
    try:
        with urllib.request.urlopen(url) as response:
            hosts_content = response.read().decode('utf-8')
            return hosts_content
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return ""

# Function to process hosts content
def process_hosts_content(content):
    processed_lines = []
    for line in content.splitlines():
        if line.strip() and not line.startswith(("#", "!", "@", "?", "-", "<", ".", ":", "/")) and "$" not in line:
            line = re.sub(r'\^', '', line)
            processed_lines.append(line)
    
    return processed_lines

# Function to extract hostnames and write to file
def extract_and_write_hostnames(content, filename):
    hostnames = set()
    for line in content:
        hostnames.update(re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b|([\w.-]+)', line))
    
    hostnames.discard(None)

    with open(filename, 'w') as file:
        file.writelines(hostname + '\n' for hostname in hostnames)

# Function to filter out ignored hostnames
def filter_ignored_hostnames(hostnames, ignore_list):
    return [hostname for hostname in hostnames if not any(fnmatch(hostname, pattern) for pattern in ignore_list)]

# Function to create local hosts file
def create_local_hosts_file(filtered_hostnames, output_filename):
    with open(output_filename, 'w') as file:
        for i in range(0, len(filtered_hostnames), 1):
            line = '0.0.0.0 ' + ' '.join(filtered_hostnames[i:i+1]) + '\n'
            file.write(line)

def main():
    # Step 1
    temp_hosts_file_combined = "temp_hosts_file_combined.txt"
    temp_hostnames_file = "temp_hostnames.txt"
    local_file = "local_file.txt"
    ignore_list_file = "ignorelist.txt"

    # Step 2
    with open("lists.txt", "r") as lists_file, open(temp_hosts_file_combined, "a") as temp_file:
        for url in lists_file:
            url = url.strip()
            if url:
                content = download_and_process_hosts(url)
                processed_content = process_hosts_content(content)
                temp_file.write('\n'.join(processed_content) + '\n')

    # Step 3
    with open(temp_hosts_file_combined, "r") as temp_file:
        temp_content = temp_file.readlines()

    # Step 4
    with open(temp_hosts_file_combined, "w") as temp_file:
        temp_file.writelines(line.replace('^', '') for line in temp_content)

    # Step 5
    temp_content = [line for line in temp_content if '*' not in line]

    # Step 6
    extract_and_write_hostnames(temp_content, temp_hostnames_file)

    # Step 7
    with open(temp_hostnames_file, "r") as file:
        hostnames = file.readlines()

    # Step 8
    hostnames = [hostname.strip() for hostname in hostnames if hostname.strip()]

    # Step 9
    with open(ignore_list_file, "r") as ignore_file:
        ignore_list = [line.strip() for line in ignore_file]

    filtered_hostnames = filter_ignored_hostnames(hostnames, ignore_list)

    # Step 10
    create_local_hosts_file(filtered_hostnames, local_file)

if __name__ == "__main__":
    main()
