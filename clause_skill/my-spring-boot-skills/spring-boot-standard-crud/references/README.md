# Spring Boot Standard CRUD Skill

Esta skill permite generar un CRUD completo, robusto y 100% funcional siguiendo las mejores prácticas estándar de Spring Boot con anotaciones.

## ¿Qué incluye?
- **Modelo (Entity)**: Con Lombok y validaciones de Jakarta (Jakarta Validation).
- **Repositorio**: Interfaz que extiende de `JpaRepository`.
- **Servicio**: Interfaz e implementación con lógica de mapeo explícita para actualizaciones.
- **Controlador**: REST Controller con mapeos estándar y validación de entrada (`@Valid`).
- **Manejo de Errores**: Instrucciones para asegurar una respuesta JSON limpia en caso de errores de validación.

## ¿Cómo usarla?
Solo pide al agente:
- "Implementa un CRUD estándar para [NombreEntidad]"
- "Crea un servicio completo de Spring Boot para [Entidad] con validaciones"

## Estructura generada
La skill sigue una arquitectura de capas simple:
1. `model/` -> Entidad JPA.
2. `repository/` -> Repositorio Spring Data.
3. `service/` -> Capa de negocio.
4. `controller/` -> Endpoints REST.
