# Reference: Standard Producto CRUD

This example shows the implementation of a `Producto` entity using the `spring-boot-standard-crud` pattern.

## 1. Model: `Producto.java`

```java
package com.juandidev.primerarepeticion.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name="producto")
@Getter @Setter
@AllArgsConstructor
@NoArgsConstructor
public class Producto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    @NotBlank(message = "El nombre no puede estar vacío")
    private String nombre;

    @Column(nullable = false)
    @NotBlank(message = "La categoría no puede estar vacía")
    private String categoria;

    @Column(nullable = false)
    @Positive(message = "El precio debe ser mayor a cero")
    private Double precio;

    @Column(nullable = false)
    @PositiveOrZero(message = "El stock no puede ser negativo")
    private Integer stock;
}
```

## 2. Repository: `ProductoRepository.java`

```java
package com.juandidev.primerarepeticion.repository;

import com.juandidev.primerarepeticion.model.Producto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProductoRepository extends JpaRepository<Producto, Long> {
}
```

## 3. Service Implementation: `ProductoServiceImpl.java`

```java
package com.juandidev.primerarepeticion.service;

import com.juandidev.primerarepeticion.model.Producto;
import com.juandidev.primerarepeticion.repository.ProductoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductoServiceImpl implements IProductoService {

    private final ProductoRepository productoRepo;

    @Override
    public List<Producto> listarProductos() {
        return productoRepo.findAll();
    }

    @Override
    public Producto crearProducto(Producto producto) {
        return productoRepo.save(producto);
    }

    @Override
    public Producto buscarProducto(Long id) {
        return productoRepo.findById(id)
                .orElseThrow(() -> new RuntimeException("Producto no encontrado con ID: " + id));
    }

    @Override
    public Producto actualizarProducto(Long id, Producto producto) {
        Producto existente = buscarProducto(id);

        existente.setNombre(producto.getNombre());
        existente.setCategoria(producto.getCategoria());
        existente.setPrecio(producto.getPrecio());
        existente.setStock(producto.getStock());

        return productoRepo.save(existente);
    }

    @Override
    public void eliminarProducto(Long id) {
        productoRepo.deleteById(id);
    }
}
```

## 4. Controller: `ProductoController.java`

```java
package com.juandidev.primerarepeticion.controller;

import com.juandidev.primerarepeticion.model.Producto;
import com.juandidev.primerarepeticion.service.IProductoService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/productos")
@RequiredArgsConstructor
public class ProductoController {

    private final IProductoService productoService;

    @GetMapping
    public List<Producto> listarProductos() {
        return productoService.listarProductos();
    }

    @PostMapping
    public Producto crearProducto(@Valid @RequestBody Producto producto) {
        return productoService.crearProducto(producto);
    }

    @GetMapping("/{id}")
    public Producto buscarProducto(@PathVariable Long id) {
        return productoService.buscarProducto(id);
    }

    @PutMapping("/{id}")
    public Producto actualizarProducto(@PathVariable Long id, @Valid @RequestBody Producto producto) {
        return productoService.actualizarProducto(id, producto);
    }

    @DeleteMapping("/{id}")
    public void eliminarProducto(@PathVariable Long id) {
        productoService.eliminarProducto(id);
    }
}
```
