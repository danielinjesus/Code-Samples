import pandas as pd; import matplotlib.pyplot as plt; import seaborn as sns
test_result = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/Daun/dev/leng.csv")

test_result['summary_len'] = test_result['summary'].apply(lambda x: len(x))

sns.histplot(test_result['summary_len'], kde=True, bins=30, alpha=0.6, color='blue')
plt.title('Daun - length'); plt.xlabel('length'); plt.ylabel('Frequency'); plt.show()