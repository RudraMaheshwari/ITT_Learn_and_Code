# ITT_Learn_and_Code

**ITT_Learn_and_Code** is a structured learning and development repository built to help developers understand real-world software concepts through simple, clear, and practical examples.  
The goal is to make complex topics easier by demonstrating them with hands-on code, best practices, and explanation-driven learning.

---

## 🚀 What This Repository Offers

- **Real-world coding examples**
- **Clean and scalable code patterns**
- **Step-by-step explanations for clarity**
- **AI, ML, DevOps, and backend code samples**
- **Debugging guides and architecture notes**
- **Best practices for Python, APIs, Docker, and more**

---

## 📘 Purpose

This repository is created to:

- Provide a single place to **learn and build together**
- Break down difficult concepts into **easy-to-understand examples**
- Help new and experienced developers practice **real industry-level coding standards**

---

## 🧩 Who Is This For?

- Students
- Beginners in coding
- Developers practicing for interviews
- Engineers exploring new technologies
- Anyone who wants to learn by doing

---

## 📂 Contents (Examples)

- 🔹 Python utilities & scripts
- 🔹 API development examples
- 🔹 Docker & containerization demos
- 🔹 AI/ML small projects
- 🔹 Debugging & error explanation snippets
- 🔹 System design notes
- 🔹 Best coding practices & patterns

_(Actual content will grow over time.)_

---

## 🤝 Contribution

Contributions are welcome!  
Feel free to submit pull requests, open issues, or suggest new topics to cover.

---

## ⭐ Support

If you find this helpful, give the repository a **star** — it helps others discover it and supports future updates.

---

## 💳 Billing Project (Clean Code Assignment)

This project demonstrates the application of **Clean Code** principles, specifically focusing on the **Law of Demeter (LoD)** and the **"Tell, Don't Ask"** principle.

### 📜 The Original Assignment (Java)

The following code was the starting point, containing several Clean Code violations:

```java
public class Paperboy {
    public void collectPayment(Customer customer, double paymentAmount) {
        Wallet wallet = customer.getWallet();
        if (wallet.getTotalMoney() >= paymentAmount) {
            wallet.subtractMoney(paymentAmount);
        } else {
            // come back later
        }
    }
}

public class Customer {
    private String firstName;
    private String lastName;
    private Wallet myWallet;
    public String getFirstName(){ return firstName; }
    public String getLastName(){ return lastName; }
    public Wallet getWallet(){ return myWallet; }
}

public class Wallet {
    private float value;
    public float getTotalMoney() { return value; }
    public void setTotalMoney(float newValue) { value = newValue; }
    public void subtractMoney(float debit) { value -= debit; }
}
```

### ❌ Law of Demeter (LoD) Violations

1.  **Direct Internal Access**: In `Paperboy.collectPayment()`, the `Paperboy` calls `customer.getWallet()`. This violates LoD because the `Paperboy` is now interacting with a "friend of a friend" (the `Wallet`). It should only interact with its direct friend, the `Customer`.
2.  **Train Wreck Pattern**: The chaining of `customer.getWallet().subtractMoney()` is a classic "train wreck." The `Paperboy` should not be responsible for checking the wallet's balance or substracting money from it; that logic belongs to the `Customer` and the `Wallet`.
3.  **Encapsulation Breach**: By providing `getWallet()`, the `Customer` class exposes its internal data structure (`Wallet`) to the outside world, making the system brittle to changes in how payments are managed.

### ✅ Refactored Solution (Python)

The refactored solution follows the **"Tell, Don't Ask"** principle:

- The `PaperboyCollector` **tells** the `Customer` to pay.
- The `Customer` **tells** the `Wallet` to debit the amount.
- The `Wallet` handles its own state transition atomically via `try_debit()`.

### 🚀 How to Run

To execute the payment workflow and see the result:

```bash
python3 main.py
```

### 📂 Project Structure

```text
billing/
├── domain/
│   ├── customer.py      # Encapsulates names and wallet
│   └── wallet.py        # Manages balance and atomic debits
├── services/
│   └── paperboy_collector.py  # Orchestrates payment collection logic
└── workflows/
    └── collect_payment.py      # End-to-end payment workflow class
main.py                  # Project entry point
```

---

### **Learn. Build. Improve. Repeat.**

**ITT_Learn_and_Code**
