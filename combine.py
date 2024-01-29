def combine_hosts(file1, file2, combined_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(combined_file, 'w') as combined:
        combined.write(f1.read())
        combined.write(f2.read())

def read_hostnames(input_file):
    with open(input_file, 'r') as file:
        return set(line.split()[1].strip().lower() for line in file if line.strip())

def extract_hostnames(hostnames_set, output_file):
    with open(output_file, 'w') as output:
        output.write('\n'.join(hostnames_set))

def read_custom_hostnames(custom_file, hostnames_set):
    with open(custom_file, 'r') as custom:
        custom_hostnames = set(line.strip().lower() for line in custom if line.strip())
        hostnames_set.update(custom_hostnames)

def create_hosts_file(hostnames_set, output_file):
    unique_hostnames = sorted(hostnames_set, key=lambda s: s.lower())  # Remove duplicates case-insensitively
    with open(output_file, 'w') as output_file:
        for i in range(0, len(unique_hostnames), 9):
            output_file.write("0.0.0.0 " + " ".join(unique_hostnames[i:i+9]) + "\n")

if __name__ == "__main__":
    hosts_file1 = "local_file.txt"
    hosts_file2 = "adguard-extractor/local_file.txt"
    combined_hosts_file = "main_combined_hosts.txt"
    custom_hostnames_file = "custom.txt"
    temp_hostnames_file = "final_temp.txt"
    final_hosts_file = "HOSTS"

    # Combine hosts files
    combine_hosts(hosts_file1, hosts_file2, combined_hosts_file)

    # Read hostnames from combined hosts file
    hostnames_set = read_hostnames(combined_hosts_file)

    # Read custom hostnames
    read_custom_hostnames(custom_hostnames_file, hostnames_set)

    # Extract and create new hosts file with IP 0.0.0.0
    extract_hostnames(hostnames_set, temp_hostnames_file)
    create_hosts_file(hostnames_set, final_hosts_file)

    print(f"Script executed successfully. The new hosts file '{final_hosts_file}' has been created.")
