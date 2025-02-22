import os
import shutil
import json
import time
from datetime import datetime, timedelta

SETTINGS_FILE = "settings.json"


def check_path_exists(path):
    return os.path.exists(path)


def create_default_settings():
    """Erstellt eine Standard settings.json-Datei, falls sie nicht existiert."""
    if not check_path_exists(SETTINGS_FILE):
        default_data = {
            "backup_intervall": 60,  # Standard: 60 Minuten
            "sync_ordner": ["C:/Users/Benutzer/Dokumente"],
            "last_sync": datetime.now().isoformat(),
            "sync_device": "D:/auto_backup",
            "max_backups": 5  # Maximale Anzahl an Backups
        }

        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(default_data, file, indent=4, ensure_ascii=False)

        print("Standard-Settings wurden erstellt.")


def load_settings():
    """Lädt die Einstellungen, erstellt Standardwerte, falls Datei fehlt."""
    create_default_settings()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return (data["backup_intervall"],
                data["sync_ordner"],
                datetime.fromisoformat(data["last_sync"]),
                data["sync_device"],
                data["max_backups"])
    except (json.JSONDecodeError, KeyError, ValueError):
        print("⚠ Fehler in settings.json erkannt! Bitte Datei manuell prüfen und korrigieren.")
        return None


def save_settings(backup_intervall, sync_ordner, last_sync, sync_device, max_backups):
    data = {
        "backup_intervall": backup_intervall,
        "sync_ordner": sync_ordner,
        "last_sync": last_sync.isoformat(),
        "sync_device": sync_device,
        "max_backups": max_backups
    }

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def is_backup_device_connected(path, src):
    if check_path_exists(path):
        datetime_string = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        print(f"Der Pfad '{path}' existiert.")
        name = src.replace(":", "-").replace("/", "_")
        dst = f"{path}/{datetime_string}/{name}"
        shutil.copytree(src, dst)
        return True
    return False


def cleanup_old_backups(backup_path, max_backups):
    """Löscht alte Backups, wenn die maximale Anzahl überschritten wird."""
    if not check_path_exists(backup_path):
        print(f"⚠ Der Backup-Pfad '{backup_path}' existiert nicht.")
        return

    try:
        # Liste der Backups erstellen und nach Erstellungsdatum sortieren
        backups = sorted(
            [os.path.join(backup_path, d) for d in os.listdir(backup_path) 
             if os.path.isdir(os.path.join(backup_path, d)) and "System Volume Information" not in d],
            key=lambda x: os.path.getctime(x)  # Nach Erstellungsdatum sortieren
        )

        # Alte Backups löschen, wenn die Anzahl überschritten wird
        while len(backups) > max_backups:
            oldest_backup = backups.pop(0)
            shutil.rmtree(oldest_backup)
            print(f"Altes Backup gelöscht: {oldest_backup}")

    except PermissionError as e:
        print(f"⚠ Zugriff verweigert beim Löschen von '{backup_path}': {e}")
    except Exception as e:
        print(f"⚠ Fehler beim Bereinigen der Backups: {e}")


def check_sync_intervall(last_sync, sync_intervall):
    now = datetime.now()
    time_difference = now - last_sync
    return time_difference.total_seconds() / 60 > sync_intervall


def run_backup():
    settings = load_settings()
    if settings is None:
        return "Fehlerhafte settings.json – Backup wird nicht ausgeführt!"

    backup_intervall, sync_ordner, last_sync, sync_device, max_backups = settings

    if not check_sync_intervall(last_sync, backup_intervall):
        return "Es ist noch nicht Zeit für ein Backup."

    for i in sync_ordner:
        if not is_backup_device_connected(sync_device, i):
            return "Kein externes Laufwerk erkannt."
    
    cleanup_old_backups(sync_device, max_backups)
    
    now = datetime.now()
    save_settings(backup_intervall, sync_ordner, now, sync_device, max_backups)
    
    return "Backup abgeschlossen."

# Hauptschleife für automatische Backups
while True:
    print(run_backup())
    time.sleep(10)
