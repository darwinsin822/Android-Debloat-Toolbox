# 📱 Android Universal Debloat & Optimization Toolbox

Herramienta universal de código abierto diseñada para auditar, limpiar y deshabilitar bloatware, adware y telemetría de fábrica en dispositivos móviles Android (smartphones y tablets), con **garantía de reversibilidad total al 100%**.

Incluye el instalador optimizado de **Nova Launcher Prime (v8.8.6)** para sustituir launchers pesados del fabricante.

---

## 🛡️ REGLA DE ORO DE COMUNICACIONES (PROTECCIÓN ESTRICTA)

> [!IMPORTANT]
> **Protección absoluta de apps de Teléfono, Marcador, Contactos y SMS:**
> Esta herramienta tiene prohibido de forma determinista modificar o deshabilitar cualquier componente relacionado con llamadas telefónicas, libreta de contactos, mensajería SMS y servicios de emergencia (como `com.sh.smart.caller`, marcadores del fabricante o servicios de red celular). Tu teléfono nunca perderá la capacidad de hacer llamadas ni gestionar contactos de forma nativa.

---

## 🚀 Características Principales

- **Universal para Móviles:** Compatible con Android 8.0 hasta Android 14 / 15+ (HiOS, XOS, One UI, HyperOS/MIUI, ColorOS, etc.).
- **100% Reversible y Seguro:** Utiliza `pm disable-user --user 0` en lugar de borrados destructivos de partición. Nunca rompe OTAs ni provoca bootloops.
- **Auditoría y Respaldo Automático:** Genera un archivo `.json` de respaldo fechado con cada paquete desactivado para restaurar en 1 solo comando.
- **Perfiles de Fabricante Incluidos:**
  - 🟢 **Tecno / Infinix / Itel:** HiOS / XOS (Telemetría de ventas, ads y trackers Transsion neutralizados).
  - 🔵 **Xiaomi / Redmi / POCO:** MIUI / HyperOS (Joyose, MSA Ads, Analytics).
  - 🟣 **Samsung:** One UI (Bixby, Samsung Pay bloatware).
  - 🌐 **Meta / Facebook:** Servicios de instalación y rastreo en segundo plano preinstalados en el sistema.

---

## 📦 Requisitos Previos

1. **ADB Platform Tools** instalado en tu PC (Linux, macOS o Windows).
2. **Depuración USB** o **Depuración Inalámbrica (Wireless Debugging)** activada en el móvil:
   - *Ajustes* → *Información del teléfono* → Tocar 7 veces en *Número de compilación*.
   - *Opciones de desarrollador* → Activar *Depuración USB* o *Depuración Inalámbrica*.

---

## 🛠️ Guía Rápida de Uso

### 1. Detectar tu dispositivo
```bash
python3 debloater.py detect
```

### 2. Ejecutar limpieza por perfil
Selecciona el perfil según la marca de tu dispositivo:

```bash
# Para móviles Tecno, Infinix o Itel:
python3 debloater.py debloat --profile tecno_infinix

# Para Xiaomi, Redmi o POCO:
python3 debloater.py debloat --profile xiaomi

# Para Samsung Galaxy:
python3 debloater.py debloat --profile samsung
```

### 3. Reversibilidad (Restaurar en cualquier momento)
Si necesitas reactivar alguna aplicación o devolver el dispositivo a su estado original de fábrica:

```bash
python3 debloater.py restore --file backup_debloat_tecno_infinix_YYYYMMDD_HHMMSS.json
```
O de forma manual por paquete:
```bash
adb shell pm enable <nombre_del_paquete>
```

---

## 🌟 Instalación de Nova Launcher Prime

El repositorio incluye el APK de **Nova Launcher Prime v8.8.6** en la carpeta `apps/`. Puedes instalarlo directamente en el dispositivo conectado mediante:

```bash
python3 debloater.py install-nova
```
O usando ADB clásico:
```bash
adb install -r apps/Nova-Launcher-8.8.6-Prime.apk
```

---

## 🛡️ Lista de Paquetes Protegidos

Esta herramienta **NUNCA** toca los componentes críticos del sistema operativo:
- **Telefonía y Contactos:** Marcadores (`dialer`, `caller`, `telecom`, `contacts`), SMS/MMS y llamadas de emergencia.
- **Framework base:** `android`, `com.google.android.gms`, `com.google.android.gsf`.
- **Hardware y Multimedia:** Drivers y módulos de cámara, audio DTS y pantalla.
- **Seguridad biométrica:** Sensores de huella dactilar (`fpsensor`) y reconocimiento facial.
- **Bajas capas del SoC:** Modems y procesadores base (`com.mediatek.*` / `com.qualcomm.*`).

---

## 📄 Licencia

Distribuido bajo licencia MIT. Desarrollado para mantener la privacidad, rendimiento y control sobre tus propios dispositivos.
