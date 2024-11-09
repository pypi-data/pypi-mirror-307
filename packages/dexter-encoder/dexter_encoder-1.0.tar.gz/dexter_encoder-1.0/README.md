# Dexter Encoder

Dexter is a custom encoding library designed for security professionals and developers who need to obfuscate shellcode or sensitive data as part of security testing and analysis. By applying complex encoding rules, Dexter aims to bypass Intrusion Detection Systems (IDS) and evade signature-based detection, making it a valuable tool in controlled, ethical hacking and red team assessments.  
## Features
- **Advanced Encoding**: Uses dynamic, randomized shifts to obfuscate data effectively.
- **Simple Interface**: Easy-to-use `encode()` and `decode()` methods for quick encoding and decoding.
- **Security-Oriented**: Designed to enhance security testing workflows while minimizing the risk of detection.
                                                        ## Installation

Install Dexter easily via pip:                          
```bash
pip install dexter-encoder
```
## Usage

Once installed, you can import the Dexter library and use the `encode()` and `decode()` methods to obfuscate and deobfuscate your data.

### Example:

```python
import dexter as d  # Import the Dexter encoding library
```

# Encoding & Decoding
```
data = "this is secret data"
```

# Encoding the data
```
encoded_data = d.encode(data)
print(f"Encoded: {encoded_data}")
```

# Decoding the data
```
decoded_data = d.decode(encoded_data)
print(f"Decoded: {decoded_data}")

```
