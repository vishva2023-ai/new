public class MathOperations {

    // a. Addition
    public int add(int a, int b) {
        return a + b;
    }

    // b. Even or Odd
    public String evenOdd(int num) {
        return (num % 2 == 0) ? "Even" : "Odd";
    }

    // c. Multiplication
    public int multiply(int a, int b) {
        return a * b;
    }

    // d. Factorial
    public long factorial(int n) {
        if (n < 0) throw new IllegalArgumentException("Negative not allowed");
        long fact = 1;
        for (int i = 1; i <= n; i++) {
            fact *= i;
        }
        return fact;
    }

    // e. Prime Number
    public boolean isPrime(int n) {
        if (n <= 1) return false;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) return false;
        }
        return true;
    }

    // f. Switch Case (Add, Sub, Mul, Div)
    public double calculator(int a, int b, String operation) {
        switch (operation.toLowerCase()) {
            case "add":
                return a + b;
            case "sub":
                return a - b;
            case "mul":
                return a * b;
            case "div":
                if (b == 0) throw new ArithmeticException("Divide by zero");
                return (double) a / b;
            default:
                throw new IllegalArgumentException("Invalid operation");
        }
    }

    // e. Fibonacci
    public int fibonacci(int n) {
        if (n <= 1) return n;
        int a = 0, b = 1, c = 0;
        for (int i = 2; i <= n; i++) {
            c = a + b;
            a = b;
            b = c;
        }
        return c;
    }

    // g. Palindrome
    public boolean isPalindrome(int num) {
        int original = num, reverse = 0;
        while (num != 0) {
            int digit = num % 10;
            reverse = reverse * 10 + digit;
            num /= 10;
        }
        return original == reverse;
    }
}
