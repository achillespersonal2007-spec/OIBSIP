# Number Guessing Game (Java Development Track - Task 2)

A desktop graphical application (GUI) built with **Java Swing** for the **Oasis Infobyte Internship Program (OIBSIP)**.

---

## Features
- **Standalone GUI Interface**: Interactive Java Swing desktop application featuring clean event-driven controls.
- **Dynamic Difficulty Modes**:
  - Easy: Range 1–50 (10 attempts)
  - Medium: Range 1–100 (7 attempts)
  - Hard: Range 1–200 (5 attempts)
- **Interactive Feedback**: Real-time heuristic alerts (`Too High!`, `Too Low!`, `Correct!`).
- **Scoring & State Retention**: Tracks round numbers, attempts used, and cumulative score with a "Play Again" cycle.
- **Input Validation**: Safe handling for empty, non-numeric, or out-of-range inputs.

---

## Preview
![Gameplay Demo](screenshots/gameplay_demo.png)

---

## Compilation & Execution

```bash
cd src
javac GuessingGameApp.java
java GuessingGameApp