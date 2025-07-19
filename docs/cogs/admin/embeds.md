# 📨 Sistema de Embeds Administrativos

Sistema completo para enviar mensajes oficiales profesionales en formato embed para administradores y moderadores.

## 🎯 Características Principales

### ✨ **Tres tipos de comandos:**
- **Simple**: Embed básico con título y descripción
- **Avanzado**: Personalización completa (color, footer, thumbnail, etc.)
- **Plantillas**: Templates prediseñados para diferentes tipos de mensajes

### 🔒 **Seguridad:**
- Solo administradores y moderadores pueden usar los comandos
- Los comandos no aparecen para usuarios sin permisos
- Todas las respuestas son privadas (ephemeral)
- Log completo de todas las acciones

### 👁️ **Preview:**
- Vista previa antes de enviar
- Prueba diferentes configuraciones
- Confirmación visual del resultado

## 📋 Comandos Disponibles

### 1. **Embed Simple** - Para uso rápido
```bash
/admin embed-simple titulo:"Título del mensaje" descripcion:"Contenido del mensaje" canal:#canal-destino
```

**Ejemplo:**
```bash
/admin embed-simple titulo:"Mantenimiento del Servidor" descripcion:"El servidor estará en mantenimiento el domingo de 2-4 AM"
```

### 2. **Embed Avanzado** - Personalización completa
```bash
/admin embed-avanzado titulo:"Título" descripcion:"Contenido" color:rojo footer:"Footer personalizado" canal:#general autor:"Administración" thumbnail:true
```

**Ejemplo:**
```bash
/admin embed-avanzado titulo:"Nueva Normativa" descripcion:"Se implementan nuevas reglas a partir del lunes" color:#ff0000 footer:"Administración UAIn'T" canal:#anuncios
```

### 3. **Embed con Plantilla** - Templates predefinidos
```bash
/admin embed-plantilla tipo:anuncio titulo:"Título del anuncio" contenido:"Contenido del mensaje" canal:#canal-destino
```

**Ejemplo:**
```bash
/admin embed-plantilla tipo:evento titulo:"Torneo de Programación" contenido:"Inscripciones abiertas hasta el viernes" canal:#eventos
```

### 4. **Vista Previa** - Probar antes de enviar
```bash
/admin embed-preview titulo:"Test" descripcion:"Esto es una prueba" color:azul tipo_plantilla:anuncio
```

### 5. **Ayuda** - Guía completa
```bash
/admin embed-ayuda
```

### 6. **Info de Plantillas** - Ver todas las plantillas
```bash
/admin plantillas-info
```

## 📋 Plantillas Disponibles

| Plantilla | Emoji | Color | Uso Recomendado |
|-----------|-------|--------|-----------------|
| **anuncio** | 📢 | Azul | Comunicados oficiales, noticias importantes |
| **reglas** | 📋 | Rojo | Normativas, reglas del servidor |
| **informacion** | ℹ️ | Verde | Guías, tutoriales, información general |
| **aviso** | ⚠️ | Naranja | Advertencias, cambios importantes |
| **evento** | 🎉 | Morado | Actividades, concursos, eventos |
| **bienvenida** | 👋 | Dorado | Mensajes de bienvenida, presentaciones |

## 🎨 Colores Disponibles

### **Colores por nombre:**
- `rojo`, `verde`, `azul`, `amarillo`
- `naranja`, `morado`, `rosa`, `cyan`
- `dorado`, `gris`, `negro`, `blanco`

### **Códigos hexadecimales:**
- `#ff0000` (rojo)
- `#00ff00` (verde)
- `#0000ff` (azul)
- `#ffaa00` (naranja)
- Cualquier código hex válido

## 💡 Ejemplos de Uso Práctico

### **Anuncio de Evento:**
```bash
/admin embed-plantilla tipo:evento titulo:"🎓 Semana de la Informática" contenido:"Del 15 al 19 de abril. Charlas, talleres y competencias. ¡No te lo pierdas!" canal:#anuncios
```

### **Reglas del Servidor:**
```bash
/admin embed-plantilla tipo:reglas titulo:"Normas del Canal de Voz" contenido:"1. Respeto mutuo\n2. No spam de audio\n3. Usar push-to-talk si hay ruido\n4. No música sin permiso" canal:#reglas
```

### **Información Académica:**
```bash
/admin embed-avanzado titulo:"📚 Horarios de Consulta" descripcion:"**Programación I:** Lunes 14-16h\n**Base de Datos:** Miércoles 10-12h\n**Redes:** Viernes 16-18h" color:verde footer:"Profesores disponibles en sus horarios" canal:#academico
```

### **Aviso Importante:**
```bash
/admin embed-plantilla tipo:aviso titulo:"Cambio en el Sistema de Roles" contenido:"A partir del lunes, los roles se asignarán automáticamente. Revisa #guia-roles para más información." canal:#anuncios
```

### **Bienvenida Personalizada:**
```bash
/admin embed-avanzado titulo:"👋 ¡Bienvenido a Informática UAIn'T!" descripcion:"Hola **@nuevo-miembro**, nos alegra tenerte aquí.\n\n📋 Lee #reglas\n🎯 Escoge tus roles en #roles\n💬 Preséntate en #presentaciones" color:dorado footer:"¡Esperamos que disfrutes tu estadía!" canal:#bienvenida
```

## 🔧 Configuración e Instalación

### **1. Crear el directorio:**
```bash
mkdir -p src/bot/cogs/admin
```

### **2. Crear archivo:**
Guarda el código como: `src/bot/cogs/admin/embeds.py`

### **3. Crear archivos init:**
```python
# src/bot/cogs/admin/__init__.py
"""
Comandos administrativos
"""
```

### **4. Actualizar bot.py:**
Agrega a la lista de cogs:
```python
"cogs.admin.embeds",  # Sistema de embeds administrativos
```

### **5. Configurar permisos:**
Los comandos requieren uno de estos permisos:
- **Administrador** del servidor
- **Gestionar Mensajes** de Discord
- Rol configurado en `ADMIN_ROLE_IDS` o `MOD_ROLE_IDS`

## 🛡️ Permisos y Seguridad

### **¿Quién puede usar los comandos?**
- 👑 **Administradores** del servidor
- 🔧 **Usuarios con "Gestionar Mensajes"**
- 📋 **Roles configurados** en el archivo `.env`

### **Visibilidad:**
- ❌ **Usuarios sin permisos**: No ven los comandos
- ✅ **Usuarios autorizados**: Ven todos los comandos del grupo `/admin`
- 👁️ **Respuestas privadas**: Solo quien ejecuta ve la confirmación

### **Logs de seguridad:**
Todas las acciones se registran en los logs del bot:
```
📨 Embed enviado por Juan (123456789) en #anuncios: 'Nuevo Evento' (Tipo: plantilla-evento)
```

## 🎯 Casos de Uso Recomendados

### **Para Administración:**
- Anuncios oficiales del servidor
- Cambios en normativas
- Comunicados importantes
- Información académica

### **Para Moderación:**
- Avisos de mantenimiento
- Recordatorios de reglas
- Eventos de la comunidad
- Mensajes de bienvenida

### **Para Eventos:**
- Convocatorias a concursos
- Información de actividades
- Resultados de competencias
- Calendarios académicos

## 🔍 Solución de Problemas

### **Los comandos no aparecen:**
1. Verificar permisos del usuario
2. Asegurar que el cog esté cargado
3. Reiniciar el bot si es necesario

### **Error al enviar embed:**
1. Verificar permisos del bot en el canal
2. Asegurar que el canal existe
3. Verificar que el bot no esté silenciado

### **Color no funciona:**
1. Usar nombres válidos: `rojo`, `azul`, etc.
2. Para hex, incluir `#`: `#ff0000`
3. Verificar que el código hex sea válido

## 🚀 Próximas Funcionalidades

- **Campos personalizados** en embeds
- **Imágenes adjuntas** en embeds
- **Programación de envíos** (envío automático)
- **Plantillas personalizadas** por servidor
- **Embeds con botones** interactivos

---

*¿Necesitas ayuda? Usa `/admin embed-ayuda` o contacta a los administradores.*