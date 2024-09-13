from exploit.restore import restore_files, FileToRestore, restore_file

from pymobiledevice3.exceptions import PyMobileDevice3Exception
from pymobiledevice3.services.diagnostics import DiagnosticsService
from pymobiledevice3 import usbmux
from pymobiledevice3.lockdown import create_using_usbmux

from pathlib import Path
from tempfile import TemporaryDirectory
import traceback
import plistlib
import traceback
from time import sleep

# Function to replace the region code in a plist file
def replace_region_code(plist_path, original_code="US", new_code="US"):
    with open(plist_path, 'rb') as f:
        plist_data = plistlib.load(f)

    plist_str = str(plist_data)
    updated_plist_str = plist_str.replace(original_code, new_code)
    updated_plist_data = eval(updated_plist_str)  # Convert string back to dictionary

    return plistlib.dumps(updated_plist_data)

# Function to handle file restoration
def restore(files, max_retries=3):
    for attempt in range(max_retries):
        try:
            restore_files(files=files, reboot=True)
            break  # Exit loop on success
        except ConnectionAbortedError:
            print(f"Connection aborted, retrying... ({attempt + 1}/{max_retries})")
            sleep(2)  # Pause before retrying
        except Exception as e:
            print(traceback.format_exc())
            break

# Function to prompt the user for an action
def prompt_for_action():
    print("Select an option:")
    print("1. Restore files with no data")
    print("2. Apply eligibility and config patches")
    print("3. Restore files with no data and apply patches")
    choice = input("Enter your choice (1, 2, or 3): ").strip()
    return choice

# Get the region code from the user
region_code = input("Enter YOUR CURRENT 2-letter region code (default to US): ").strip().upper() or "US"
print("Please wait...")

# Paths to plist files
file_path = Path.joinpath(Path.cwd(), 'eligibility.plist')
with open(file_path, 'rb') as file:
    eligibility_data = file.read()
file_path = Path.joinpath(Path.cwd(), 'Config.plist')
with open(file_path, 'rb') as file:
    config_data = file.read()

# File definitions for restoring
files_to_restore_empty = [  # Empty restore files
    FileToRestore(
        contents=b'',
        restore_path="/var/db/os_eligibility/",
        restore_name="eligibility.plist"
    ),
    FileToRestore(
        contents=b'',
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/c55a421c053e10233e5bfc15c42fa6230e5639a9.asset/AssetData/",
        restore_name="Config.plist"
    ),
    FileToRestore(
        contents=b'',
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/247556c634fc4cc4fd742f1b33af9abf194a986e.asset/AssetData/",
        restore_name="Config.plist"
    ),
    FileToRestore(
        contents=b'',
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/250df115a1385cfaad96b5e3bf2a0053a9efed0f.asset/AssetData/",
        restore_name="Config.plist"
    ),
]

files_to_restore_patches = [  # Files to apply eligibility and config patches
    FileToRestore(
        contents=eligibility_data,
        restore_path="/var/db/os_eligibility/",
        restore_name="eligibility.plist"
    ),
    FileToRestore(
        contents=config_data,
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/c55a421c053e10233e5bfc15c42fa6230e5639a9.asset/AssetData/",
        restore_name="Config.plist"
    ),
    FileToRestore(
        contents=config_data,
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/247556c634fc4cc4fd742f1b33af9abf194a986e.asset/AssetData/",
        restore_name="Config.plist"
    ),
    FileToRestore(
        contents=config_data,
        restore_path="/var/MobileAsset/AssetsV2/com_apple_MobileAsset_OSEligibility/purpose_auto/250df115a1385cfaad96b5e3bf2a0053a9efed0f.asset/AssetData/",
        restore_name="Config.plist"
    ),
]

# Prompt the user for action
choice = prompt_for_action()

try:
    if choice == '1':
        restore(files_to_restore_empty)
    elif choice == '2':
        print("You need to restore with empty files first before applying patches.")
        input("Press enter if you ran method 1 before...")
        restore(files_to_restore_patches)
    elif choice == '3':
        restore(files_to_restore_empty)  # First restore with empty files
        input("Press Enter after rebooting and unlocking...")
        restore(files_to_restore_patches)  # Then restore with patches
        input("Press Enter after rebooting and unlocking...")
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
except Exception as e:
    print(traceback.format_exc())
finally:
    input("Press Enter to exit...")
