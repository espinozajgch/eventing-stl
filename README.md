![sport data campus](assets/images/ucam_sdc.png)

## 📊 Comparación de Proveedores en Fútbol

Este proyecto forma parte del trabajo final del Máster en Big Data aplicado al fútbol (PFM), y tiene como objetivo comparar la calidad, cobertura y aplicabilidad de los datos de eventos futbolísticos proporcionados por **Opta**, **StatsBomb** y **Wyscout**, utilizando el modelo de estandarización **SPADL**.

### 🧠 Funcionalidades

La aplicación desarrollada en **Streamlit** permite:

- 🔍 Selección interactiva del proveedor y tipo de acción SPADL.
- ⚽ Visualización geoespacial de acciones:
  - Mapa de calor.
  - Mapa de eventos.
- 📈 Consulta de métricas generales por acción.
- 🧭 Exploración del comportamiento de los datos en el campo por proveedor.

---

### 📁 Estructura del proyecto

- **app/**: Archivo principal de la app Streamlit.
- **assets/**: Logotipos e imágenes usadas en la interfaz.
- **data/**: Contiene los archivos originales de eventos (JSON/XML) por proveedor.
- **pages/**: Módulos Streamlit individuales (interfaz multipágina).
- **converters/**: Conversores personalizados (`OptaConverter`, `StatsBombConverter`, `WyscoutConverter`).
- **utils/**:  Funciones auxiliares y gráficas personalizadas.

---

### 📋 Metodología

Se ha seguido una combinación entre **CRISP-DM** y **evaluación de fiabilidad de datos**. Cada evento se convierte al formato SPADL, que define 21 tipos de acciones estándar. Los datos se normalizan, limpian y analizan estadísticamente para evaluar:

- Cobertura de eventos.
- Distribución y frecuencia por tipo de acción.
- Coherencia espacial y granularidad temporal.
- Aplicabilidad en análisis de rendimiento y scouting.

---

### ▶️ Cómo ejecutar

1. Instala las dependencias:

```bash
pip install -r requirements.txt
```
2. Ejecuta la aplicación:

```bash
streamlit run app.py
```

---

### Contribución
Para colaborar en el proyecto, sigue las mejores prácticas de Git y envía **pull requests** con mejoras o nuevas funcionalidades.
