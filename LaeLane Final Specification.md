# This specifies the functions of LaeLane I am going to implement in Red

This will be first-order Laegna Logecs, with only discrete operations: it can be used as mathematical basis, such as fractions made from two integers, or integer divided by constant or mantissa to receive new Laegna numbers: these are not first-order, because additional digits have semantic forms in laegna base system, while theories and literal grammar forms create advanced forms of 2nd order math, for example each digit can have accent, but accent is base-4 digit itself, graphically and symbolically in it's visual position: base Laegna, order-1, does not have this grammar, but has this semantic form that each digit can be associated with it's parallel digit: this is already math, not building a basic number system.

***Laegna Number Database and Lane now need one single implementation, so documents often mix up the concepts rather into modules of single, than providers of two different systems: so it's sometimes hard to understand whether lines, lanes or numbers and R's are considered, because - they are parts of this same implementation and LaeLane and LaeAutomation will have just different configuration, with the same program, as a few other ones.***

## Base-4 system

Base-4 system will be implemented, without fractions, to allow further development of advanced number system.
- Basic counting, R's
- Primitive math operations might follow
- Signed and UnSigned
- Laegna and Laegna Wave
- Lanes, Lines, and trivial identification codes (number itself, in geometric-linear repr.)
- 1D and 2D numbers might follow

## Signed and UnSigned

Sign is Laegna digit:
- Higher band should be sign of higher band of other digits.
- Lower band should be sign of lower band of other digits.
- Each band, in rather symmetric projections, should be sign of digits of this band naturally or by definition.
  - Surrealistic projection might not linearize this.

If X is facing foreward, Y upward - X positions in writing direction, Y from bottom to top -, right foreward direction (where X is growing, and Y is not) is zero degrees, right upward (where Y is growing, X is not) is 180 degrees, and right downwards (where Y is shrinking, X is still still) is -90 degrees, minus 90 degrees.

Multiplication sign "E": From 90 to 45 degrees. "\*E(e)", digit periodic equivalent of "\*E.(E)" if dot is used for fractional part and braces for infinite series of digit, is exactly 90 degrees, from E to A to O to I it counts to 45 degrees (8, 7, 6, 5) and \*E(i) is exactly 45 degrees if number has sign "E" or alternative decimal-based "*".

Addition sign "A": From 0 to 45 degrees. +I(i) is 0 degrees, +E(e) is 45 degrees: it's a limit value, thus melts to next point as single, two-point-symmetric acceleration between them, at actual ideal limit. They behave differently if following digits do not continue the same-letter series, for example in unfolding of large numbers or large number basis (accumulation of numbers enables their statistical properties as mean fact, and UV-layer of Laegna Logecs happily processes these probabilities as normal numbers we do not cover in basic math). In basic math, to omit a digit to probability, omit it's processing, or process only one bit and give it a value in base-2, not affecting the other, then give the resulting value to base-4, *which needs to have compatible program*. I, O, A, E count from 0 to 45 degrees (1, 2, 3, 4).

Negation sign "O": From 0 to -45, -E, -A, -O, -I count -1, -2, -3, -4 in this order - from 0 to -45, minus 45, degrees.

Division sign "I": From -90 to -45, in order of I, O, A, E count from -90 to -45, -8, -7, -6, -5.

Counting orders are important: *number content* of *negatively contained (Z) numbers* is inversed, *superpositively contained (Y) numbers* are reversed - upwards analog of inversing in Laegna.

---

Signed Domain is shown both in plus and minus.

### Signed Lines

Very easily, given projections hold.

Upwards movement becomes exponent growth, not visible in Eucleidean-typical function of linear X and Y.

### Signed Lanes

I and E become 2-dimensional, with built-in exponential growth; base-16 would also separate each component in each digit, and base-2 convert it to diagonal binary represenation under various modes (binaries are hardly used alone). Laegna Quaternary, Binary, Hexademical formats of Signed and UnSigned form.

In each system, sign is multi-bit: in base-16, sign applies to each channel and their normal relations, and diagonal sign matters in compression which keeps the base-16 dimension and it's number-linear manners vs. logic (whose complexity grows by octave with every added bit, single number is more linear and solution is approximated, thus the growth is seen linear: multitude of numbers behave non-linearly and complexity growth is that-level exponent).

On Lane Level: angle goes to exponent, touches the straight-up or straight-down at end of first or second quarter (based on octave mechanics), then grows straight up and *knows the math relations, for example to show integral curve of binary jumps*. Binary logic: linearly accelerated.

Life case:

> If you know the acceleration, see it in your curves, calculate as valid method of math;
>
> It happens anyway: to do it, is to measure, choose, and repeat the best cases. To see, precisely, where you exponent speed up: is already, to do it.
> - And advanced math makes it even better.

## Lane Hashing

Upper part of minus and plus (-45 to 0 degrees, 45 to 90 degrees) are higher-channel-topologies of two octaves, and you see how octaves span plus and minus of given frequency (this is not from music theory, but fractal repetition of fixed and balanced resolutions: from music theory, a tone is what resonates with tone, and negative numbers resonate *upwards* - notes are not resonant, if what happens for *first* negative, or *last* positive, is that *you need infinitely large number). Opposition: -90 to -45 degrees, 0 to 45 degrees, are the *lower band* of a number: you start counting from minus infinity to reach it's first half, and from both directions: laegna number symmetry to count the *middle*, octave-symmetric area of finite numbers, their exact center with limit value point included, this area is also infinite, because it's *fractal point acceleration product*, *not zeroeth integral or not zeroeth differential* class number.

Primary, lower hash: Exponent of I, O, A, E etc. if X at that position, and Y is where each position grows fractal smallest branch; latination (line calculation) of laegna lanes makes this non-ordered between positions. Bottom half of minus scale repeats this display, because the number is flat and grows at given speed, defined by two bands. If four bands are used, they can be disharmonic: if not, they are harmonic, and this is linear nature of line, growth linearly represented - if growth factor itself grows, the linearity represents differently, but also higher level integrals exist as bands not as projections. Value count for every position X is equal to X, so Y is in range of X value, signed Y is in absolute range of absolute value of X, range of Y = plus-minus abs X and between.

Secondary, higher hash: also, from the end of same box which appears counting from ending of this box: the higher sign of *lowest* bit connects the duplicate of exponent points to zero downwards, octave-repeated at minus (so that higher band of minus R-equals higher band of plus, but opposes the lower band. In order E, A, O, I, points are drawn by digits of number we this time count from end: exponent 1, 4, 16, 256 etc. is now removed from end in each step; if range is 64 for two-digit number, I, O, A, E of lower band count 1, 4, 16, 64, while E, A, O, I of higher band count down 64, 61, 49, 1.

We can see more branches to count upwards and downwards.

If we do this by mixing multichannel, for example two channels X and Y provide fractal: for 1 digit, 4 values each fractally made of 4 values. But *linear* is to count first value of first branch, second of second etc., not to associate whole blocks to fractal representations - fractal representation also removed the "added infinitesimal" of number system, and makes it hologram-like, to represent limits at edges and centers of each digit, it's natural directions and flow. IOAE is divided on band 1, lower band, to I<!>O, A<!>E, and on higher band to IO<!>AE. Notice that on lower band, OA are connected but middle-symmetrically: On each level, they go in pairs; on lower channel the pairs are divided by higher channel; on higher channel by lower channel - these positions which contradict, count the middle-values by this contradiction and this is perhaps the hardest part to imagine and model, but also not primitive part of the number system now, for our automation.

## Angles

Positive angles use full 0-90 degrees framework, and with minus sign counting from up, they project same amount of degrees down: this is how to write a *minus unsigned number*, for example E is -1, A is -2, O is -3, I is -4, and which is easily another way to use 1 to 8 compatible framework, especially if +U and -V are used, -U and +V removed from H, the cellular space of number system, it's coordinate belonging.

Each angle counts symmetrically so much exponents on X that Y never fails to smoothly grow in it's direction, where discrete pixel exists for every position of growth.

We can see: as range is growing, so is content, by steps but exponential Y growth.

## Representation

One basic modulus written in Red/Rebol (one or both) will serve me in implementing *this version of number system*.

It goes roughly like this:
- L#A - this would be Laegna number A, where base is unknown (function might fix this with type check and range specification).
- L2#A - this would be Laegna base-2 number A.
- 4L#A - this would be Laegna base-unknown number A in four digits, such as AAAA (padded by repeating it's first digit, or it's base-2 simplification).
- 4L2#A - this would be AAAA, base-2 R=4 version of A's exact value.
  - Notice this is about numeric values, where we raise R by padding, not mathematical operation, where we raise R by single- or multiband scaling.
- L# - laegna R=0, number with zero digits
- 4R# - whole R range 4, where 2R# to 4R# would involve all three ranges in order.
- 4R#AE - 4R (4 digit numbers) from AAAA to EEEE, or 4R in AAAAEEEE - I use this format of single number, because in Laegna *such projection exists*, because each digit follows in timely manner - for example IO, as it can be represented as Line or Lane from I to O, does *meaningfully equal* counting, and single number as base system scale would do the same; thus, in Laegna it's natural to see *time* in numbers, and thus use some trivial forms - I specifically use two and four digit forms, but not much beyond. It's a little "syntactic sugar".

Creating lanes and lines is not part of this:
- They will be naturally represented in very same numbers, using natural language constructs.
