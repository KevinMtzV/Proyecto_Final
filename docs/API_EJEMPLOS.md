# Ejemplos de uso de la API REST

## Autenticación

La API usa sesiones de Django. Debes iniciar sesión primero en `/accounts/login/` o usar token-based authentication si lo configuras.

Para pruebas desde navegador, inicia sesión normalmente y las cookies de sesión se usarán automáticamente.

## Endpoints de Campañas

### 1. Listar todas las campañas (GET)
```bash
curl -X GET http://localhost:8000/api/v1/campanas/
```

### 2. Ver detalle de una campaña (GET)
```bash
curl -X GET http://localhost:8000/api/v1/campanas/1/
```

### 3. Crear una campaña (POST)
**Requiere autenticación**

```bash
curl -X POST http://localhost:8000/api/v1/campanas/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: TU_TOKEN_CSRF" \
  -b "sessionid=TU_SESSION_ID" \
  -d '{
    "titulo": "Nueva Campaña de Prueba",
    "descripcion": "Esta es una descripción de prueba",
    "categoria": 1,
    "fecha_limite": "2025-12-31",
    "meta_monetaria": 5000.00,
    "estado": "ACT"
  }'
```

### 4. Actualizar campaña completa (PUT)
**Requiere ser el organizador**

```bash
curl -X PUT http://localhost:8000/api/v1/campanas/1/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: TU_TOKEN_CSRF" \
  -b "sessionid=TU_SESSION_ID" \
  -d '{
    "titulo": "Campaña Actualizada",
    "descripcion": "Nueva descripción completa",
    "categoria": 1,
    "fecha_limite": "2025-12-31",
    "meta_monetaria": 10000.00,
    "estado": "ACT"
  }'
```

### 5. Actualizar campo específico (PATCH)
**Requiere ser el organizador**

#### Cambiar solo el título:
```bash
curl -X PATCH http://localhost:8000/api/v1/campanas/1/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: TU_TOKEN_CSRF" \
  -b "sessionid=TU_SESSION_ID" \
  -d '{
    "titulo": "Nuevo Título"
  }'
```

#### Cambiar solo el estado:
```bash
curl -X PATCH http://localhost:8000/api/v1/campanas/1/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: TU_TOKEN_CSRF" \
  -b "sessionid=TU_SESSION_ID" \
  -d '{
    "estado": "COM"
  }'
```

#### Cambiar descripción:
```bash
curl -X PATCH http://localhost:8000/api/v1/campanas/1/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: TU_TOKEN_CSRF" \
  -b "sessionid=TU_SESSION_ID" \
  -d '{
    "descripcion": "Nueva descripción actualizada"
  }'
```

### 6. Eliminar campaña (DELETE)
**Requiere ser el organizador y que no tenga donaciones**

```bash
curl -X DELETE http://localhost:8000/api/v1/campanas/1/ \
  -H "X-CSRFToken: TU_TOKEN_CSRF" \
  -b "sessionid=TU_SESSION_ID"
```

### 7. Ver mis campañas (GET - acción personalizada)
**Requiere autenticación**

```bash
curl -X GET http://localhost:8000/api/v1/campanas/mis-campanas/ \
  -b "sessionid=TU_SESSION_ID"
```

## Endpoints de Donaciones

### 1. Listar donaciones (GET)
```bash
curl -X GET http://localhost:8000/api/v1/donaciones/
```

### 2. Listar donaciones de una campaña específica (GET con filtro)
```bash
curl -X GET "http://localhost:8000/api/v1/donaciones/?campana=1&limit=5"
```

### 3. Crear donación (POST)
**Requiere autenticación**

```bash
curl -X POST http://localhost:8000/api/v1/donaciones/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: TU_TOKEN_CSRF" \
  -b "sessionid=TU_SESSION_ID" \
  -d '{
    "campana": 1,
    "tipo": "MON",
    "monto": 100.00
  }'
```

### 4. Ver mis donaciones (GET - acción personalizada)
**Requiere autenticación**

```bash
curl -X GET http://localhost:8000/api/v1/donaciones/mis-donaciones/ \
  -b "sessionid=TU_SESSION_ID"
```

## Endpoints de Categorías

### 1. Listar categorías (GET)
```bash
curl -X GET http://localhost:8000/api/v1/categorias/
```

### 2. Ver detalle de categoría (GET)
```bash
curl -X GET http://localhost:8000/api/v1/categorias/1/
```

## Códigos de estado HTTP

- **200 OK**: Solicitud exitosa (GET, PATCH, PUT)
- **201 Created**: Recurso creado exitosamente (POST)
- **204 No Content**: Recurso eliminado exitosamente (DELETE)
- **400 Bad Request**: Datos inválidos
- **401 Unauthorized**: Autenticación requerida
- **403 Forbidden**: No tienes permisos (no eres el organizador)
- **404 Not Found**: Recurso no encontrado

## Usar desde JavaScript (Frontend)

```javascript
// Obtener token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Ejemplo PATCH: Actualizar título
async function actualizarTitulo(campanaId, nuevoTitulo) {
    const response = await fetch(`/api/v1/campanas/${campanaId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            titulo: nuevoTitulo
        })
    });
    
    if (response.ok) {
        const data = await response.json();
        console.log('Actualizado:', data);
    } else {
        console.error('Error:', await response.json());
    }
}

// Ejemplo DELETE: Eliminar campaña
async function eliminarCampana(campanaId) {
    const response = await fetch(`/api/v1/campanas/${campanaId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    
    if (response.ok || response.status === 204) {
        console.log('Campaña eliminada');
    } else {
        console.error('Error:', await response.json());
    }
}
```

## Notas importantes

1. **CSRF Token**: Django requiere el token CSRF para POST/PUT/PATCH/DELETE. Obtenerlo de las cookies.
2. **Autenticación**: Usa sesiones de Django o configura DRF TokenAuthentication.
3. **Permisos**: Solo el organizador puede modificar/eliminar sus campañas.
4. **Validación**: No puedes eliminar campañas con donaciones existentes.
5. **Campo protegido**: No puedes cambiar el campo `organizador` en PUT/PATCH.
