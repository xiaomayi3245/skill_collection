---
name: spring-boot-pro-crud
description: Professional-grade CRUD generation featuring MapStruct for DTO mapping, Java Records, Global Exception Handling, and Data Transfer Objects to avoid Exposing Entities.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
category: backend
tags: [spring-boot, java, crud, mapstruct, dtos, records, exception-handling, pro-level]
version: 1.0.0
---

# Spring Boot Professional CRUD (Nivel Pro)

## Overview

Elevate the standard CRUD API to a professional level by completely decoupling the database layer from the client. This skill implements the **DTO Pattern** using immutable Java Records, automates the mapping process intelligently with **MapStruct**, and controls all error outputs via a **Global Exception Handler** (`@RestControllerAdvice`).

## When to Use

- When building enterprise-ready REST APIs.
- When you need to hide sensitive database fields (like `id`, `createdAt`, `password`) from the API output.
- When validating input data securely without polluting the Entity model.
- When you want to eliminate the "Whitelabel Error Page" and return standardized JSON error messages instead.
- Trigger phrases: **"implement pro level CRUD for [Entity]"**, **"crear CRUD profesional con DTOs y MapStruct"**, **"refactorizar a nivel pro con manejo de excepciones"**.

## Instructions

Follow these steps strictly to implement the Pro CRUD pattern:

### 0. Configuración Inicial (Dependencias y Base de Datos)
Before implementing, verify the standard dependencies in `pom.xml` (`spring-boot-starter-web`, `data-jpa`, `validation`, `lombok`).

**Configuración de Base de Datos (application.properties):**
Inserta la configuración básica de H2 en `src/main/resources/application.properties`:
```properties
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=update
spring.h2.console.enabled=true
```

**⚠️ CRITICO PARA EL AGENTE:** Debes indicarle al usuario que se agregarán nuevas configuraciones y que **DEBE recargar Maven** (Load Maven Changes) al terminar.

Añade la dependencia de MapStruct:
```xml
<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct</artifactId>
    <version>1.5.5.Final</version>
</dependency>
```

**⚠️ MODIFICACIÓN OBLIGATORIA DEL PLUGIN:** Para que MapStruct funcione con Lombok, debes modificar la configuración del `maven-compiler-plugin` en el bloque `<build><plugins>` del `pom.xml`. Debe lucir exactamente así:
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <annotationProcessorPaths>
            <path>
                <groupId>org.mapstruct</groupId>
                <artifactId>mapstruct-processor</artifactId>
                <version>1.5.5.Final</version>
            </path>
            <path>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok</artifactId>
            </path>
            <path>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok-mapstruct-binding</artifactId>
                <version>0.2.0</version>
            </path>
        </annotationProcessorPaths>
    </configuration>
</plugin>
```
*Dile explícitamente al usuario: "Recarga tu proyecto Maven ahora mismo para que MapStruct funcione correctamente".*

### Presentación del Plan (OBLIGATORIO) 🛑
Antes de escribir CUALQUIER código, **MUESTRALE al usuario el siguiente plan de implementación "Bottom-Up"** y espera su aprobación.

**⚠️ REGLA DE DOCUMENTACIÓN EDUCATIVA:** Al escribir el código, DEBES incluir comentarios `Javadoc` detallados en las clases y métodos (especialmente en Service, Controllers y DTOs) explicando el *"por qué"* de las decisiones (ej: por qué se usa un RequestDTO en lugar de la Entidad). El objetivo principal de este código es que el usuario lo ESTUDIE.

**⚠️ REGLA ESTRICTA DE EJECUCIÓN:** Tienes prohibido empezar a programar por las Excepciones o el Controller. Debes programar exactamente en este orden secuencial:
1. Entidad y Repositorio
2. Base de Datos (`application.properties`)
3. Excepciones Globales
4. DTOs
5. Mappers
6. Service
7. Controller
8. Archivo de Pruebas HTTP

Una vez aprobado, ejecuta siguiendo estrictamente este orden:

### 1. Entidad y Repositorio (El Núcleo)
Crea la Entity (`.model`) asegurándote de removerle las validaciones asumiendo que ya pasaron por el DTO (excepto constraints como `@Column(nullable=false, unique=true)`).
Crea el Repository (`.repository`) extendiendo de `JpaRepository`.

### 2. Base de Datos y Propiedades
Asegúrate de configurar la conexión a la base de datos H2 en `application.properties` (ver Paso 0).

### 3. Manejo Global de Errores (Las Reglas de Juego)
Crea las clases en el paquete `.exception`:
- **`ErrorResponse.java`**: Un `record` simple con `(String mensaje, String detalles, LocalDateTime fecha)`.
- **`ResourceNotFoundException.java`**: Extiende de `RuntimeException` para errores "404 Not Found".
- **`GlobalExceptionHandler.java`**: Anotado con `@RestControllerAdvice`. Debe capturar `ResourceNotFoundException` (devuelve 404) y `MethodArgumentNotValidException` (devuelve 400 mapeando los errores de `@Valid`).

### 4. Patrón DTO (Cajas de Entrada y Salida)
Crea el paquete `.dto`:
- **`[Entity]RequestDTO.java`**: Es un `record`. SOLO contiene validaciones (`@NotBlank`, `@Email`, etc.). NO lleva el ID.
- **`[Entity]ResponseDTO.java`**: Es un `record`. SÍ contiene el ID. NO lleva anotaciones de validación.

### 5. El Mapper Automático (El Puente)
Crea la interfaz en el paquete `.mapper`:
```java
@Mapper(componentModel = "spring")
public interface [Entity]Mapper {
    [Entity]ResponseDTO toResponseDTO([Entity] entity);
    
    @Mapping(target = "id", ignore = true)
    [Entity] toEntity([Entity]RequestDTO dto);
    
    @Mapping(target = "id", ignore = true)
    void updateEntity([Entity]RequestDTO dto, @MappingTarget [Entity] entity);
}
```

### 6. Service Layer (El Coordinador)
El Service ya tiene todo para funcionar sin errores de compilación:
- Inyecta tanto el Repository como el Mapper.
- Para **Crear**: usa `mapper.toEntity(dto)`, guarda, e inmediatamente retorna `mapper.toResponseDTO(guardado)`.
- Para **Actualizar**: usa `repository.findById()` (si no, lanza tu `ResourceNotFoundException`), actualiza usando `mapper.updateEntity(dto, entidadExistente)`, guarda y devuelve el `ResponseDTO`.
- La Entidad jamás sale de esta capa.

### 7. Controller (El Despachador Ciego)
- El Controller delega al Service.
- Solo recibe `[Entity]RequestDTO` validado con `@Valid @RequestBody` y solo retorna `[Entity]ResponseDTO`.
- No inyecta Reopositorios ni Mappers.

### 8. Pruebas HTTP (Generación de Endpoints)
Para poder probar inmediatamente, al finalizar el Controller crea un directorio `http` en la raíz del proyecto y genera un archivo `[entity].http` (ej: `cliente.http`) que contenga ejemplos completos de solicitudes (POST, GET, PUT, DELETE) usando la sintaxis de archivos `.http` compatible con IntelliJ IDEA o REST Client de VS Code.

## Mejores Prácticas Integradas
- **Enfoque Educativo:** Todo el código generado incluye Javadocs explicativos para facilitar el estudio de la arquitectura.
- **DTOs como Records**: Menos código basura, más seguridad por ser inmutables.
- **Fail-Fast Validation**: El `GlobalExceptionHandler` ataja la petición mala en el controlador antes de que toque la capa Service.
- **MapStruct > Mapeo Manual**: Evita escribir código "espagueti" al pasar datos `a.setNome(b.getNome())`.
