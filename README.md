# Spring4Shell Detection using Random Forest

This is a machine learning-based project for the IT Network Security course at Vilnius University.

The project focuses on detecting **Spring4Shell (CVE-2022-22965)** vulnerability exploitation by combining traditional statistical flow metrics with application layer payload analysis.

## Project Structure

* `data/` - Raw PCAPNG files (learning, testing, validating splits).
* `scripts/` - Automation for the entire pipeline:
    * `setup_victim.sh` / `setup_attacker.sh` / `setup_data.sh` - Environment preparation (Docker, TShark, etc.).
    * `simulate_attacker_traffic.py` / `simulate_valid_traffic.sh` - Traffic generation for dataset creation.
    * `capture_traffic.sh` - Live traffic capture utility.
    * `extract_features.py` - Hybrid feature extractor (NFStreamer + TShark).
* `model/` - Machine learning logic:
    * `model.py` - Initial flow-based Random Forest.
    * `model_payload.py` - Advanced detection using `TfidfVectorizer` for payload keywords.
* `victim/` - Vulnerable Spring Boot application.
* `poc/` - Exploit PoC.

## Data Pipeline

1. **Traffic Simulation:** Malicious and normal traffic is generated and captured into `.pcapng` files.
2. **Feature Extraction:** The extract features script uses `NFStreamer` to extract flow-based features (packet counts, ratios, durations) and `tshark` to grab the raw TCP payload (limited to 2000 chars).
3. **Preprocessing:** Data is split into `learning`, `testing`, and `validating` sets. Features like `packet_ratio`, `ack_ratio`, and `duration_ratio` are engineered for better accuracy.

### Traffic Types:
1. **Normal Traffic:** Randomized CRUD operations and harmless 404 errors.
2. **Abnormal Traffic:** Spring4Shell exploitation followed by post-exploitation activities (reconnaissance, credential theft).

## Feature Engineering
The core of the detection logic lies in the hybrid feature set:
* **Flow Metrics:** Packet counts, SYN/ACK/PSH flag frequencies.
* **Engineered Ratios:** `Packet Ratio`, `ACK Ratio`, and `Duration Ratio`.
* **Payload Analysis:** Using `TfidfVectorizer` to detect L7 keywords like `classLoader`, `runtime`, and `jsp`, as well as protocol signatures (e.g., frequency of `=` characters in POST requests).

## Model Performance

The detection system is implemented as a Scikit-learn `Pipeline` using a `ColumnTransformer`.
* **Algorithm:** Random Forest.
* **Dataset:** 100 PCAP files (approx. 5000 packets each).
* **Accuracy:** ~84%.
* **Key Finding:** While the model initially relied on flow duration, the inclusion of payload-based features significantly reduced false positives and improved robustness against network jitter.

## How to Run

### Setup Environment

```bash
cd scripts
sudo ./setup_victim.sh
sudo ./setup_attacker.sh
sudo ./setup_data.sh
```

### Generate Normal Traffic Data
```bash
# In one terminal: Simulate normal traffic
cd scripts
python3 simulate_valid_traffic.py

# In another: capture traffic
./capture_traffic.sh
```

### Generate Abnormal Traffic Data
```bash
# In one terminal: Run poc and simulate abnormal traffic
cd ../poc
python3 exploit.py --url http://localhost:8080/save
cd ../scripts
python3 simulate_attacker_traffic.py http://localhost:8080/shell.jsp

# In another: capture traffic
./capture_traffic.sh
```

### Feature Extraction
```bash
python3 extract_features.py
```

### Model Training and Evaluation
```bash
cd ../model
python3 model_payload.py
```
