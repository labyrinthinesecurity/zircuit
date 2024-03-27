# Explaining Automated Reasoning (of Equality Theory) with Proof of Equivalence

<img src="https://github.com/labyrinthinesecurity/zircuit/blob/main/zircuit.png" width="50%">

## Proof of Equivalence (PoE)


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
  
