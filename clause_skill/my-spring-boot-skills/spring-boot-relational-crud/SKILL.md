---
name: spring-boot-relational-crud
description: Relational CRUD with JPA relationships (OneToMany / ManyToOne), nested DTOs, MapStruct with uses, and manual FK assignment in the Service layer.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
category: backend
tags:
  [
    spring-boot,
    java,
    crud,
    jpa-relationships,
    one-to-many,
    many-to-one,
    mapstruct,
    dtos,
    nested-dtos,
  ]
version: 1.0.0
---

# Spring Boot Relational CRUD (Nivel Relacional)

## Overview

Extiende el patrón Pro CRUD para manejar **relaciones entre entidades**. Esta skill enseña a construir dos entidades con relación `@OneToMany` / `@ManyToOne`, mapear DTOs anidados con MapStruct (`uses`), y conectar las relaciones manualmente en el Service con `setAutor()`. El proyecto de referencia es un CRUD completo de **Autores y Libros**.

## When to Use

- Cuando necesitas crear un CRUD con **dos o más entidades relacionadas** (por ejemplo: Autor → Libros, Departamento → Empleados, Categoría → Productos).
- Cuando quieres practicar relaciones JPA de forma clara y directa.
- Cuando tus DTOs de respuesta deben incluir **listas anidadas** de otras entidades.
- Trigger phrases: **"crear CRUD con relaciones JPA"**, **"implementar OneToMany entre [Entidad1] y [Entidad2]"**, **"CRUD relacional con DTOs anidados"**.

## Prerequisites

Esta skill requiere TODO lo que usa el Pro CRUD (MapStruct, Lombok, Validation, JPA, H2), más el conocimiento previo del patrón DTO y el `GlobalExceptionHandler`. **Se recomienda haber completado el Pro CRUD antes de usar esta skill.**

## Instructions

Follow these steps strictly. This skill creates TWO related entities simultaneously.

**⚠️ CONVENCIÓN DE NOMBRES:** A lo largo de esta guía, `[Padre]` representa la entidad "uno" (ej: Autor, Departamento, Categoría) y `[Hijo]` representa la entidad "muchos" (ej: Libro, Empleado, Producto).

**⚠️ REGLA DE DOCUMENTACIÓN EDUCATIVA:** Al escribir el código, DEBES incluir comentarios `Javadoc` concisos en las clases explicando el _"por qué"_ de las decisiones (ej: por qué se ignora `autor` en el LibroMapper, por qué no incluimos Autor dentro de LibroResponseDTO).

**⚠️ REGLA ESTRICTA DE EJECUCIÓN:** Debes programar exactamente en este orden secuencial:

1. Entidades y Repositorios (ambas)
2. Base de Datos (`application.properties`)
3. DTOs (los 4: Request y Response de cada entidad)
4. Mappers (los 2, con `uses` para conectarlos)
5. Excepciones Globales
6. Services (interfaces e implementaciones)
7. Controllers (los 2)
8. Archivos de Pruebas HTTP

### Presentación del Plan (OBLIGATORIO) 🛑

Antes de escribir CUALQUIER código, **MUESTRALE al usuario el siguiente plan** y espera su aprobación.

### 0. Configuración Inicial

Verifica las dependencias estándar en `pom.xml` (`spring-boot-starter-web`, `data-jpa`, `validation`, `lombok`, `mapstruct`) y la configuración del `maven-compiler-plugin` con los `annotationProcessorPaths` para Lombok y MapStruct.

Configura la base de datos H2 en `application.properties`:

```properties
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=update
spring.h2.console.enabled=true
```

### 1. Entidades y Repositorios (Las Dos Tablas)

Crea AMBAS entidades en el paquete `.model` y sus repositorios en `.repository`.

**Entidad Padre `[Padre].java`:**

```java
/**
 * Entidad JPA que representa un [Padre].
 * Un [padre] puede tener muchos [hijos] (relación OneToMany).
 * cascade = ALL: las operaciones sobre el [padre] se propagan a sus [hijos].
 * orphanRemoval = true: si un [hijo] se desasocia, se elimina de la BD.
 */
@Entity
@Getter @Setter @AllArgsConstructor @NoArgsConstructor
@Table(name = "[padres]")
public class [Padre] {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // ... campos propios del padre ...

    @OneToMany(mappedBy = "[padre]", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<[Hijo]> [hijos] = new ArrayList<>();
}
```

**Entidad Hijo `[Hijo].java`:**

```java
/**
 * Entidad JPA que representa un [Hijo].
 * Cada [hijo] pertenece a un único [padre] (relación ManyToOne).
 * La columna [padre]_id es la FK que conecta con la tabla [padres].
 */
@Entity
@Getter @Setter @AllArgsConstructor @NoArgsConstructor
@Table(name = "[hijos]")
public class [Hijo] {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // ... campos propios del hijo ...

    @ManyToOne
    @JoinColumn(name = "[padre]_id", nullable = false)
    private [Padre] [padre];
}
```

**Repositorios:** Ambos extienden `JpaRepository<[Entity], Long>`.

### 2. DTOs (Las 4 Cajas)

Crea 4 DTOs como `record` en el paquete `.dto`:

- **`[Padre]RequestDTO`**: Solo los campos del padre con validaciones (`@NotBlank`, etc.). SIN id, SIN lista de hijos.
- **`[Padre]ResponseDTO`**: Con `id` + campos del padre + `List<[Hijo]ResponseDTO> [hijos]`. ← **Este es el DTO anidado.**
- **`[Hijo]RequestDTO`**: Campos del hijo con validaciones + `Long [padre]Id`. ← **No el objeto completo, solo el ID.**
- **`[Hijo]ResponseDTO`**: Con `id` + campos del hijo. **SIN incluir el objeto [Padre]** para evitar recursión infinita en el JSON.

**⚠️ REGLA CRÍTICA:** El `[Hijo]ResponseDTO` NUNCA debe contener un campo de tipo `[Padre]` o `[Padre]ResponseDTO`. Esto causaría recursión infinita: Autor → Libros → Autor → Libros → ...

### 3. Mappers (El Puente Doble)

Crea 2 mappers en el paquete `.mapper`:

**`[Hijo]Mapper.java`** (SE CREA PRIMERO porque el Padre lo necesita):

```java
/**
 * Ignora "autor" en toEntity y updateEntity porque el DTO
 * solo trae autorId (Long), no el objeto completo.
 * El Service lo asigna manualmente con setAutor().
 */
@Mapper(componentModel = "spring")
public interface [Hijo]Mapper {
    [Hijo]ResponseDTO toResponseDTO([Hijo] entity);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "[padre]", ignore = true)  // ← CRÍTICO
    [Hijo] toEntity([Hijo]RequestDTO dto);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "[padre]", ignore = true)  // ← CRÍTICO
    void updateEntity([Hijo]RequestDTO dto, @MappingTarget [Hijo] entity);
}
```

**`[Padre]Mapper.java`:**

```java
/**
 * Usa [Hijo]Mapper para convertir automáticamente la lista de [hijos].
 * Ignora "libros" en toEntity y updateEntity porque el RequestDTO no trae hijos.
 */
@Mapper(componentModel = "spring", uses = {[Hijo]Mapper.class})  // ← CLAVE
public interface [Padre]Mapper {
    [Padre]ResponseDTO toResponseDTO([Padre] entity);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "[hijos]", ignore = true)
    [Padre] toEntity([Padre]RequestDTO dto);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "[hijos]", ignore = true)
    void updateEntity([Padre]RequestDTO dto, @MappingTarget [Padre] entity);
}
```

**⚠️ CONCEPTOS CLAVE PARA EL USUARIO:**

- `uses = {[Hijo]Mapper.class}`: Le dice a MapStruct que cuando necesite convertir un `[Hijo]` → `[Hijo]ResponseDTO`, delegue al `[Hijo]Mapper`.
- `ignore = "[padre]"`: El DTO trae `[padre]Id` (Long), pero la entidad espera un objeto `[Padre]`. MapStruct no sabe convertir uno en otro, así que lo ignoramos y lo asignamos manualmente en el Service.

### 4. Manejo Global de Errores

Crea las clases en el paquete `.exception`:

- **`ErrorResponse.java`**: Un `record` con `(String error, String detalle, LocalDateTime fecha)`.
- **`ResourceNotFoundException.java`**: Extiende `RuntimeException` para errores 404.
- **`GlobalExceptionHandler.java`**: Con `@RestControllerAdvice`. Captura:
  - `ResourceNotFoundException` → 404 Not Found
  - `MethodArgumentNotValidException` → 400 Bad Request (mapa de errores por campo)
  - `Exception` genérica → 500 Internal Server Error

### 5. Service Layer (La Conexión de la Relación) ⭐

Aquí está **el corazón de esta skill**: cómo se conecta la relación en el Service.

**`I[Padre]Service` + `[Padre]ServiceImpl`**: CRUD estándar igual que el Pro CRUD. Nada especial.

**`I[Hijo]Service` + `[Hijo]ServiceImpl`**:

```java
/**
 * Al crear un [hijo], busca al [Padre] por [padre]Id y lo asigna con set[Padre]().
 * Esta es la pieza clave que conecta la relación ManyToOne en el Service.
 */
@Service
@RequiredArgsConstructor
public class [Hijo]ServiceImpl implements I[Hijo]Service {
    private final [Hijo]Repository [hijo]Repo;
    private final [Hijo]Mapper [hijo]Mapper;
    private final [Padre]Repository [padre]Repo;  // ← Inyecta el repo del PADRE

    @Override
    public [Hijo]ResponseDTO crear[Hijo]([Hijo]RequestDTO dto) {
        // 1. Buscar al padre por ID (si no existe, lanzar 404)
        [Padre] [padre] = [padre]Repo.findById(dto.[padre]Id())
            .orElseThrow(() -> new ResourceNotFoundException("[Padre] no encontrado con ID: " + dto.[padre]Id()));

        // 2. Convertir el DTO a entidad (sin el padre, MapStruct lo ignoró)
        [Hijo] nuevo[Hijo] = [hijo]Mapper.toEntity(dto);

        // 3. ⭐ ASIGNAR LA RELACIÓN MANUALMENTE
        nuevo[Hijo].set[Padre]([padre]);

        // 4. Guardar y retornar como DTO
        [Hijo] [hijo]Guardado = [hijo]Repo.save(nuevo[Hijo]);
        return [hijo]Mapper.toResponseDTO([hijo]Guardado);
    }
    // ... demás métodos CRUD estándar ...
}
```

**⚠️ EXPLICACIÓN CLAVE PARA EL USUARIO:** La línea `nuevo[Hijo].set[Padre]([padre])` es toda la magia. Sin esta línea, la columna FK `[padre]_id` quedaría null y la BD lanzaría error. El flujo es:

1. El cliente envía `[padre]Id: 1` en el JSON
2. El Service busca al `[Padre]` con ID 1 en la BD
3. Si existe, se lo asigna al `[Hijo]` con `set[Padre]()`
4. JPA automáticamente llena la columna FK al hacer `save()`

### 6. Controllers

Crea 2 controllers:

- **`[Padre]Controller`**: `@RequestMapping("/api/[padres]")` — CRUD estándar con `@Valid`.
- **`[Hijo]Controller`**: `@RequestMapping("/api/[hijos]")` — CRUD estándar con `@Valid`.

Ambos siguen el mismo patrón del Pro CRUD. Los Controllers no saben nada de relaciones; eso lo maneja el Service.

### 7. Pruebas HTTP

Crea una carpeta `http/` en la raíz del proyecto con 2 archivos:

- **`[padres].http`**: CRUD completo del padre + pruebas de error (404, validaciones).
- **`[hijos].http`**: CRUD completo del hijo + prueba de autor inexistente (404) + **prueba estrella**: `GET /api/[padres]/1` debe mostrar al padre con sus hijos anidados en el JSON.

**⚠️ ORDEN DE EJECUCIÓN obligatorio:**

1. Primero crear los padres
2. Luego crear los hijos (necesitan el `[padre]Id`)
3. Finalmente, consultar un padre para ver los hijos anidados

## Mejores Prácticas Integradas

- **Enfoque Educativo:** Todo el código incluye Javadocs concisos que explican el "por qué" de cada decisión.
- **Evitar Recursión Infinita:** El `[Hijo]ResponseDTO` NUNCA contiene al `[Padre]`. La relación se ve solo desde el lado del padre.
- **FK Manual en Service:** La relación `set[Padre]()` se asigna en el Service, no en el Mapper. MapStruct no sabe convertir un `Long` en un objeto JPA.
- **Mapper con `uses`:** El `[Padre]Mapper` delega al `[Hijo]Mapper` para convertir listas automáticamente.
- **DRY con método helper:** Un método privado `buscar[Entity]PorId()` centraliza la búsqueda con manejo de 404.
