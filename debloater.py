#!/usr/bin/env python3
"""
Android Universal Debloat & Optimization Tool
Compatible with Android 8 to 15+ (Fire OS, HiOS, OneUI, MIUI/HyperOS, ColorOS, OxygenOS, RealUI, Motorola, Pixel).
"""

import argparse
import datetime
import json
import os
import subprocess
import sys

# Manufacturer Database & Bloatware Lists
DEBLOAT_PROFILES = {
    "tecno_infinix": {
        "name": "Tecno / Infinix / Itel (Transsion HiOS / XOS)",
        "packages": [
            "com.transsion.statisticalsales",
            "com.transsion.uxdetector",
            "com.transsion.ella",
            "com.transsion.kolun.aiservice",
            "com.transsion.kolun.assistant",
            "com.transsion.aivoiceassistant",
            "com.transsion.aisettings",
            "com.transsion.aisupportercore",
            "com.transsion.microintelligence",
            "com.transsion.magazineservice.hios",
            "com.transsion.magicshow",
            "com.transsion.smartpanel",
            "com.transsion.tecnospot",
            "com.transsnet.store",
            "net.bat.store",
            "com.transsion.mol",
            "com.transsion.nephilim",
            "com.transsion.zahooc",
            "com.transsion.succ",
            "com.transsion.tabe",
            "com.transsion.teop",
            "com.transsion.sk",
            "com.transsion.tower",
            "com.transsion.tranengine",
            "com.transsion.trancare",
            "com.transsion.overlaysuw",
            "com.transsion.overlaysuw.resoverlay",
            "com.hilauncherconfig",
            "com.hoffnung",
            "com.idea.questionnaire",
            "com.transsion.manualguide",
            "com.funbase.xradio",
            "com.talpa.hibrowser",
            "com.talpa.hiservice",
            "com.rlk.weathers",
            "com.sh.smart.caller",
            "com.transsion.repaircard",
            "com.transsion.cloudserver",
            "com.transsion.thunderback",
            "com.skyroam.silverhelper",
            "com.reallytek.wg",
            "com.transsion.letswitch",
            "com.facebook.appmanager",
            "com.facebook.services",
            "com.facebook.system",
            "com.transsion.carlcare"
        ]
    },
    "amazon_firetv": {
        "name": "Amazon Fire TV & Fire Tablets (Fire OS)",
        "packages": [
            "com.amazon.device.sale.service",
            "com.amazon.tarkin",
            "com.amazon.whisperplay.contracts",
            "com.amazon.shpm",
            "com.amazon.visualservice",
            "com.amazon.advertising.service",
            "com.amazon.kor.tz",
            "com.amazon.recess",
            "com.amazon.bueller.music",
            "com.amazon.bueller.photos",
            "com.amazon.ftv.screensaver",
            "com.amazon.device.crashmanager",
            "com.amazon.tv.settings.v2",
            "com.amazon.ods.kindleconnect"
        ]
    },
    "xiaomi": {
        "name": "Xiaomi / Redmi / POCO (MIUI / HyperOS)",
        "packages": [
            "com.miui.analytics",
            "com.miui.msa.global",
            "com.miui.bugreport",
            "com.miui.yellowpage",
            "com.miui.translation.kingsoft",
            "com.miui.translation.youdao",
            "com.miui.hybrid",
            "com.miui.hybrid.accessory",
            "com.xiaomi.joyose",
            "com.xiaomi.midrop",
            "com.xiaomi.mipicks",
            "com.mi.globalbrowser"
        ]
    },
    "samsung": {
        "name": "Samsung (One UI)",
        "packages": [
            "com.samsung.android.bixby.agent",
            "com.samsung.android.bixby.wakeup",
            "com.samsung.android.bixbyvision.framework",
            "com.samsung.android.spay",
            "com.samsung.android.spayfw",
            "com.samsung.android.app.spage",
            "com.samsung.android.game.gamehome",
            "com.samsung.android.game.gametools",
            "com.sec.android.app.sbrowser"
        ]
    },
    "general_meta": {
        "name": "Universal Facebook / Meta Bloatware",
        "packages": [
            "com.facebook.appmanager",
            "com.facebook.services",
            "com.facebook.system"
        ]
    }
}

def run_adb(cmd, device=None):
    dev_flag = f"-s {device}" if device else ""
    full_cmd = f"adb {dev_flag} {cmd}".strip()
    res = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def detect_device(device=None):
    code, stdout, _ = run_adb("devices -l", device)
    lines = [l for l in stdout.splitlines() if "device " in l and not l.startswith("List of")]
    if not lines:
        print("[!] No se detectó ningún dispositivo Android conectado por ADB.")
        print("    Asegúrate de tener la depuración USB o inalámbrica activa.")
        return None
    print(f"[✓] Dispositivo detectado: {lines[0]}")
    _, brand, _ = run_adb("shell getprop ro.product.brand", device)
    _, model, _ = run_adb("shell getprop ro.product.model", device)
    _, android_ver, _ = run_adb("shell getprop ro.build.version.release", device)
    print(f"    Marca: {brand} | Modelo: {model} | Android: {android_ver}")
    return {"brand": brand.lower(), "model": model, "android": android_ver}

def list_installed_packages(device=None):
    code, stdout, _ = run_adb("shell pm list packages --user 0", device)
    return set(line.replace("package:", "").strip() for line in stdout.splitlines() if line.strip())

def debloat(profile_key, device=None):
    if profile_key not in DEBLOAT_PROFILES:
        print(f"[!] Perfil desconocido: {profile_key}")
        print(f"    Perfiles disponibles: {', '.join(DEBLOAT_PROFILES.keys())}")
        return

    profile = DEBLOAT_PROFILES[profile_key]
    print(f"\n[+] Iniciando debloat para: {profile['name']}")
    installed = list_installed_packages(device)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_debloat_{profile_key}_{timestamp}.json"
    
    backup_data = {
        "profile": profile_key,
        "timestamp": timestamp,
        "disabled_packages": [],
        "skipped_packages": [],
        "errors": []
    }

    for pkg in profile["packages"]:
        if pkg in installed:
            code, out, err = run_adb(f"shell pm disable-user --user 0 {pkg}", device)
            if code == 0 or "disabled" in out.lower() or "new state" in out.lower():
                print(f"  [✓] Desactivado: {pkg}")
                backup_data["disabled_packages"].append(pkg)
            else:
                print(f"  [!] Error al desactivar {pkg}: {err or out}")
                backup_data["errors"].append({"pkg": pkg, "error": err or out})
        else:
            print(f"  [-] No encontrado / Ya inactivo: {pkg}")
            backup_data["skipped_packages"].append(pkg)

    with open(backup_file, "w") as f:
        json.dump(backup_data, f, indent=2)

    print("\n[✓] Proceso de debloat finalizado.")
    print(f"    Total desactivados: {len(backup_data['disabled_packages'])}")
    print(f"    Copia de seguridad guardada en: {backup_file}")
    print("    Puedes revertir en cualquier momento con: python3 debloater.py restore --file " + backup_file)

def restore_from_backup(backup_file, device=None):
    if not os.path.exists(backup_file):
        print(f"[!] Archivo de backup no encontrado: {backup_file}")
        return
    with open(backup_file, "r") as f:
        data = json.load(f)
    packages = data.get("disabled_packages", [])
    print(f"\n[+] Restaurando {len(packages)} paquetes desde: {backup_file}")
    restored = 0
    for pkg in packages:
        code, out, err = run_adb(f"shell pm enable {pkg}", device)
        if code == 0 or "enabled" in out.lower() or "new state" in out.lower():
            print(f"  [✓] Reactivado: {pkg}")
            restored += 1
        else:
            print(f"  [!] Falló reactivación de {pkg}: {err or out}")
    print(f"\n[✓] Restauración completada: {restored}/{len(packages)} reactivados.")

def install_launcher(device=None):
    apk_path = os.path.join(os.path.dirname(__file__), "apps", "Nova-Launcher-8.8.6-Prime.apk")
    if not os.path.exists(apk_path):
        print(f"[!] No se encontró el instalador de Nova Launcher en: {apk_path}")
        return
    print(f"\n[+] Instalando Nova Launcher Prime en el dispositivo...")
    code, out, err = run_adb(f"install -r \"{apk_path}\"", device)
    if code == 0 and "success" in out.lower():
        print("[✓] Nova Launcher Prime instalado con éxito.")
    else:
        print(f"[!] Error de instalación: {err or out}")

def main():
    parser = argparse.ArgumentParser(description="Universal Android Debloat & Optimization Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Command: detect
    subparsers.add_parser("detect", help="Detectar dispositivo conectado")

    # Command: debloat
    p_debloat = subparsers.add_parser("debloat", help="Desactivar bloatware según perfil")
    p_debloat.add_argument("--profile", required=True, choices=list(DEBLOAT_PROFILES.keys()), help="Perfil de fabricante")
    p_debloat.add_argument("--device", help="Serial o IP:puerto del dispositivo ADB")

    # Command: restore
    p_restore = subparsers.add_parser("restore", help="Restaurar paquetes desde archivo JSON")
    p_restore.add_argument("--file", required=True, help="Ruta al archivo JSON de respaldo")
    p_restore.add_argument("--device", help="Serial o IP:puerto del dispositivo ADB")

    # Command: install-nova
    p_nova = subparsers.add_parser("install-nova", help="Instalar Nova Launcher Prime")
    p_nova.add_argument("--device", help="Serial o IP:puerto del dispositivo ADB")

    args = parser.parse_args()

    if args.command == "detect":
        detect_device()
    elif args.command == "debloat":
        debloat(args.profile, args.device)
    elif args.command == "restore":
        restore_from_backup(args.file, args.device)
    elif args.command == "install-nova":
        install_launcher(args.device)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
