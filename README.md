# SOLID Principles - Learn and Code

This branch contains practical examples demonstrating the five SOLID principles of object-oriented design. Each principle is organized in its own folder with real-world code samples extracted from production applications.

---

## What This Branch Contains

This repository showcases how SOLID principles are applied in actual codebases. Each folder contains Python files that demonstrate a specific principle, along with a README explaining why each file is a good example.

---

## Folder Structure

### Single_Responsibility_Principle

Contains examples where each class or module has exactly one reason to change. Files include repository classes for specific database tables, a dedicated email service, and a focused transcript extraction module.

### Open_Closed_Principle

Contains examples of code that is open for extension but closed for modification. Files include a factory pattern for creating agents, an extensible exception hierarchy, and a registry pattern for managing tools.

### Liskov_Substitution_Principle

Contains examples where derived classes can substitute their base classes without breaking functionality. Files include a base repository with consistent interfaces, API client with uniform error handling, and properly composed repository implementations.

### Interface_Segregation_Principle

Contains examples where clients depend only on the interfaces they need. Files include focused helper functions, specific service getters, and modules that import only required functionality.

### Dependency_Inversion_Principle

Contains examples where high-level modules depend on abstractions rather than concrete implementations. Files include services that accept repository instances through constructors and validators that rely on configuration abstractions.

---

## How to Use This Repository

1. Navigate to any SOLID principle folder
2. Read the principle-specific README file for context
3. Review the code files to see practical implementations
4. Use these patterns as references when designing your own systems

---

## Purpose

This branch serves as a learning resource for developers who want to understand how SOLID principles translate from theory to practice. The examples are drawn from real applications, making them more valuable than abstract textbook examples.
