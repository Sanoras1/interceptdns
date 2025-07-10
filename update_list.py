import requests
OUTFILE = "blockedList.txt"

def update_list(entry):
    r = requests.get(entry)
    lines = r.text.splitlines()
    with open(OUTFILE, "w") as f:
        for line in lines:
            if line.startswith("0.0.0.0 "):
                domain = line.split()[1]
                f.write(domain + "\n")

if __name__ == "__main__":
    URL = "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
    update_list(URL)
    print("[INFO] updated.")