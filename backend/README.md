# Backend

Arquitectura: React (Frontend) + Next.js (Framework) + FastAPI + Supabase

Instalación Node:
  cd backend-node
  npm install
  npm run dev

Instalación FastAPI:
  cd backend-python
  pip install -r requirements.txt
  uvicorn main:app --reload

© 2025 Francisco J. Aucar

---

### 📄 ¿Cómo acceder a los CSV desde el frontend?

- Si usas React/Vite/Next.js, puedes hacer fetch a `/data/rentabilidad.csv`.
- Ejemplo:
  ```js
  fetch('/data/rentabilidad.csv')
    .then(res => res.text())
    .then(data => {
      // Parsear CSV y usar los datos
    });
  ```

---

### ✅ Resumen

- Crea la carpeta: `frontend/public/data/`
- Coloca ahí todos los archivos `.csv` que vayas a usar.
- Accede a ellos desde el frontend usando rutas relativas (`/data/archivo.csv`).

---

---

## **Checklist para dejar el flujo local listo**

### 1. **Backend FastAPI**
- El backend debe estar corriendo en `http://localhost:8000`.
- El archivo `datos.csv` debe estar en la carpeta `/backend`.
- Puedes iniciar el backend con:
  ```powershell
  cd backend
  venv\Scripts\activate
  uvicorn main:app --reload
  ```

### 2. **Frontend Next.js**
- El frontend debe estar corriendo en `http://localhost:3000`.
- El fetch de Axios en el frontend apunta a `http://localhost:8000/pacientes`.
- Puedes iniciar el frontend con:
  ```powershell
  cd frontend
  npm install
  npm run dev
  ```

### 3. **Prueba del flujo**
- Inicia primero el backend, luego el frontend.
- Accede a [http://localhost:3000](http://localhost:3000) y verifica que:
  - Se muestra la tabla de pacientes.
  - Todos los gráficos y KPIs aparecen correctamente.
  - No hay errores en consola.

### 4. **Documentación**
- El archivo `README.md` ya tiene instrucciones claras para uso local y deploy.
- El workflow de GitHub Actions para Vercel está listo para cuando quieras desplegar.

### 5. **Variables de entorno (opcional)**
- Si en el futuro cambias la URL del backend, puedes usar una variable de entorno en Next.js:
  - Crea un archivo `.env.local` en `/frontend` con:
    ```
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```
  - Cambia el fetch de Axios a:
    ```js
    axios.get(`${process.env.NEXT_PUBLIC_API_URL}/pacientes`)
    ```

---

## **¿Qué sigue?**
- Haz una prueba local de todo el flujo.
- Si todo funciona, ¡ya tienes tu stack listo para producción!
- Cuando quieras desplegar, solo tendrás que cambiar la URL del backend en el frontend y seguir las instrucciones del README.

¡Perfecto! El backend FastAPI está corriendo correctamente en `http://127.0.0.1:8000` y responde a las peticiones.

Ahora, para asegurarnos de que el frontend pueda conectarse correctamente:

---

### **1. Prueba directa del endpoint**
Abre en tu navegador:  
[http://127.0.0.1:8000/pacientes](http://127.0.0.1:8000/pacientes)

- Si ves un JSON con los datos de pacientes, el backend está funcionando bien.
- Si ves un error, copia el mensaje aquí.

---

### **2. Cambia la URL en el frontend**
Edita la línea de Axios en `frontend/src/app/page.tsx` para que apunte a `127.0.0.1`:

```js
axios.get('http://127.0.0.1:8000/pacientes')
```

Guarda el archivo y recarga la página del frontend ([http://localhost:3000](http://localhost:3000)).

---

### **3. Verifica la consola del navegador**
Si sigue sin mostrar datos, abre la consola de tu navegador (F12 > pestaña "Console" o "Red/Network") y revisa si hay algún error de red o CORS.

---

**Haz estos pasos y dime:**
- ¿Ves los datos en el navegador al acceder a `/pacientes`?
- ¿Se soluciona el problema al cambiar la URL en el frontend?
- ¿Aparece algún error en la consola del navegador?

¡Con esto encontraremos la causa y lo solucionamos!


---

## **¿Por qué el frontend sigue sin mostrar los datos?**

Si el backend responde bien, pero el frontend muestra “No se pudo obtener los datos del backend”, el problema está en la conexión entre ambos.  
Vamos a revisar los últimos puntos críticos:

---

### 1. **Verifica la consola del navegador**
- Abre la consola de tu navegador (F12 > pestaña "Console" o "Red/Network").
- Recarga la página del frontend.
- Busca errores relacionados con la petición a `/pacientes` (CORS, 404, 500, ECONNREFUSED, etc.).
- Copia aquí el mensaje exacto del error.

---

### 2. **Verifica la consola del backend**
- Cuando recargas el frontend, ¿aparece una línea como esta?
  ```
  INFO:     127.0.0.1:XXXXX - "GET /pacientes HTTP/1.1" 200 OK
  ```
- Si no aparece, el frontend no está haciendo la petición correctamente.

---

### 3. **Verifica la URL en el frontend**
- Asegúrate de que la línea de Axios en `frontend/src/app/page.tsx` sea exactamente:
  ```js
  axios.get('http://127.0.0.1:8000/pacientes')
  ```
- Guarda y recarga el frontend.

---

### 4. **Verifica si hay un proxy o variable de entorno**
- Si usas una variable de entorno para la URL, asegúrate de que esté bien configurada en `.env.local` y que el código la use correctamente.

---

**Por favor, responde:**
- ¿Qué error aparece en la consola del navegador al recargar el frontend?
- ¿Aparece la petición en la consola del backend cuando recargas el frontend?
- ¿La URL de Axios es exactamente la que corresponde?

¡Con esa información, encontraremos el último detalle y lo dejamos funcionando!

