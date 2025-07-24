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
