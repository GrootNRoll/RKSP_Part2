from db import insert_log, get_all_logs

def save_device_event(name: str):
    if not name or not name.strip():
        raise ValueError("Имя не может быть пустым")
    insert_log(name.strip())

def fetch_device_logs():
    return get_all_logs()