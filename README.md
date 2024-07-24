# Explaining Automated Reasoning (of Equality Theory) with Proof of Equivalence

<img src="https://github.com/labyrinthinesecurity/zircuit/blob/main/zircuit.png" width="50%">

*zircuit* aims at easing the life of humans reviewing automated proofs made with Equality Theory. It was designed for reviewing clusters of Azure SPNs sharing the same RBAC role definitions, but it can be generalized for any kind of reviews, as long as the input file sticks to the JSON format explained below.

## Proof of Equivalence (PoE)

Any two elements a and b are equivalent if and only if a chain of equalities can be found to link them together. This "circuit" is a proof that a and b belong to the same equivalence class, even when the relation is not obvious because the chain is long.

## JSON input format: FEATHER

The input format is very, very simple and straightfoward: it's a historical timeline of atomic operations ("Ops") performed by the solver. Ops can be of 3 kinds:
- create (C): puts an element in a new equivalence class if it cannot fit elsewhere
- merge (M): merges two equivalence classes into one if they share a common element
- grow (G): puts an element into an existing equivalence class if it can be equated to one of the elements of the class

After each operation is performed, the fresh list of resulting equivalence classes is dumped: here is an example showing a single equivalence class featuring two class members called "a" and "b":
```
"classes": [
          [
            "a","g"
          ]
```

Take a look at test_samples/test1.json for a concrete example.

## Run test sample(s)

### First test (test1.json)
./z.py --filename test_samples/test1.json --name RG0 --origin a --endpoint b

```
*** Proof Of Equivalence between a and b ***

(1) a -[G]-> g
(7) g -[M]-> b
```

To prove that a and b are connected by a chain of equalities, zircuit shows that:
- a is connected to g at time (1) by adding a to the equivalence class of g through the GROW operation (because a is alone in its class)
- g is connected to b at time (7) by adding g to the equivalence class of b through the MERGE operation (because g is not alone in its class, so its whole class is merged with the class of b into a single new class)

### Second test (test2.json)
./z.py --filename test_samples/test2.json --name RG0 --origin a --endpoint h

```
*** Proof Of Equivalence between a and h ***

(1) a -[G]-> b
(8) b -[M]-> d
(4) d -[G]-> e
(9) e -[G]-> h
```
  
