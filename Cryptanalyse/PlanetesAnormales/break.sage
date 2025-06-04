# From https://github.com/elikaski/ECC_Attacks?tab=readme-ov-file#the-curve-is-anomalous

import sys

# Constants
p = 0xf7fda1b2f0c9ea506e8a125766fd9e5046fd5716630c84f526fea8ce10497829
a = 0xbb0480e1f010abb2e69e7d72df5d75a23a15bc73710df25b6da04121f904e4f5
b = 0xfa2bddcca24c1d80baf26cb1e1f04cf78e995c675543c9692e959f83b470a03
G = (0x735d07d96821ec8bff37eb23c31081ea526ddc10abe22375518c44e043a39db0, 0x97e570cf7c177584ddd036d9181a3f5f83307f60c92b539a2d4f479d9c9ad4bd)

#################################################################################

E = EllipticCurve(GF(p), [a,b])
G = E(G[0], G[1])

# Anomalous Curve check
assert E.order() == p


def lift(P, E, p):
    # lift point P from old curve to a new curve
    Px, Py = map(ZZ, P.xy())
    for point in E.lift_x(Px, all=True):
         # take the matching one of the 2 points corresponding to this x on the p-adic curve
        _, y = map(ZZ, point.xy())
        if y % p == Py:
            return point


# Main program

args = sys.argv[1:]

# Unknown point
P = E(int(args[0]), int(args[1]))

# Lift the points to some new curve over p-adic numbers
E_adic = EllipticCurve(Qp(p), [a+p*13, b+p*37]) 
G = p * lift(G, E_adic, p)
P = p * lift(P, E_adic, p)

# Calculate discrete log
Gx, Gy = G.xy()
Px, Py = P.xy()
found_key = int(GF(p)((Px / Py) / (Gx / Gy)))

print(found_key)