This assignment provided deep insights into the role of comments in software maintenance and readability:

- **Impact of Comments**: I observed how comments can either clarify complex logic or clutter the codebase, directly affecting maintainability.
- **Code as Documentation**: I learned that the primary source of truth should be the code itself; clear naming conventions often eliminate the need for explanation.
- **Filtering Comment Types**: It became clear which categories of comments add value (e.g., business logic explanations) and which are detrimental (e.g., stating obvious operations).
- **Maintenance Cost**: I realized that every comment is a liability that requires updating alongside the code, otherwise it becomes misleading.
- **Differentiation**: I can now distinguish between helpful "Why" comments and harmful "What" comments.
- **Refactoring Signal**: I learned to see comments as a potential "smell" indicating that a code segment might need refactoring rather than explaining.

Regarding detailed comment categories, I learned:

1.  **Redundant & Noisy Comments**: Comments that merely repeat the code (e.g., "increment i") are noise and must be removed to improve readability.
2.  **TODOs**: These should be actionable and managed properly, ideally in a tracker, rather than left as vague notes in the code.
3.  **Journal/Attribution**: Version control systems (Git) are the correct place for history and authorship, not the source files.
4.  **Intent & Warnings**: The most valuable comments explain the _business intent_ or warn of non-obvious consequences, as this information cannot be derived from the code syntax alone.
5.  **Misleading Comments**: Outdated comments are dangerous; it is better to have no comments than incorrect ones.
6.  **Emotional Comments**: Code comments should remain professional and objective; emphasis should be structural, not emotional.
