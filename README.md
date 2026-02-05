# 💰 MisGastos - Control Financiero Personal

¡Bienvenido a **MisGastos**! Esta aplicación web ha sido diseñada para gestionar tus finanzas de forma visual, sencilla y personalizada. Olvídate de cálculos automáticos que no entiendes: aquí tú tienes el control total.


## 🖥️ ¿Qué puedes hacer en esta App?

La aplicación está organizada en cuatro secciones principales:

* **🏠 Dashboard (Inicio):** El centro de mando. Aquí verás gráficos anuales comparativos entre lo que ganas y lo que gastas, además del estado de tus "Huchas" de ahorro.
* **📈 Ingresos:** Registra tus entradas de dinero. Al igual que en gastos, puedes visualizar cuánto has ganado cada semana del mes.
* **💸 Gastos:** La sección más detallada. 
    * **Categorías y Subcategorías:** Clasifica tus gastos (Ocio, Personal, Suscripciones, etc.).
    * **Control Semanal Manual:** Cuando añades un gasto, tú eliges en qué semana del gráfico quieres que aparezca (Semana 1 a 5).
    * **Panel Admin:** Puedes añadir nuevas categorías principales directamente desde la interfaz.
* **🐷 Huchas:** Gestiona tus ahorros específicos para objetivos concretos.


## ⚙️ Instalación 

Si quieres ejecutar esta aplicación en tu ordenador, sigue estos pasos en la terminal:

1. **Clonar/Descargar el proyecto** y entrar en la carpeta:
   ```bash
   cd misgastos

2. **Crear y activar el entorno virtual:** 
    python -m venv .venv
    # En Windows:
    .\.venv\Scripts\activate
    # En Mac/Linux:
    source .venv/bin/activate

3. **Instalar las librerías necesarias:**
    Al crear el entorno virtual, seleccionar requirements.txt para la instalación de librerías.
    Si no te sale por defecto: pip install -r requirements.txt

4. **Ejecutar la aplicación**:
    python run.py


##🗄️ **Guía de la Base de Datos (Flask-Migrate)**
Este proyecto usa un sistema de Migraciones. Esto es fundamental para que, si el código cambia (añades columnas o tablas), los datos que ya has metido no se borren nunca.

¿Has hecho cambios en models.py?
Si añades un nuevo campo (ej: "Notas" o "Método de Pago"), sigue estos pasos para actualizar la base de datos sin perder nada:

1. **Genera el archivo de migración:**
    flask db migrate -m "Descripción del cambio"

2. **Aplicar el cambio a la base de datos real:**
    flask db upgrade