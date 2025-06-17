# 💳 Sistema Bancario

Sistema web desarrollado con **Django** para la gestión de operaciones bancarias básicas como creación de cuentas, envío de transacciones, auditoría y administración de usuarios. Diseñado para simular el comportamiento de una plataforma bancaria real.

---

## 📚 Tabla de Contenidos

- [🎯 Objetivo](#-objetivo)
- [🚀 Funcionalidades Principales](#-funcionalidades-principales)
- [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [⚙️ Instalación y Ejecución](#️-instalación-y-ejecución)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)

---

## 🎯 Objetivo

Este proyecto tiene como propósito simular un sistema bancario básico que permita registrar usuarios, gestionar sus cuentas, realizar transacciones entre ellas y mantener un historial auditable de todas las operaciones.

---

## 🚀 Funcionalidades Principales

- 🧑 Registro y autenticación de usuarios
- 💼 Creación y gestión de cuentas bancarias
- 💸 Transferencias entre cuentas
- 📬 Gestión de solicitudes (autorizaciones, revisiones)
- 📜 Auditoría de eventos y operaciones del sistema
- 📚 Implementación de estructuras de datos clásicas (pila, cola, árbol binario, lista enlazada)

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **Framework:** Django
- **Base de datos:** PostgreSQL 
- **Estilos:** Bootstrap
- **Otros:** 
  - Django Admin
  - Django ORM
  - Virtualenv

---

## ⚙️ Instalación y Ejecución

Sigue estos pasos para correr el proyecto localmente:

### 1. Clona el repositorio

```bash
git clone https://github.com/syderkkk/sistema-bancario.git
cd sistema-bancario
```
### 2. Crea un entorno virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecuta las migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crea un superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 6. Ejecuta el servidor

```bash
python manage.py runserver
```

### 📁 Estructura del Proyecto
```text
sistema-bancario/
├── auditoria/         # Módulo de auditoría de operaciones
├── cuentas/           # Lógica para cuentas bancarias
├── solicitudes/       # Gestión de solicitudes entre usuarios/cuentas
├── transacciones/     # Envío y recepción de dinero
├── usuarios/          # Registro y autenticación de usuarios
├── utils/             # Implementaciones de estructuras de datos
├── sistema_bancario/  # Configuración global del proyecto Django
├── manage.py          # Script de gestión del proyecto
└── requirements.txt   # Lista de dependencias
```