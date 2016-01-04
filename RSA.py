# Same output with the JS RSA encryptString function on http://www.ohdave.com/rsa/
public_modulus_hex1 = 'b1ad50d3d9ac3a2506c83dca3750b291f9f1f3275c4fee0f140bd6a98679e2fa5017802a1983b74e0c3937310de118f64ef00a7f2d2a4fbf58698f958abc9b048a9228c5b094bd5bf27b08050d1773e728a70046b5725f2b59fd73c687875da323067a9a79c7d5df1f032286b39b85786c165160314f213b3b2d01fb2c2d9ab55e1afad08157da6e14a11c3814a2b8ef166d58cfd9a0aca7ceefe0aa591b15e268eb087923fb13befa58afd9359dc4b4cb9698c1f02d2f7fe05c92f8811ffb8985c47696199d2b0d56433f9ef9dd5f61151238e4bec842cc3e9e6cf6d2656fcefd8a74d05ccd40cda1860d6b556f6b0f3580a91ca517e96f6714bac5df2fc6db'
public_exponent_hex1 = '10001'


def encrypt(plaintext_text, public_modulus_hex, public_exponent_hex):
    public_modulus = int(public_modulus_hex, 16)
    public_exponent = int(public_exponent_hex, 16)
    # Beware, plaintext must be short enough to fit in a single block!
    plaintext = int(plaintext_text[::-1].encode('hex'), 16)
    ciphertext = pow(plaintext, public_exponent, public_modulus)
    return '%X' % ciphertext # return hex representation

