def gcd(x, y):
  # algorytm euclidesa
  while y > 0:
    x, y = y, x%y
  return x

def xgcd(a, b):
  # rozszerzony algorytm euclidesa
  a, b = max(a, b), min(a, b)

  q = [-1, -1]
  r = [a, b]
  s = [1, 0]
  t = [0, 1]

  while r[-1] > 0:
    q.append(r[-2] // r[-1])
    r.append(r[-2]% r[-1])
    s.append(s[-2] - q[-1] * s[-1])
    t.append(t[-2] - q[-1] * t[-1])

  return s[-2], t[-2]


print(gcd(21, 14))
print(gcd(14, 21))

print(gcd(77, 30))

#print(xgcd(77, 30))
a, base = 600, 1050
inv = xgcd(a, base)
print(inv)

print(f'extended euclidian: ax + by = gcd(a, b) : {a} * {inv[1]} + {base} * {inv[0]} = {gcd(a, base)}')
print(f'{gcd(a, base)} = {base * inv[0] + a * inv[1]}')
print(f'inverse of {a} in ring of int {base} is {inv[1]}')
print(f'{a} * {inv[1]} = {a * inv[1]} % {base} = {(a * inv[1]% base)}')