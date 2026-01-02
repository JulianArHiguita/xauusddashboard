# XAUUSD Dashboard - Configuración

## Configuración del Backend

1. **Ubicación del Backend**: El backend debe estar ejecutándose antes de iniciar el frontend.

2. **Configurar la URL del API**:
   - Copia el archivo `.env.example` a `.env` en la carpeta `frontend/`
   - Edita `.env` y ajusta `VITE_API_URL` según donde esté tu backend:
     ```
     # Mismo dispositivo (desarrollo local)
     VITE_API_URL=http://localhost:8000
     
     # Otro dispositivo en la misma red (reemplaza con la IP del servidor)
     VITE_API_URL=http://192.168.1.100:8000
     
     # Servidor en Internet (reemplaza con tu dominio)
     VITE_API_URL=https://tu-servidor.com
     ```

3. **Encontrar la IP de tu servidor** (para acceso desde otros dispositivos):
   - Windows: `ipconfig` (busca "IPv4 Address")
   - Linux/Mac: `ifconfig` o `ip addr`

## Instrucciones de Uso

### En el dispositivo que ejecuta el Backend:

1. Abre terminal en `backend/`
2. Ejecuta: `venv\Scripts\uvicorn main:app --host 0.0.0.0 --reload`
   - El parámetro `--host 0.0.0.0` permite conexiones desde otros dispositivos
3. Anota la IP del servidor (ej: 192.168.1.100)

### En cualquier otro dispositivo:

1. En `frontend/.env`, configura:
   ```
   VITE_API_URL=http://192.168.1.100:8000
   ```
   (donde 192.168.1.100 es la IP del servidor)

2. Ejecuta el frontend:
   ```bash
   cd frontend
   npm run dev -- --host
   ```

3. Accede desde el navegador a la URL que muestre Vite

## Notas Importantes

- Asegúrate de que el firewall permita conexiones en el puerto 8000
- Ambos dispositivos deben estar en la misma red WiFi/LAN
- No subas el archivo `.env` a Git (ya está en `.gitignore`)
