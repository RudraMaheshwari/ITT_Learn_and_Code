# Comment Analysis and Refactoring Summary

## Identified Bad Comment Types

### 1. Redundant Comments

Comments that restate what the code clearly does.

**Examples:**

- "Check if order is null" (for `if (order == null)`)
- "Validate the order" (for `IsValidOrder(order)`)
- "Process payment" (for `_paymentGateway.ProcessPayment(...)`)
- "Check inventory"
- "If no inventory, return failur"
- "Reserve inventory"
- "Check if payment succeeded"
- "Update inventory"
- "Send confirmation email"
- "Return success"
- "Payment failed, release inventory"
- "Return failure"
- "Log the error"
- "Throw it"

---

### 2. Noise Comments

Comments that add no information and clutter the code, often summarizing a method or block trivially.

**Examples:**

- "This method processes an order" (above `ProcessOrder`)
- "Gets order by ID" (above `GetOrderById`)
- "Saves the order" (above `SaveOrder`)
- "Something went wrong" (in catch block)
- "Implementation here" (in `GetOrderById`, `SaveOrder`)

---

### 3. Misleading Comments

Comments that don't match the code or are confusing.

**Example:**

- "Fix this later" (if not actually fixed or if logic is fine but comment is left)
- _Note: In the provided snippet, `// If no inventory, return failur` contains a typo and states the obvious._

---

### 4. TODO Comments

Markers for future work left in production code.

**Example:**

- "TODO: Fix this later" (inside `IsValidOrder`)

---

### 5. Journal / Attribution Comments

Comments tracking who changed what and when.

**Examples:**

- "Added by John on 12/15/2023 - needed for the new feature"
- "John says we need to refund here"

---

### 6. Overly Emotional / Emphatic Comments

Comments that express emotion or use excessive formatting to emphasize importance.

**Example:**

- "This is important!!!"
