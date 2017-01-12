import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('testnu.csv')
df.plot(x='Timestamp', y=['Current', 'MVoltage', 'Sl1Voltage', 'Sl2Voltage', 'Sl3Voltage'])

plt.show()
