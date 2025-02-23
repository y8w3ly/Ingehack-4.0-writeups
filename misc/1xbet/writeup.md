# **misc/1xbet**
solves : 8/69
points : 430/500

## **Challenge Description**

There are no losers , only quitters

challenge file : [casino.py](files/casino.py)

connection info : `ncat 1xbet.ctf.ingeniums.club 1337 --ssl`

### Initial Thoughts

+ After reading the source code and connecting to the instance we understand that we must guess the winning number each round :
```
            if user_guess == winning_number  :
                if self.current_round <= self.total_rounds - 1:
                    print("Correct! Moving to the next round.\n")
                elif self.current_round == self.total_rounds :
                    print("u beated the house congrats !!! ")
                    print(f"here is your flag : {FLAG}")
```
+ The winning number is a 32bit number generated with `random.getrandbits`.
+ So we must break the 32bit PRNG with only 6 values to get the 1000 winning numbers.


### Searching

The first thing that I searched for was Breaking PRNG with 6 values.

I found this [article](https://stackered.com/blog/python-random-prediction/) and we understand that we can recover 32bitseed with 6 values and 64bitseed with 8 values.

I got lazy to write a script from scratch so i have directly visited thier github and i found a this repo [python-random-playground](https://github.com/StackeredSAS/python-random-playground.git)


