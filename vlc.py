import requests
import hashlib
import subprocess
import os

def get_expected_sha256(url):
    
    resp_msg = requests.get(url)
    if resp_msg.status_code == requests.codes.ok:
        return resp_msg.text.split()[0]
    return None

def download_installer(url):
    
    resp_msg = requests.get(url)
    if resp_msg.status_code == requests.codes.ok:
        return resp_msg.content
    return None

def verify_installer(installer_data, expected_sha256):
    
    sha256_hash = hashlib.sha256(installer_data).hexdigest()
    return sha256_hash == expected_sha256

def save_installer(installer_data, path):
    """Saves the installer to disk."""
    with open(path, 'wb') as file:
        file.write(installer_data)
    return path

def run_installer(path):
    """Runs the VLC installer silently."""
    subprocess.run([path, '/L=1033', '/S'])
    
def delete_installer(path):
    """Deletes the installer from disk."""
    os.remove(path)

def main():
    # Define URLs
    hash_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    installer_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    
    #  SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256(hash_url)
    
    installer_data = download_installer(installer_url)
    
    
    # expected and computed SHA-256 hash values
    if installer_data and verify_installer(installer_data, expected_sha256):
        # Saving the downloaded VLC installer to disk
        installer_path = os.path.join(os.getenv('TEMP'), 'vlc-3.0.17.4-win64.exe')
        save_installer(installer_data, installer_path)
        
        # Silently run the VLC installer
        run_installer(installer_path)
        
        # Deleting the VLC installer from disk
        delete_installer(installer_path)
    else:
        print("Installer verification failed. Download might be corrupted.")

if __name__ == '__main__':
    main()
