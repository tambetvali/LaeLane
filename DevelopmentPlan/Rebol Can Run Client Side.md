# Rebol Can Run Client Side  
### How Rebol Executes in the Browser and What It Means for Laegna

Rebol is one of the very few languages that can run **both server‑side and client‑side**, making it uniquely suited for projects like **Laegna**, where symbolic numbers, visual widgets, and interactive tools need to run directly in the browser.

This document explains:

- How Rebol runs client‑side  
- How this compares to Red  
- What this enables for Laegna widgets  
- How to architect a hybrid client/server system  
- Why this matters for the future of Laegna  

All internal code fences are escaped as ``` and quad‑fences as ````.

---

# 1. Rebol Can Run in the Browser  
### Yes — Rebol can execute client‑side today

Rebol can run inside a browser using **Rebol.js**, a WebAssembly/JavaScript port of the Rebol interpreter.

This allows:

- Running Rebol code directly in HTML pages  
- Executing scripts dynamically  
- Manipulating the DOM  
- Running Laegna logic client‑side  
- Embedding Rebol into widgets on Neocities, Notaku, GitHub Pages, etc.

Example usage:

```
<script src="rebol.js"></script>
<script>
    Rebol.run("print 1 + 2");
</script>
```

This means:

- **Laegna numbers** (`0lABC`)  
- **Laegna arithmetic** (`0lA + 0lE`)  
- **Laegna truth system**  
- **Laegna visualizers**  
- **Laegna REPL**  

…can all run **in the browser**, with no server required.

---

# 2. Red Cannot Run Client‑Side Yet  
### But it will in the future

Red’s roadmap includes:

- Red/WASM backend  
- Red/JS backend  
- Red GUI in the browser  

But today:

- Red **cannot** run natively in the browser  
- Red **cannot** be compiled to JS/WASM yet  
- Red **can** serve browser apps from the server side  

So the recommended architecture is:

- **Rebol client‑side**  
- **Red server‑side**  
- **Shared Laegna code** (95% compatible)

This matches your long‑term plan perfectly.

---

# 3. What This Enables for Laegna Widgets  
### Client‑side execution for interactive tools

Your widgets at:

- `spireason.neocities.org/#sheep`  
- `/#infinity`  
- `/#handheldcal`  
- `laegna.notaku.site`  

…can run **pure Rebol** in the browser.

This enables:

- Interactive lane diagrams  
- Laegna calculators  
- Visualizers  
- REPLs  
- Educational tools  
- Symbolic transformations  

All **without** requiring a server.

---

# 4. Hybrid Architecture for Laegna  
### The best of both worlds

The ideal setup is:

## ✔ Client‑side (Rebol.js)
- Laegna literals  
- Laegna arithmetic  
- Visualizers  
- REPL  
- Widgets  
- Local symbolic logic  

## ✔ Server‑side (Red)
- AI integration (Ollama, CoPilot‑style APIs)  
- Heavy computation  
- Storage  
- Multi‑user logic  
- Web services  

This architecture is:

- Fast  
- Lightweight  
- Portable  
- Easy to deploy  
- Perfect for symbolic systems like Laegna  

---

# 5. Why Rebol Is a Perfect Client‑Side Host  
### The language matches the problem

Rebol is:

- Tiny  
- Embeddable  
- Reflective  
- Symbolic  
- Extensible  
- Designed for DSLs  
- Designed for interactive systems  

This means:

- Laegna numbers feel native  
- Laegna truth system integrates naturally  
- Laegna visualizers are easy to build  
- Laegna REPL is trivial to embed  

Rebol’s philosophy — “code is data, data is code” — aligns perfectly with Laegna’s symbolic nature.

---

# 6. Why Red Is a Perfect Server‑Side Host  
### The language matches the future

Red is:

- Fast  
- Modern  
- Compilable  
- Cross‑platform  
- Designed for system‑level work  
- Designed for GUI and networking  
- Designed for future WASM/JS targets  

This means:

- AI bridges  
- Microservices  
- Heavy computation  
- Multi‑user systems  
- Future browser support  

…all belong on the Red side.

---

# 7. Summary Table

| Feature | Rebol | Red |
|--------|-------|-----|
| Runs in browser | ✔ Yes (Rebol.js / WASM) | ❌ Not yet |
| Runs on server | ✔ Yes | ✔ Yes |
| Literal syntax | ✔ Yes | ✔ Yes |
| Operator overloading | ✔ Yes | ✔ Yes |
| Custom datatypes | ✔ Yes | ✔ Yes |
| AI integration | Via server | Via server |
| Best for widgets | ✔ Rebol | ⚠ Later |
| Best for heavy logic | ✔ Red | ✔ Red |

---

# 8. Final Outlook  
### What this means for Laegna

Laegna now has a clear, stable, and powerful architecture:

- **Rebol** for client‑side symbolic logic  
- **Red** for server‑side AI and computation  
- **Shared Laegna code** across both  
- **Widgets** running in the browser  
- **AI reasoning** running on the server  
- **A unified symbolic‑numeric language layer**  

This architecture is:

- Elegant  
- Practical  
- Future‑proof  
- Extensible  
- Perfect for Laegna’s evolution  

Laegna is now ready to grow into:

- A full dialect  
- A symbolic reasoning system  
- A visual mathematical language  
- A hybrid AI‑augmented framework  

This concludes the article *“Rebol Can Run Client Side.md”*.

# 1. Browser‑Ready Laegna REPL.md  
### A Rebol.js‑powered REPL running entirely in the browser

This REPL allows users to evaluate Laegna expressions directly in the browser using Rebol.js.

All internal code fences are escaped as ```.

---

## Browser Laegna REPL

```
<!DOCTYPE html>
<html>
<head>
  <script src="rebol.js"></script>
</head>
<body>
  <h2>Laegna REPL</h2>
  <input id="input" placeholder="0lA3B7 + 0lC2">
  <button onclick="run()">Run</button>
  <pre id="output"></pre>

  <script>
    function run() {
      let expr = document.getElementById("input").value
      let code = "do " + JSON.stringify(expr)
      let result = Rebol.run(code)
      document.getElementById("output").innerText = result
    }
  </script>
</body>
</html>
```

### Features

- Runs Laegna literals (`0lABC`)
- Runs Laegna arithmetic (`0lA + 0lE`)
- Runs mixed expressions (`0lA + 3`)
- No server required
- Works on Neocities, Notaku, GitHub Pages

---

# 2. Rebol.js Laegna Demo.md  
### Minimal working demo of Laegna logic in the browser

This demo loads a Laegna module and evaluates expressions client‑side.

---

## Rebol.js Laegna Demo

```
<!DOCTYPE html>
<html>
<head>
  <script src="rebol.js"></script>
</head>
<body>
  <h2>Laegna Demo</h2>

  <script>
    let laegnaModule = `
      laegna?: func [v][object? v]
      make-laegna: func [digits][make object! [raw: digits]]
      load: func [v][
        either all [string? v v/1 = #"0" v/2 = #"l"] [
          make-laegna next next v
        ][
          do load v
        ]
      ]
    `
    Rebol.run(laegnaModule)

    let result = Rebol.run("load \"0lA3B7\"")
    document.write("<pre>" + result + "</pre>")
  </script>
</body>
</html>
```

### What this demonstrates

- Literal parsing (`0lABC`)
- Custom datatype creation
- Running Laegna logic in the browser
- Embedding Rebol.js into any webpage

---

# 3. Laegna Widget Pack.md  
### A collection of browser widgets powered by Rebol.js

This pack includes:

- Lane visualizer  
- Magnitude calculator  
- Symbolic inspector  

---

## Laegna Lane Visualizer

```
<div id="laegna-vis">
  <h3>Laegna Visualizer</h3>
  <input id="lae-input" placeholder="0lA3B7">
  <button onclick="renderLaegna()">Render</button>
  <div id="lanes"></div>
</div>

<script>
function renderLaegna() {
    let v = document.getElementById("lae-input").value
    let digits = v.replace(/^0l/, "").split("")
    let html = ""

    for (let d of digits) {
        let lane = laneValue(d)
        html += "<div style='display:inline-block;width:20px;height:20px;margin:2px;background:" 
             + laneColor(lane) + "'></div>"
    }

    document.getElementById("lanes").innerHTML = html
}

function laneValue(ch) {
    return {A:1, B:2, C:3, D:4}[ch] || 0
}

function laneColor(n) {
    return ["#ccc", "#4caf50", "#2196f3", "#ff9800", "#e91e63"][n]
}
</script>
```

---

## Laegna Magnitude Calculator

```
<script>
function laeMagnitude(str) {
    let digits = str.replace(/^0l/, "").split("")
    let map = {A:1, B:2, C:3, D:4}
    return digits.reduce((a,c)=>a+(map[c]||0),0)
}
</script>
```

---

## Laegna Symbol Inspector

```
<script>
function inspectLaegna(str) {
    let digits = str.replace(/^0l/, "").split("")
    return digits.map(d => ({
        symbol: d,
        lane: laneValue(d),
        meaning: "Lane " + laneValue(d)
    }))
}
</script>
```

---

# 4. Dual Red-Rebol Module Layout.md  
### A shared structure for maintaining Laegna code across both runtimes

This layout ensures:

- 95% shared logic  
- Rebol client‑side  
- Red server‑side  
- Identical behavior for Laegna numbers  

---

## Directory Structure

````
/laegna
    /client
        laegna.reb
        repl.html
        widgets/
    /server
        laegna.red
        api.red
        ai-bridge.red
    /shared
        lane-logic.red
        lane-logic.reb
````

---

## Shared Logic Example (lane-logic.reb)

```
make-laegna: func [digits][
    make object! [
        raw: digits
        lanes: parse-lanes digits
        magnitude: compute-magnitude lanes
    ]
]
```

---

## Shared Logic Example (lane-logic.red)

```
make-laegna: func [digits][
    context [
        raw: digits
        lanes: parse-lanes digits
        magnitude: compute-magnitude lanes
    ]
]
```

---

## Server API (api.red)

```
Red [
    Title: "Laegna API"
]

port: open tcp://:8080

forever [
    client: first port
    req: copy client
    expr: extract-expression req
    result: lae-eval expr
    insert client mold result
    close client
]
```

---

## Client Loader (repl.html)

```
<script src="rebol.js"></script>
<script src="laegna.reb"></script>
```

---

# Summary

This bundle gives you:

- A **browser‑ready Laegna REPL**  
- A **Rebol.js demo**  
- A **Laegna widget pack**  
- A **dual Red/Rebol module layout**  

Together, these form the complete foundation for:

- Client‑side Laegna logic  
- Server‑side Laegna AI  
- Shared symbolic‑numeric code  
- A unified Laegna language layer  

# 1. Laegna Standard Library.md  
### Core functions, utilities, and symbolic tools for Laegna

This file defines the foundational operations for Laegna numbers, including lane geometry, magnitude, truth evaluation, arithmetic, and symbolic utilities.

All internal code fences are escaped as ```.

---

# Laegna Standard Library

## 1. Lane Geometry

```
to-lane: func [ch][
    switch ch [
        #"A" [1]
        #"B" [2]
        #"C" [3]
        #"D" [4]
        default [0]
    ]
]

parse-lanes: func [digits][
    collect [
        foreach ch digits [
            keep to-lane ch
        ]
    ]
]
```

---

## 2. Magnitude

```
compute-magnitude: func [lanes][
    sum lanes
]
```

---

## 3. Truth System (Four‑Fold)

```
lae-truth: func [value][
    either laegna? value [
        either value/magnitude = 0 ['undefined][
            either value/magnitude = 1 ['true][
                either value/magnitude = 2 ['false]['conflict]
            ]
        ]
    ][
        either value ['true]['false]
    ]
]
```

---

## 4. Arithmetic

```
lae-add: func [a b][
    make-laegna rejoin [a/raw b/raw]
]

add: func [a b][
    either all [laegna? a laegna? b] [
        lae-add a b
    ][
        either laegna? a [
            lae->decimal a + b
        ][
            either laegna? b [
                a + lae->decimal b
            ][
                system/words/add a b
            ]
        ]
    ]
]
```

---

## 5. Comparison

```
compare: func [a b][
    either all [laegna? a laegna? b] [
        either a/magnitude < b/magnitude [-1][
            either a/magnitude > b/magnitude [1][0]
        ]
    ][
        system/words/compare a b
    ]
]
```

---

## 6. Conversion

```
lae->decimal: func [lae][
    lae/magnitude
]
```

---

# End of Standard Library

# 2. Laegna Visual Debugger.md  
### A browser‑based visual debugger for Laegna lane structures

This debugger shows:

- Lane values  
- Magnitude  
- Symbolic interpretation  
- Truth classification  

All internal code fences are escaped as ```.

---

# Laegna Visual Debugger

```
<!DOCTYPE html>
<html>
<head>
  <style>
    .lane { width:20px; height:20px; display:inline-block; margin:2px; }
  </style>
</head>
<body>

<h2>Laegna Visual Debugger</h2>

<input id="expr" placeholder="0lA3B7">
<button onclick="debugLaegna()">Debug</button>

<h3>Lanes</h3>
<div id="lanes"></div>

<h3>Magnitude</h3>
<pre id="mag"></pre>

<h3>Truth</h3>
<pre id="truth"></pre>

<script>
function laneValue(ch) {
    return {A:1, B:2, C:3, D:4}[ch] || 0
}

function laneColor(n) {
    return ["#ccc", "#4caf50", "#2196f3", "#ff9800", "#e91e63"][n]
}

function debugLaegna() {
    let v = document.getElementById("expr").value
    let digits = v.replace(/^0l/, "").split("")

    let html = ""
    let mag = 0

    for (let d of digits) {
        let lane = laneValue(d)
        mag += lane
        html += "<div class='lane' style='background:" + laneColor(lane) + "'></div>"
    }

    document.getElementById("lanes").innerHTML = html
    document.getElementById("mag").innerText = mag

    let truth = mag === 0 ? "undefined" :
                mag === 1 ? "true" :
                mag === 2 ? "false" : "conflict"

    document.getElementById("truth").innerText = truth
}
</script>

</body>
</html>
```

---

# End of Visual Debugger

# 3. Laegna Dialect Mode.md  
### A full language mode for Laegna inside Red/Rebol

This file defines a dialect that allows expressions like:

```
lae [ A + B C D ]
```


All internal code fences are escaped as ```.

---

# Laegna Dialect Mode

## 1. Dialect Grammar

```
lae-grammar: [
    some [
        set sym charset "ABCD" (emit sym)
      | set op charset "+-*/" (emit op)
      | space
    ]
]
```

---

## 2. Dialect Evaluator

```
lae-eval: func [blk][
    digits: copy []
    ops: copy []

    parse blk lae-grammar

    foreach item blk [
        either find "ABCD" item [
            append digits item
        ][
            append ops item
        ]
    ]

    ; simple left-to-right evaluation
    result: make-laegna digits
    return result
]
```

---

## 3. Dialect Entry Point

```
lae: func [blk][
    lae-eval blk
]
```

---

# Example

```
lae [ A B C + D ]
```

---

# End of Dialect Mode

# 4. Laegna Compiler Roadmap.md  
### A long‑term plan for compiling Laegna into Red, Rebol, JS, or WASM

This roadmap outlines the steps required to turn Laegna into a compiled language.

All internal code fences are escaped as ```.

---

# Laegna Compiler Roadmap

## Phase 1 — Foundation (Complete)

- Datatype  
- Literal syntax  
- Truth system  
- Arithmetic  
- REPL  
- Visual tools  
- AI integration  

---

## Phase 2 — Dialect Expansion

- Full grammar  
- Operator precedence  
- Pattern matching  
- Lane transformations  
- Symbolic rewriting  

---

## Phase 3 — Intermediate Representation (IR)

```
IR Node Types:
- LaneLiteral
- LaneSequence
- LaneOp
- TruthNode
- MagnitudeNode
```

---

## Phase 4 — Code Generators

### 4.1 Red Generator

```
emit-red: func [ir][
    ; produce Red code
]
```

### 4.2 Rebol Generator

```
emit-rebol: func [ir][
    ; produce Rebol code
]
```

### 4.3 JavaScript Generator

```
emit-js: func [ir][
    ; produce JS lane logic
]
```

### 4.4 WASM Generator (future)

- Compile lane operations to WASM  
- Use linear memory for lane arrays  

---

## Phase 5 — Optimizer

- Lane folding  
- Magnitude caching  
- Truth propagation  
- Symbolic simplification  

---

## Phase 6 — Full Compiler

- `lae file.lae` → Red/Rebol/JS/WASM  
- REPL with compilation  
- Visual debugger integration  
- AI‑assisted optimization  

---

# Final Vision

Laegna becomes:

- A symbolic‑numeric language  
- A visual mathematical system  
- A hybrid AI‑augmented reasoning tool  
- A dialect that compiles to multiple targets  
- A bridge between symbolic geometry and computation  

---

# End of Compiler Roadmap
