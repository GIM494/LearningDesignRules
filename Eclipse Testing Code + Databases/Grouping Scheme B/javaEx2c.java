// Filename: javaEx.java
// Author: Gennie Mansi
// Created: 07/03/1029
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
  int x;
  Base(int _x) {
    x = _x;
  }
}

class Derived extends Base {
  int y;
  Derived(int _x, int _y) {
    super(_x);
    y = _y;
  }
  void Display() {
    System.out.println("x = "+x+", y = "+y);
  }

  // Using the annotation that we defined above
  @Todo(priority = Todo.Priority.LOW,
        author = "Yashwant",
        status = Todo.Status.STARTED)
  private void incompleteMethod1() {
    //Some business logic is written
    // but it’s not complete yet
  }

  @TodoAgain(priority2 = Todo.Priority.HIGH,
        author2 = "Yashwant",
        status2 = Todo.Status.NOT_STARTED)
  private void incompleteMethod2(){
    // More interesting stuff
  }

}

// Using an annotation that we defined above
@Todo(priority = Todo.Priority.HIGH,
      author = "Yashwant",
      status = Todo.Status.STARTED)

class A {
  string firstName;
  A(string _firstName) {
    firstName = _firstName;
  }

  void printName(){
    System.out.printlin("First Name: " + firstName);
  }

  void extraTest(){
    System.out.printlin("Test");
  }

  void notPresentInChildren(){
    System.out.printlin("This one is not in the others!");
  }

}

class B extends A {
  string lastName;

  B(string _firstName, string _lastName){
    super(_firstName);
    lastName = _lastName;
  }

  void printFullName(){
    System.out.println("Last Name: " + lastName);
  }

  void printName(){
    System.out.printlin("First Name: " + firstName);
  }

}

class C extends A{

  C(){
    System.out.println("Object C created");
  }

  void printName(){
    System.out.printlin("First Name: " + firstName);
  }

  void extraTest(){
    System.out.printlin("Test");
  }

}

class Outer {
   // Simple nested inner class
   int q1;
   int q2;

   public void show() {
        System.out.println("In a nested class method");
   }

   @Todo(priority = Todo.Priority.HIGH,
         author = "Yashwant",
         status = Todo.Status.STARTED)
   class Inner {
      int q1;
      boolean isInner;
      boolean isOuter;

      @TodoAgain(priority = Todo.Priority.HIGH,
            author = "Yashwant",
            status = Todo.Status.STARTED)
      public void show() {
           System.out.println("In a nested class method");
      }

      public int returnNum() {
           return 5;
      }

      public int returnNumAgain() {
           return 234;
      }
   }
}

class OuterEx2 {
   // Simple nested inner class
   int q3;
   int q4;

   public void show() {
        System.out.println("In a nested class method");
   }

   @Todo(priority = Todo.Priority.HIGH,
         author = "Yashwant",
         status = Todo.Status.STARTED)
   class InnerEx2 {
      int q4;
      int q5;

      @TodoAgain(priority = Todo.Priority.HIGH,
            author = "Yashwant",
            status = Todo.Status.STARTED)

      public void show() {
           System.out.println("In a nested class method");
      }

      public int returnNumAgain() {
           return 234;
      }

      public int returnDifInt(){
           return -90;
      }
   }
}

public class Main {

  public static void main(String[] args) {

    Derived d = new Derived(10, 20);
    d.Display();

    B name = new B("Gennie", "Mansi");
    name.printFullName();

    Outer.Inner in = new Outer().new Inner();
       in.show();

  }
}

// A simple interface
interface in1
{
    // public, static and final
    final int a = 10;

    // public and abstract
    void display();
}

// A class that implements interface.
class testClass implements in1
{
    // Implementing the capabilities of
    // interface.
    public void display()
    {
        System.out.println("Geek");
    }

    // Driver Code
    public static void main (String[] args)
    {
        testClass t = new testClass();
        t.display();
        System.out.println(a);
    }
} 
