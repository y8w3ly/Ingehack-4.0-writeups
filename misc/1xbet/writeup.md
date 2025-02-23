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
+ The winning number is a 32bit number generated with random.getrandbits .
+ So we must break the 32bit PRNG with only 6 values.


