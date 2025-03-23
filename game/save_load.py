import os
import json
from cryptography.fernet import Fernet

def get_or_create_key():
    key_path = os.path.join(os.environ.get('KOHIHAUSU_SAVES', os.path.expanduser('~/Documents/My Games/Kohihausu')), 'key.key')
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
    return key

def save_game_encrypted(state):
    key = get_or_create_key()
    cipher = Fernet(key)
    save_path = os.path.join(os.environ.get('KOHIHAUSU_SAVES', os.path.expanduser('~/Documents/My Games/Kohihausu')), 'save_game.dat')
    with open(save_path, 'wb') as f:
        encrypted_data = cipher.encrypt(json.dumps(state).encode())
        f.write(encrypted_data)

def load_game_encrypted():
    key = get_or_create_key()
    cipher = Fernet(key)
    save_path = os.path.join(os.environ.get('KOHIHAUSU_SAVES', os.path.expanduser('~/Documents/My Games/Kohihausu')), 'save_game.dat')
    if os.path.exists(save_path):
        with open(save_path, 'rb') as f:
            encrypted_data = f.read()
            try:
                decrypted_data = cipher.decrypt(encrypted_data).decode()
                return json.loads(decrypted_data)
            except Exception:
                return None
    return None