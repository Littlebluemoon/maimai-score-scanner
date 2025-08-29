## maimai DX Score Scanner
A simple websocket scanner for scanning judgment data for maimai DX

## Installation

### Requirements
- Python 3
- gcc 64-bit

### Build .dll
```
gcc -shared -o address_capture.dll address_capture.c -m64
```

### Install python deps
```commandline
pip install -r requirements.txt
```

## Usage

### Start the game
You should be able to do this if you found this repo

### Launch server
```commandline
python server.py
```

Then access the frontend with `localhost:5000/score-scanner`

## Problems & Caveats
This project is based on memory editing and pointer scanning, so the following may (and will) occur:
- Frontend displays obviously incorrect results
- Multilevel pointers pointing to incorrect memory address
- Values occasionally flashes briefly, even if the memory address referenced by the pointer is correct

If anyone can find a way to do the things that this project do via any means and with higher consistency (via MelonLoader for example), please feel free to contribute. Thank you.