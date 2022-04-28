# Hardcore 2

```

score: 105 Points
solved: 16/84
difficulty: medium
tags: crypto
```

## Problem
GL!
This is the second and more in-depth part of Hardcore
nc ctf.b01lers.com 9003

Same code as [part1]({Hardcore.md}).

## Got the flag
This is level 2, which has input for probability = 0.9

The main part:

```py
def generate_hardcore(secret, r):
    return int(np.sum(secret * r) % 2)

def predictor(r, probability = 1):
    x_r = (r.copy() != digest_to_array(FLAG))
    np.random.seed(x_r)
    chance = np.random.rand()

    prediction = 0
    if chance <= probability:
        prediction = generate_hardcore(digest_to_array(FLAG), r)
    else:
        prediction = 1 - generate_hardcore(digest_to_array(FLAG), r)

    return int(prediction)
```

base on user input, it returns 0 or 1, which is sum of input * secret, element-wise then
mod 2. So we can guess each character by set it to 1, the rest to 0. If secret
also 1, it returns 1, otherwise returns 0 **with the probability of 90%**.

Instead of check each bit once, we check it 10 times, as the probability is 90%,
we likely get 9 correct answer and 1 wrong answer (maybe 8-2 or 7-3 but not 5-5),
get the bit has more corrects and use it as result.

Iterate throught 256 bits then got result.

Solver script:

```py
TODO
```
