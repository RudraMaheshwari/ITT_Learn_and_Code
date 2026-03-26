# Does This Book Class Follow SRP?

## No, This Code Does Not Follow SRP

The Single Responsibility Principle states that a class should have only one reason to change. Looking at this Book class, we can see it is doing too many things at once.

## The Problem

The Book class has four different responsibilities mixed together:

First, it handles book information through the `getTitle()` and `getAuthor()` methods. This is about storing and retrieving basic book metadata.

Second, it manages reading behavior with `turnPage()` and `getCurrentPage()`. This is about navigating through the book content.

Third, it tracks library location using `getLocation()`. This is about where the book sits on the shelf in the library.

Fourth, it handles data persistence with `save()`. This is about saving the book object to the file system.

Each of these responsibilities could change for completely different reasons. If the library reorganizes its shelving system, we would need to modify this class. If we decide to store books in a database instead of files, we would need to modify this class. If we change how page navigation works, we would need to modify this class. This makes the class fragile and hard to maintain.

## Fixed version is in the folder book_services
