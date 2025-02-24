from multiprocessing import Pool, cpu_count; import time; from tqdm import tqdm
import googletrans; translator=googletrans.Translator(); import pandas as pd; from datetime import datetime
en = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/train_dh_v2.csv"); print(en.columns)
dial_list=[]; now = datetime.now(); formatted_time=now.strftime("%Y_%m_%d_%H_%M")
with Pool(processes=cpu_count()) as pool:
    for en in tqdm(en.itertuples(), total=len(en)):
        try:
            en2ko_dialogue = translator.translate(en.dialogue, src="ko", dest="en")
            en2ko_summary = translator.translate(en.summary, src="ko", dest="en")     
            dial_list.append([en.fname, en2ko_dialogue, en2ko_summary])
            print(en2ko_summary)        
        except Exception as e:   
            print("error :", e)         
            dial_list.append([en.fname, None, None])
    en2ko_df = pd.DataFrame(dial_list, columns=["fname", "dialogue", "summary"])
    en2ko_df.to_csv(f"/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/googletrans-translate/02_train_{formatted_time}.csv", index=False, encoding="utf-8-sig")
