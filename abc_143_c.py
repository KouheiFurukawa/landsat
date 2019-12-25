from sys import stdin

N = int(stdin.readline().rstrip())
S = stdin.readline().rstrip()
ans = 1

for i in range(1, N):
    if S[i - 1] != S[i]:
        ans += 1

print(ans)
