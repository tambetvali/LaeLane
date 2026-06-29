# Introduction

The numbers I implemented were seen by me as *close to Laegna standard numbers*.

What is the problem?

With my existing math, I am operating in my brain and they are tolerant:
- Lacking certain bits is compensated by my understanding, and use of algorithms which somehow emulate the bit, take it from other place or just be happy if it's wrong.
- Many operations can be intuitively done: for example, "EE"*"EE" was "EEEE" right from beginning of Laegna - notice that this just mapped my *general idea of laegna number* and not that the number type would directly do this operation, like current Laegna number: I was intuitively choosing sequences, comparing them and making sure every important number for infinity exists.
  - I followed certain rules, brought it always back to less number of axioms in axiomatic system and finally:
    - Reached these counters which have standard counting format.

The standard counting format is not 100% what lanes need, but lanes add a few additional criteria:
- For example, bit-length of number must be always normalized to even number of bits, not assuming that I know sweet and interpolated answer for operation I cannot do.
  - Head-calculation, intuitive: for every two numbers, for example to add them, I could solve all the axiomatic process and run three times with my single added number, for example doing everyhing "EE + EE = EEEE" can do, based on axiomatic properties of each of two numbers, operation, even equality.
  - Automated caluclation: wants closed binary table, logical structure with all paths of calculations closed, explicit, and standard.
    - Computers, without an AI, are thus not going to show us the beauty and depth of infinity, or the wisdom of creatively handling the calculations, but:
      - This is like calculating with Roman numbers: multiplying two big numbers and guaranteeing the solution for critical account could take a day, for experienced and specially chosen person. Even if it's not so reliable, you do it for hours. Because there are all kinds of known tricks and relations you can creatively use.
      - Multiplying two latin numbers was relatively fast, dumb and automatic: now we could make normal people calculate interest, find if one day is worth x then how much 365 days would be worth of.
      - Laegna numbers are supposed to reach infinity with this, and not be another roman numerals where one would spend day to calculate general direction of their life, or whether an outcome of simulation is positive.

Now I promise you:
- Critical aspects won't change, they are based on stable standard and experience.
- I will take utter care to normalize number lengths, make sure different tables point to operations on same data and do not expect intermediate calculations to be used.
- API and interface remains roughly the same - it needs some routine refactoring, perhaps, like changing every 1 to 2 somewhere, but it does not expect learning new structures and implementing them except the case that signed numbers: will be much more powerful if they start with "E" or "I".

Because this overcomplication reached suddenly, I understood that *lane format must be much more clear*, and this means developments are stopped, and fresh design for LaeAutomation and LaeLane number formats will be reached, and each other number database will be two-way associated, such as sending data back to number counters, and utilizing all their functions, perhaps generation sheepcounter.json or animation.json locally as needed or later, also accepting user modifications, tags and metadata added later to these files (I think they are progressive raise of complexity - sheepcounter is simplest, the next version more complicated, and this version will look almost like a system).

# Updated Laegna Number Types

Laegna number types implement:
- Signed and unsigned.
- Ordered, discrete, natural and no floating-point implemented.
  - Every operation in this linear domain is implemented: +, -, *, /, pow, some more essential functions like geometric and numerical average.
- Decimal and decimal-like laegna conversations (convert to decimal, in this database means providing it's growth function, where actual decimal number is in decimal conversion field, not the field index which needs laegna R and T synchronization - decimals themselves will provide *irrational number as a synchronizer*).
- Laegna numbers and Laegna wave numbers are implemented, each-way conversion realtime first in python, then ported to js.
- System administrators can get real database models and it's enough-documented to be compatible between providers, and not so much to disable more specified compability layers.
- Every system is lane, counting compatible.
- Every system is compatible for trivial, in-system extensions to floating point (trivial to divide number's boundary and fractional boundary) and multidimensionals like Z-X-Y scale (repeated logic in three modalities). For sake of simplicity, none of them exists in basic database which becomes "laegna binary" format, rather stricted to laegna logecs essentials - it's logecal logic.

## Signed flag representation

***Problem:*** Having only + and - as signed flags is not acceptable because number bit count will not divide by two and square index is disabled: non-hashable, exponent function is intellectual and not simple operational.

***Result:*** decode the most critical missing bit to make sign take two bits, so that the remaining number keeps it's existing symmetry with 2 and is thus two-band enabled standard, discrete-base number.

***Implementation:***

Plus sign "+" ("A") maxima and minima:

```
  /
 /
/
Zero-line.
```

```


___
Zero-line.
```

Minus sign "-" ("O") maxima and minima:

```
Zero-line.
\
 \
  \
```

```
Zero-line.
---


Zero-line.
```

Multiplication sign "*" ("E") maxima and minima:

```
|
|
|
Zero-line.
```

```
  /
 /
/
Zero-line.
```

Division sign "/" ("I") maxima and minima:

```
Zero-line.
\
 \
  \
Zero-line.
```

```
Zero-line.
|
|
|
```

***Solution:*** first digit of signed number is now standard base-4 number, and four operations are supported as *infinity digits* in second order.
- If local is not solution and infinite is, use local positive number as symmetry to this single-bit value. Typically infinity solves the locality (i.e. o-optimization cancels the finite debug).

## Boundaries

Now, boundaries allow 180 degree turns, where "IOAE" approximate to "1234": this was "X (IOAE)" and backwards, "ÀÈÍÓ" provide "Z (ÀÈ)" and "Y (ÍÓ)" bits as necessity for a function to go backwards - the 8-system is discrete system and might be enabled in future conditions, right now the standard base-4 values only enable 180 degrees, standard function where infinity and zero errors are not enabled by default.

### Unsigned system

Flag is not concern and in essentials, the representation won't change.

They are all like opengl: exp-2 systems. Square fields whose "a" is order of 2 (2, 4, 16, 256 or the most preferrable).

### Signed system

Flag is now standard two-bit digit:
- Values such as `R=0.5 O, A`, and `R=1 I, O, A, E`:
  - O, A are range-2-base, which will be implemented and they mean just - and + in unsigned system, averaging - "-" is avg of "-" and "/", while "+" is avg of "+" and "*"
  - Either U means unknown and multiplicity of tracks to future is unknown, or U means 0 and the possible paths are averaged based on their compability, and operational system average is used.
  - O, A, divide 180 degrees of + and -.
  - I, O, A, E provide 180 degrees
  - Signed number now effectively provides 4 zones as unsigned provides one. For abs-number representation which removes first digit or sign representation of signed number, unsigned numbers remain in 1/4 zones like their abs-number equivalents.
  - Later, with more digits, 4 zones always open and infinity is trivially and gracefully-enough represented in 1-st order system, limited that for SC, any version, we *do not know unknowns and 8ths, we only know base-2, base-4 and base-16 systems which all are able to operate in internal, linearized spaces*.
  - To update them to higher-order math is already part of laegna mathematecs, utilizing the existing mathematical operations.
    - Here it's logecs range-1, we order the numerical and mathematical conditions for base layer, equivalent to "binary" for the os, widgets, and extended capabilities for later or even developer-programmed.

Signed system also shows function in signed range, which completes it as square hash index and open-gl-compatible because it's a laegna exponent - equivalent to an order of "2" for systems designer, useful in laegna and operational programming mode.

Signed system now: allows to perfectly fit I, O, A, E lin-exp model by automate in real-time, not inventing solution for every number (which for me is habitual).
- Sheep counters should use 1-bit sign for counting, because it's more efficient.
- This is still not possible, because the user learns same system they are going to use, so we make sheep counters inefficient for simple counting by adding one-bit-meaning to every number, about whether it's sign is linear or exponent.

The bit now has the same meaning in every digit - certain signs are linear, while higher signs are exponential.

Why the real exponent count for signs?
- Binary continuous functions for example, give missing numbers at that point. In 14 (1 to 4) zone, adding more precision to angle makes the line straight up or down longer, so functions efficiently do a *stand still* both up and down, projecting missing infinities. Two dimensions are enough to count all of them, unless you specifically seek for "irrational infinities" not for binary counting.

## High-order precision, but hashable

Upper part of function is calculated (calculation is defined already in readme md files at root), not needed by hash:
- Indexes can be filtered, O and A orders provide only hash, I and E orders provides whole function, and minus or plus flag of this letter v-flips Y axe to point down (O, programmer, text file or picture pixel / console-screen) or up (A, scientist, business / graph-introduction-as-lower-R-head).

So the O and A orders provide what currently exists, while I and E orders provide only the upper part of function in several optimal parts, as described in main README.md file as well.

## User taggable and explainable numbers

User provides data, which is manually entered for specific digits or numbers, and automatic interface loads this yet in db format, where new operations would be test-implemented first, possibly.

## My confirmation

After this:
- Relevant function of Laegna to turn function up or down is introduced as a "missing bit", which would otherwise just in trash now with technical needs and updates, issues at main page now.
- The number system is complete lin-exp from sign to number, and advanced laegna calculus can be introduced as math, not as bitwise magic and blackboxed goals.
  - To be complete means to be computable.
