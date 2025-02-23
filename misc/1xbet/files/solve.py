from pwn import *
from functions import untemper, invertStep, recover_Kj_from_Ii  
import random

def recover_seed(outputs):
    state0   = untemper(outputs[0])
    state227 = untemper(outputs[227])
    state1   = untemper(outputs[1])
    state228 = untemper(outputs[228])
    state2   = untemper(outputs[2])
    state229 = untemper(outputs[229])
    
    I_227_, I_228 = invertStep(state0, state227)
    I_228_, I_229 = invertStep(state1, state228)
    I_229_, I_230 = invertStep(state2, state229)

    I_228 += I_228_
    I_229 += I_229_
    
    seed1 = recover_Kj_from_Ii(I_230, I_229, I_228, 230)
    seed2 = recover_Kj_from_Ii(I_230 + 0x80000000, I_229, I_228, 230)
    
    return seed1, seed2

def main():
    
    io = remote("1xbet.ctf.ingeniums.club", 1337, ssl=True)
    
    io.recvuntil(b"preview (e.g., 0,10,100): ")
    io.sendline(b"0,227,1,228,2,229")
    
    header = io.recvline().decode().strip()
    print(header)
    
    outputs = {}
    
    while len(outputs) < 6:
         line = io.recvline().decode().strip()
         if line.startswith("Index"):
            parts = line.split(":")
            index = int(parts[0].split()[1])
            number = int(parts[1].strip(), 0)
            outputs[index] = number
    
    chosen_indices = [0, 227, 1, 228, 2, 229]
    preview_numbers = [outputs[i] for i in chosen_indices]
    
    
    seed1, seed2 = recover_seed({0: preview_numbers[0],
                                 227: preview_numbers[1],
                                 1: preview_numbers[2],
                                 228: preview_numbers[3],
                                 2: preview_numbers[4],
                                 229: preview_numbers[5]})
                                 
    
    for seed in (seed1, seed2):
        random.seed(seed)
        predicted = [random.getrandbits(32) for _ in range(1000)]
        if (predicted[0] == outputs[0] and predicted[227] == outputs[227] and
            predicted[1] == outputs[1] and predicted[228] == outputs[228] and
            predicted[2] == outputs[2] and predicted[229] == outputs[229]):
            trueseed = seed
            break

    for i in range(1000):
        io.sendlineafter(b"Guess the number: ",str(predicted[i]).encode())
        response = io.recvline().decode().strip()
        log.info("Round {}: {}".format(i+1, response))
    
    io.interactive()

if __name__ == "__main__":
    main()
