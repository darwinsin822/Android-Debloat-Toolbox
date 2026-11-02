# 📱 Android Universal Debloat & Optimization Toolbox

Herramienta universal de código abierto diseñada para auditar, limpiar y deshabilitar bloatware, adware y telemetría de fábrica en cualquier dispositivo Android (móviles, tablets y Fire TV Stick), con **garantía de reversibilidad total al 100%**.

Incluye el instalador optimizado de **Nova Launcher Prime (v8.8.6)** para sustituir launchers pesados del fabricante.

---

## 🚀 Características Principales

- **Universal:** Compatible con Android 8.0 hasta Android 14 / 15+ (incluyendo Fire OS, HiOS, One UI, HyperOS/MIUI, ColorOS, etc.).
- **100% Reversible y Seguro:** Utiliza `pm disable-user --user 0` en lugar de borrados destructivos de partición. Nunca rompe OTAs ni provoca bootloops.
- **Auditoría y Respaldo Automático:** Genera un archivo `.json` de respaldo fechado con cada paquete desactivado para restaurar en 1 solo comando.
- **Perfiles de Fabricante Incluidos:**
  - 🟢 **Tecno / Infinix / Itel:** HiOS / XOS (46 paquetes de telemetría agresiva Transsion neutralizados).
  - 🔥 **Amazon Fire TV:** Fire OS 7 y 8 (publicidad de pantalla de inicio y telemetría KSO desactivados sin tocar Prime Video ni Luna).
  - 🔵 **Xiaomi / Redmi / POCO:** MIUI / HyperOS (Joyose, MSA Ads, Analytics).
  - 🟣 **Samsung:** One UI (Bixby, Samsung Pay bloatware).
  - 🌐 **Meta / Facebook:** Servicios de instalación y rastreo en segundo plano preinstalados en el sistema.

---

## 📦 Requisitos Previos

1. **ADB Platform Tools** instalado en tu PC (Linux, macOS o Windows).
2. **Depuración USB** o **Depuración Inalámbrica (Wireless Debugging)** activada en el móvil/dispositivo:
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

# Para Amazon Fire TV Stick / Fire Tablets:
python3 debloater.py debloat --profile amazon_firetv

# Para Xiaomi, Redmi o POCO:
python3 debloater.py debloat --profile xiaomi

# Para Samsung Galaxy:
python3 debloater.py debloat --profile samsung
```

### 3. Reversibilidad (Restaurar en cualquier momento)
Si necesitas reactivar alguna aplicación o devolver el dispositivo a su estado original de fábrica:

```bash
python3 debloater.py restore --file backup_debloat_tecno_infinix_20261101_205653.json
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

## 🛡️ Lista de Paquetes Protegidos (Regla de Oro)

Esta herramienta **NUNCA** toca los componentes críticos del sistema operativo:
- Framework base (`android`, `com.google.android.gms`, `com.google.android.gsf`).
- Drivers y módulos de cámara, audio DTS y pantalla.
- Sensores biométricos (huella dactilar `fpsensor` y reconocimiento facial).
- Modems, telefonía y llamadas de emergencia (`com.mediatek.*`).

---

## 📄 Licencia

Distribuido bajo licencia MIT. Desarrollado para mantener la privacidad, rendimiento y control sobre tus propios dispositivos.
