// Filename: javaEx.java
// Author: Gennie Mansi
// Created: 07/03/2019
// Description: This is just a test file with a bunch of different
// functions and java features; it is created to test the ability
// of the sampleParsing.py file to parse information about a file
// correctly.

// Import
import java.util.Date;
import java.io.*;

// Note annotation example and code obtained from:
// https://dzone.com/articles/how-annotations-work-java

// Define a custom annotation
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@interface Todo {
public enum Priority {LOW, MEDIUM, HIGH}
public enum Status {STARTED, NOT_STARTED}
String author() default "Yash";
Priority priority() default Priority.LOW;
Status status() default Status.NOT_STARTED;
}

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@interface TodoAgain {
public enum Priority {LOW, MEDIUM, HIGH}
public enum Status {STARTED, NOT_STARTED}
String author2() default "Yash";
Priority priority2() default Priority.LOW;
Status status2() default Status.NOT_STARTED;
}

// Using the annotation throughout the file on classes and on
// functions
@Todo(priority = Todo.Priority.HIGH,
      author = "Yashwant",
      status = Todo.Status.NOT_STARTED)
@TodoAgain(priority2 = Todo.Priority.HIGH,
      author2 = "Yashwant",
      status2 = Todo.Status.NOT_STARTED)
class Base {

  @Todo(priority = Todo.Priority.HIGH,
        author = "Yashwant",
        status = Todo.Status.NOT_STARTED)
  int x;

  Base(int _x) {
    x = _x;
  }

  // Using the annotation that we defined above
  @Todo(priority = Todo.Priority.LOW,
        author = "Yashwant",
        status = Todo.Status.STARTED)
  private void incompleteMethod1() {
    // Some business logic is written,
    // but it’s not complete yet
  }

  @TodoAgain(priority2 = Todo.Priority.HIGH,
        author2 = "Yashwant",
        status2 = Todo.Status.NOT_STARTED)
  private void incompleteMethod2(){
    // More interesting stuff
  }

  void printName(){
    System.out.printlin("First Name: " + firstName);
  }

  private static void display() {
    System.out.println("Java is my favorite programming language.");
  }

}
