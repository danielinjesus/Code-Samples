import os
if not os.path.exists(RESULT_PATH):
	os.makedirs(RESULT_PATH)
	file_name = os.path.splitext(os.path.basename(__file__))[0]
	formatted_time = now.strftime("%Y_%m_%d_%H_%M")
	output.to_csv(f"{RESULT_PATH}/{file_name}_{formatted_time}_output_solar.csv", index=False, encoding='utf-8-sig')