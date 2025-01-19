import os
import time
import subprocess
from shutil import move

# Directory to monitor for new files
MONITOR_DIRECTORY = r"C:\Users\ABAYO HIRWA JOVIN\OneDrive\Pictures\Benax"
PROCESSED_DIRECTORY = os.path.join(MONITOR_DIRECTORY, "processed")
UPLOAD_ENDPOINT = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Ensure the processed directory exists
os.makedirs(os.path.normpath(PROCESSED_DIRECTORY), exist_ok=True)

def upload_image(file_path):
    try:
        response = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{file_path}", UPLOAD_ENDPOINT],
            capture_output=True,
            text=True
        )
        if response.returncode == 0 and "200" in response.stdout:
            print(f"Upload successful: {file_path}")
            return True
        else:
            print(f"Upload failed for {file_path}: {response.stderr}")
            return False
    except Exception as error:
        print(f"Error during upload: {error}")
        return False

def watch_directory():
    print(f"Watching directory: {MONITOR_DIRECTORY}")
    while True:
        pending_files = [
            file_name for file_name in os.listdir(MONITOR_DIRECTORY)
            if os.path.isfile(os.path.join(MONITOR_DIRECTORY, file_name))
        ]
        for pending_file in pending_files:
            file_path = os.path.join(MONITOR_DIRECTORY, pending_file)
            if time.time() - os.path.getmtime(file_path) >= 30:  
                if upload_image(file_path):
                    move(file_path, os.path.join(PROCESSED_DIRECTORY, pending_file))
        time.sleep(10)

if __name__ == "__main__":
    watch_directory()
