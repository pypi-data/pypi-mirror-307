#! /usr/bin/env python3

## logger.py

import railwaypacriman.config as cfg

def log(message):
    if cfg.DEBUG_MODE:
        print(f"DEBUG: {message}")

if __name__ == "__main__":
    main()

