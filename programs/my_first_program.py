from nada_dsl import *

def nada_secure_min(party1, party2):
    """
    Calculates the minimum of two secret integers securely using NADA.

    Args:
        party1: The first party holding a secret integer.
        party2: The second party holding a secret integer.

    Returns:
        A list containing an Output object for the securely computed minimum.
    """

    my_int1 = SecretInteger(Input(name="my_int1", party=party1))
    my_int2 = SecretInteger(Input(name="my_int2", party=party2))

    # Secure comparison using shared secret
    shared_secret = SharedSecret(name="shared_secret")

    # Generate random bits for masking
    random_bit1 = SharedBit(Input(name="random_bit1"))
    random_bit2 = SharedBit(Input(name="random_bit2"))

    masked_int1 = my_int1 ^ (shared_secret & random_bit1)
    masked_int2 = my_int2 ^ (shared_secret & random_bit2)

    # Secure comparison using boolean sharing
    comparison = LessThan(masked_int1, masked_int2)

    # Reveal the minimum to the appropriate party
    min_reveal = Reveal(Select(comparison, my_int1, my_int2))
    if party1 == min_reveal.party:
        return [Output(min_reveal, "min_value", party1)]
    else:
        return [Output(min_reveal, "min_value", party2)]

# Example usage (assuming separate executions by party1 and party2)
if __name__ == "__main__":
    party1_output = nada_secure_min(Party(name="Party1"), Party(name="Party2"))
    party2_output = nada_secure_min(Party(name="Party2"), Party(name="Party1"))

    # Simulate secure computation environment (replace with actual execution)
    print(f"Party 1 receives the minimum: {party1_output[0].value}")
    print(f"Party 2 receives the minimum: {party2_output[0].value}")
