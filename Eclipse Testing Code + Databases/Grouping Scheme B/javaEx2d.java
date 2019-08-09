// Import
import java.util.Date;
import java.io.*;

class F {
  string firstName;
  F(string _firstName) {
    firstName = _firstName;
  }

  void printName(){
    System.out.println("First Name: " + firstName);
  }

  void extraTest(){
    System.out.println("Test");
  }

  void notPresentInChildren(){
    System.out.println("This one is not in the others!");
  }

}

class C extends F {
  string lastName;

  C(string _firstName, string _lastName){
    super(_firstName);
    lastName = _lastName;
  }

  void printFullName(){
    System.out.println("Last Name: " + lastName);
  }

  void printName(){
    System.out.println("First Name: " + firstName);
  }

}

class B extends F{

  B(){
    System.out.println("Object C created");
  }

  void printName(){
    System.out.println("First Name: " + firstName);
  }

  void extraTest(){
    System.out.println("Test");
  }

}


class G extends F{

  G(){
    System.out.println("Object C created");
  }

  void printName(){
    System.out.println("First Name: " + firstName);
  }

  void extraTest(){
    System.out.println("Test");
  }

  void sayMessage(string m, int i){

    for (int j = 0; j < i; j++){
      System.out.println()
    }

  }


}



class E extends B{

  E(){
    System.out.println("Object C created");
  }

  void printName(){
    System.out.printlin("First Name: " + firstName);
  }

  void extraTest(){
    System.out.printlin("Test");
  }

}


class A extends C{

  A(){
    System.out.println("Object C created");
  }

  void printName(){
    System.out.printlin("First Name: " + firstName);
  }

  void extraTest(){
    System.out.printlin("Test");
  }

}


class D extends A{

  D(){
    System.out.println("Object C created");
  }

  void printName(){
    System.out.printlin("First Name: " + firstName);
  }

  void extraTest(){
    System.out.printlin("Test");
  }

}
