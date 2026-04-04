---
name: spring-boot-standard-crud
description: Highly functional, annotation-driven CRUD pattern for Spring Boot. Includes JPA persistence, Jakarta validation, global error handling, and unit testing.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
category: backend
tags: [spring-boot, java, crud, jpa, validation, rest-api, quick-start]
version: 1.0.0
---

# Spring Boot Standard CRUD

## Overview

Deliver 100% functional, production-ready CRUD services using standard Spring Boot annotations. This skill omits the complexity of DDD-adapters in favor of a direct, layered architecture (Controller -> Service -> Repository -> Model) with centralized validation and robust error handling.

## When to Use

- Quickly scaffold a functional REST API for a new or existing entity.
- Implement standard CRUD operations (List, Find, Create, Update, Delete) with input validation.
- Ensure consistent error responses across the API using a Global Exception Handler.
- Trigger phrases: **"implement standard CRUD for [Entity]"**, **"crear un CRUD funcional para [Entidad]"**, **"implementar servicios Spring Boot con anotaciones"**, **"necesito un CRUD completo con validaciones y manejo de errores"**.

## Instructions

Follow these steps to implement a complete and functional CRUD:

### 0. Dependency Verification
Before implementing, verify that the `pom.xml` contains:
- `spring-boot-starter-web`
- `spring-boot-starter-data-jpa`
- `h2` (runtime scope)
- `lombok` (optional: true)
- `spring-boot-starter-validation`
- `spring-boot-devtools` (optional/runtime scope)
If any are missing, notify the user or suggest adding them.

### 1. Model (Entity) Configuration
Create the entity in the `.model` package.
- Use `@Entity` and `@Table`.
- Use Lombok `@Data`, `@NoArgsConstructor`, and `@AllArgsConstructor`.
- Apply `jakarta.validation.constraints` (e.g., `@NotBlank`, `@Positive`, `@Email`) directly on fields.
- Set `@Column(nullable = false)` where appropriate.

### 2. Repository Interface
Create the repository in the `.repository` package.
- Extend `JpaRepository<Entity, Long>`.
- Keep it a simple interface.

### 3. Service Layer (Interface & Implementation)
Create the interface in `.service` and implementation in `.service.impl` (or same package).
- Use `@Service` and `@RequiredArgsConstructor`.
- **Update Logic**: Explicitly map fields from the request to the existing database entity to avoid overwriting IDs or missing fields.
- **Error Handling**: Use `orElseThrow()` with custom exceptions or `RuntimeException` for "Not Found" cases.

### 4. REST Controller
Create the controller in the `.controller` package.
- Use `@RestController`, `@RequestMapping`, and `@RequiredArgsConstructor`.
- Use `@Valid` on `@RequestBody` for POST and PUT operations.
- Return appropriate status codes: `201` for Creation, `204` for Deletion (optional), `200` for others.

### 5. Robustness: Global Exception Handler
**CRITICAL**: Always ensure a `@RestControllerAdvice` exists to catch `MethodArgumentNotValidException` and return a clean JSON with validation errors. If it doesn't exist, create it.

### 6. Database Configuration (H2)
**100% Functional**: If no external database is configured, automatically add the H2 configuration to `src/main/resources/application.properties` (or `.yml`) so the project can run immediately.
- Enable H2 Console: `spring.h2.console.enabled=true`
- Set Datasource URL: `spring.datasource.url=jdbc:h2:mem:testdb`
- Set Driver and Auth (Optional but recommended):
  - `spring.datasource.driver-class-name=org.h2.Driver`
  - `spring.datasource.username=sa`
  - `spring.datasource.password=`
- Set DDL Auto: `spring.jpa.hibernate.ddl-auto=update`
- **SQL Debugging**: Add `spring.jpa.show-sql=true` and `spring.jpa.properties.hibernate.format_sql=true` for easier terminal reading.

### 7. Verification (Testing)
- Generate a Smoke Test or a simple `@DataJpaTest` to verify persistence logic.

## Best Practices
- **Never expose internal IDs in URLs if they are sensitive**, but for standard CRUD, `Long` IDs are acceptable.
- **Stay Immutable**: Use Lombok to reduce boilerplate but keep service dependencies `final`.
- **Validation**: Every String field should usually have `@NotBlank`. Every numeric field should have `@Positive` or `@Min`.

## Example
Refer to `references/example-crud.md` for a full implementation of a "Producto" entity.
