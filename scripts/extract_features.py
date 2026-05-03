import os
import subprocess
import pandas as pd
from nfstream import NFStreamer

DATA_DIR = "../data"
OUTPUT_CSV = "../dataset.csv"

splits = ["learning", "testing", "validating"]
labels = {"malicious": 1, "normal": 0}


def get_payload_from_tshark(pcap_path):
    """Runs tshark to get TCP payload and decodes hex to ASCII (LIMITED to 2000 bytes)                                                                                                            chars)."""
    cmd = ['tshark', '-r', pcap_path, '-T', 'fields', '-e', 'tcp.payload']

    try:
        raw_hex = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode                                                                                                             ('utf-8')
        lines = [line.strip() for line in raw_hex.splitlines() if line.strip()]

        ascii_payloads = []
        total_chars = 0
        LIMIT = 2000

        for hex_str in lines:
            try:
                text = bytes.fromhex(hex_str).decode('utf-8', errors='ignore')

                remaining = LIMIT - total_chars
                if remaining <= 0:
                    break

                # truncate per chunk
                text = text[:remaining]
                ascii_payloads.append(text)
                total_chars += len(text)

            except Exception:
                continue

        return " ".join(ascii_payloads)

    except Exception:
        return ""


all_dfs = []

for split in splits:
    for label_name, label_val in labels.items():
        folder = os.path.join(DATA_DIR, split, label_name)
        if not os.path.exists(folder):
            print(f"Not found: {folder}")
            continue

        pcap_files = [f for f in os.listdir(folder) if f.endswith(".pcapng")]
        print(f"[{split}/{label_name}] Found {len(pcap_files)} files")

        for pcap_file in pcap_files:
            pcap_path = os.path.join(folder, pcap_file)
            try:
                streamer = NFStreamer(source=pcap_path, statistical_analysis=True)
                df = streamer.to_pandas()
                if df.empty:
                    print(f"  EMPTY: {pcap_file}")
                    continue
                payload_text = get_payload_from_tshark(pcap_path)
                df["raw_payload"] = payload_text
                df["label"] = label_val
                df["split"] = split
                df["source_file"] = pcap_file
                all_dfs.append(df)
                print(f"  OK: {pcap_file} ({len(df)} flows)")
            except Exception as e:
                print(f"  ERROR: {pcap_file} -> {e}")

if all_dfs:
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved {len(final_df)} flows to {OUTPUT_CSV}")
    print(f"Label distribution:\n{final_df['label'].value_counts()}")
else:
    print("No data extracted")
