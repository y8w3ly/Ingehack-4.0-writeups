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

+ The first thing that I searched for was Breaking PRNG with 6 values.
+ After the search, I found this [article](https://stackered.com/blog/python-random-prediction/) in the head of the results, and after reading it we understand that we can recover 32bitseed with 6 values and 64bitseed with 8 values.
+ I got lazy to write a script from scratch so i have directly visited thier github and i found a this repo [python-random-playground](https://github.com/StackeredSAS/python-random-playground.git)
+ The scripts that we need are named [recover_32bitSeed.py](files/recover_32bitSeed.py) and [functions.py](files/casino.py)

### Final solve script

+ After having all what we need the only remaining step is to write a solve script. Beacause of my bad scripting skills, I tried many times to write a solve script and i just got many issues one of them is that mersenne implementation recovers two seeds one of them is the wrong seed. my teammate [Koyphshi](https://github.com/LanacerYasser) has solved this  by testing the 6 values that we got with the indexes of what we generated. I can't believe that I didn't think of this : 
```
for seed in (seed1, seed2):
        random.seed(seed)
        predicted = [random.getrandbits(32) for _ in range(1000)]
        if (predicted[0] == outputs[0] and predicted[227] == outputs[227] and
            predicted[1] == outputs[1] and predicted[228] == outputs[228] and
            predicted[2] == outputs[2] and predicted[229] == outputs[229]):
            trueseed = seed
            break
```

+ Then after getting all the 1000 values we send them one by one : 
```
for i in range(1000):
        io.sendlineafter(b"Guess the number: ",str(predicted[i]).encode())
        response = io.recvline().decode().strip()
        log.info("Round {}: {}".format(i+1, response))
    io.interactive()
```

+ After getting all the 1000 correct guesses we get the Flag : `ingehack{PYThON_rANdOm_1SNt_tH4T_$3cuRE_AFTER_4lL_$h0uT0uT_t0_MeRs3nn3}`

The full solve script can be found [here](files/solve.py)