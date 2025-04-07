####################### 라이브러리 일괄 설치 #######################
import wandb, random, time
from pathlib import Path
wandb_dir = Path(__file__).resolve().parent / "wandb_logs"
wandb_dir.mkdir(parents=True, exist_ok=True)
#%%
epochs = 140; lr = 0.01
formatted_time = time.time().strftime("%Y_%m_%d_%H_%M")
# %%


# from lightning.pytorch.