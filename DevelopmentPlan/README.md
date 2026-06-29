# Situational plan

> ***Agile:*** this means, many decisions are done based on previous experience of development, rather than strict "waterfall" initial plan.

DevelopmentPlan folder of LaeLane repo (current folder):
- This file contains the initial task and it will be archived if the task is ready.
- Other files would contain the number type specifications and other specifications, which will be cleaned and taken to use if the task is ready.
- Older Laegna Number Databases will be not removed, but each of them would be repeatedly confirmed about being up to the new standard.
  - If formats are heavily normalized, sheep counters and other databases might be updated to reflect rather a few ("single"), standard, and applicable type of Laegna Numbers.

You can continue your developments, because:
- Refactoring is a standard term.
- *Logical structure*, such as R as main chapter, T as subchapter, signed/unsigned lae/dec formats, etc., won't change, altough the terms can be more standardized.

Hoping for your tolerance: the standard variability in the beginning, openness and acceptance of both positive and negative experience, would mean much more stability later when it becomes costly to do even simple refactoring tasks like renaming a field - somebody might connect "Dec" and "Signed" in cryptic way such as accounting "Signed" as standard term of complex database.

## Current development

For Laegna Numbers, to have standard implementation, I currently made number database files, which contain R = \[0.5, 1 to 4\] - five possible digit lengths are written out.

One can see that code and databases themselves are important result, which is partically true, but:
- This initial experience did show automated, algorithmized Laegna Numbers as data.
  - I could see all aspects of computability, presentation and load.
    - Storing heavy load of number data slowly becomes computationally inefficient, given the file format is human-readable.
    - Generator should now start working real time, and emulate the number database or let one download zip, as it's automatically generated on the fly.
    - Number database remains as manual source form, definitely: any data for particular numbers or lanes, which is calculated for this particular instance and not general rule,
      can be associated with specific number through database in future; driver would load it from there.
  - I implemented basic conversions, mostly in one direction (from data index to content types).
    - This means basic algorithms exist and they are testable: any reverse-operation can be tested, whether it's result with initial operation provides the input for reverse op.
  - So the basic result is that I have all generators, operations, cases and exceptions around in py files and database examples.

## Next development

The following will be achieved:
- I will extract every particular number operation from Laegna code to specialized classes.
  - This means, generators are implemented as standard iterators; numbers as coherent laegna number instances.
    - Generators can produce listings at any moment.
    - Laegna numbers can count through iterators, convert between laegna and latin types.
      - They will contain all basic operations - minus, plus, divide, multiply -, plus critical laegna-contextual modifiers - octaves, exponentiation etc.
  - This also means, every class knows it's data meanings and is able to produce helpful information, i.e. number data can be viewed verbosely, such as field \["Laegna"\]\["Std"\] will be not only Laegna standard number, but verbose mode associates it with additional tag - "DocString", so that there will be \["Laegna"\]\["Std"\]\["DocString"\], and inside there will be text like "Laegna Standard Number" or print sequence such as ("Laegna Standard Number #X", {"X", "AA"}), which lets an AI or robot uniquely identify the string based on it's head (same for all numbers), but also understand it's modifiers - AI would understand "Laegna Standard Number #X" as docstring, to be compared with docstrings of other numbers so that they are identical, but also that it can print it in formatted string: "Laegna Standard Number AA"; so if it analyzes docstring more specifically, it would completely understand that it's the standard number at position "AA".
