#!/usr/bin/env python3

import os
import asyncio
from chat_shell.smart_shell import SmartShell



def main():
    shell = SmartShell()
    try:
        asyncio.run(shell.run())
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    return 0

# if __name__ == "__main__":
#     exit(main())
def entry_point():
    exit(main())