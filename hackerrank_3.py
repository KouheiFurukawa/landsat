import sys
import numpy as np

data = []
for l in sys.stdin:
    data.append(l.rstrip().split(','))
ans = []
score = np.array([0] * len(data[0]))

for i in range(len(data)):
    if i == 0:
        ans.append(','.join(data[i]))
    else:
        for j in range(len(data[0])):
            score[j] += float(data[i][j])

score = score / (len(data) - 1)
ans.append(','.join([str(int(np.round(x))) for x in score]))
print(ans[0])
print(ans[1])
