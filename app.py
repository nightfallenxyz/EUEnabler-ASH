from helper.helper_paths.file_restore_path import files_to_restore_empty, files_to_restore_patches
from helper.helper_func.functions import prompt_for_action, restore, traceback
from time import sleep

# Get the region code from the user
region_code = input("Enter YOUR CURRENT 2-letter region code (default to US): ").strip().upper() or "US"
print("Please wait...")

# Prompt the user for action
choice = prompt_for_action()

try:
    if choice == '1':
        restore(files_to_restore_empty)
    elif choice == '2':
        restore(files_to_restore_patches)
    elif choice == '3':
        restore(files_to_restore_empty)  # First restore with empty files
        input("Press Enter after rebooting and unlocking...")
        restore(files_to_restore_patches)  # Then restore with patches
        input("Press Enter after rebooting and unlocking...")
    elif choice == '4':
        input("Make sure your phone has no passcode enabled and hit enter")
        while True:
            restore(files_to_restore_empty)
            time.sleep(30)
    elif choice == '5':
        input("Make sure your phone has no passcode enabled and hit enter")
        while True:
            restore(files_to_restore_empty)
            time.sleep(30)
            restore(files_to_restore_patches)
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
except Exception as e:
    print(traceback.format_exc())
finally:
    input("Press Enter to exit...")
