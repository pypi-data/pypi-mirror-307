import warpper_schnorr
# a = warpper_schnorr.private_key_to_public_key('317zQ7EQptp9nD9xDv6BA39qtF6SPBDzRexFDwbXhrkjzR15Y9Ay9cfVNmNiEy44fZ5tjthMcAs44ypj2m1LLg3X')
a, b = warpper_schnorr.generate_keys_with_seed("hi")
print(a)
print(b)

