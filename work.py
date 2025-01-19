import os
import time
import shutil
import subprocess

# Configuration
WATCH_FOLDER = r"C:\Users\ABAYO HIRWA JOVIN\OneDrive\Pictures\Benax"
UPLOADED_FOLDER = r"C:\Users\ABAYO HIRWA JOVIN\OneDrive\Pictures\Benax\uploaded"
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"
UPLOAD_KEY = "imageFile"
UPLOAD_INTERVAL = 30  # seconds

def monitor_and_upload():
    if not os.path.exists(WATCH_FOLDER):
        print(f"Error: Watch folder {WATCH_FOLDER} does not exist.")
        return

    if not os.path.exists(UPLOADED_FOLDER):
        os.makedirs(UPLOADED_FOLDER)

    print(f"Monitoring folder: {WATCH_FOLDER}\nUploading images to: {UPLOAD_URL}")

    while True:
        # Get list of files in the watch folder
        files = [f for f in os.listdir(WATCH_FOLDER) if os.path.isfile(os.path.join(WATCH_FOLDER, f))]

        for file in files:
            file_path = os.path.join(WATCH_FOLDER, file)
            try:
                # Upload the file using curl
                print(f"Uploading: {file}")
                result = subprocess.run(
                    ["curl", "-X", "POST", "-F", f"{UPLOAD_KEY}=@{file_path}", UPLOAD_URL],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                if result.returncode == 0:
                    print(f"Successfully uploaded: {file}")
                    # Move the file to the uploaded folder
                    shutil.move(file_path, os.path.join(UPLOADED_FOLDER, file))
                else:
                    print(f"Failed to upload {file}. Error: {result.stderr}")

            except Exception as e:
                print(f"Error processing {file}: {e}")

        # Wait before checking for new files
        time.sleep(UPLOAD_INTERVAL)

if __name__ == "__main__":
    monitor_and_upload()
