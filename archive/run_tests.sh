#!/bin/bash
#python3 main.py -d intents -i in/in_eng.xlsx -o llama_eng.xlsx -m llama370b -pp prompts/prompt_eng.json
#python3 main.py -d intents -i in/in_sp.xlsx -o llama_eng.xlsx -m llama370b -pp prompts/prompt_eng.json
#python3 main.py -d intents -i in/in_tr.xlsx -o llama_eng.xlsx -m llama370b -pp prompts/prompt_eng.json

#python3 main.py -d intents_bank -i in/in_bank.xlsx -o gpt35_bank.xlsx -m openai_gpt35 -pp prompts/new_prompts_bank.json
#python3 main.py -d intents_bank -i in/in_bank.xlsx -o gpt4_bank.xlsx -m openai_gpt4 -pp prompts/new_prompts_bank.json
#python3 main.py -d intents_bank -i in/in_bank.xlsx -o gemini_bank.xlsx -m gemini -pp prompts/new_prompts_bank.json
#python3 main.py -d intents_bank -i in/in_bank.xlsx -o llama_bank.xlsx -m llama370b -pp prompts/new_prompts_bank.json




#python3 main.py -d intents_eng -i in/in_eng.xlsx -o gpt35_7_eng.xlsx -m openai_gpt35 -pp prompts/new_prompts_eng.json
#python3 main.py -d intents_de -i in/in_eng.xlsx -o gpt35_7_de.xlsx -m openai_gpt35 -pp prompts/new_prompts_ger.json
#python3 main.py -d intents_sp -i in/in_eng.xlsx -o gpt35_7_sp.xlsx -m openai_gpt35 -pp prompts/new_prompts_sp.json
#python3 main.py -d intents_tr -i in/in_eng.xlsx -o gpt35_7_tr.xlsx -m openai_gpt35 -pp prompts/new_prompts_tr.json

#python3 main.py -d intents_eng -i in/in_eng.xlsx -o gpt4_7_eng.xlsx -m openai_gpt4 -pp prompts/new_prompts_eng.json
#python3 main.py -d intents_de -i in/in_eng.xlsx -o gpt4_7_de.xlsx -m openai_gpt4 -pp prompts/new_prompts_ger.json
#python3 main.py -d intents_sp -i in/in_eng.xlsx -o gpt4_7_sp.xlsx -m openai_gpt4 -pp prompts/new_prompts_sp.json
#python3 main.py -d intents_tr -i in/in_eng.xlsx -o gpt4_7_tr.xlsx -m openai_gpt4 -pp prompts/new_prompts_tr.json

#python3 main.py -d intents_eng -i in/in_eng.xlsx -o gemini_7_eng.xlsx -m gemini -pp prompts/new_prompts_eng.json
#python3 main.py -d intents_de -i in/in_eng.xlsx -o gemini_7_de.xlsx -m gemini -pp prompts/new_prompts_ger.json
#python3 main.py -d intents_sp -i in/in_eng.xlsx -o gemini_7_sp.xlsx -m gemini -pp prompts/new_prompts_sp.json
#python3 main.py -d intents_tr -i in/in_eng.xlsx -o gemini_7_tr.xlsx -m gemini -pp prompts/new_prompts_tr.json

#python3 main.py -d intents_eng -i in/in_eng.xlsx -o llama_7_eng.xlsx -m llama370b -pp prompts/new_prompts_eng.json
#python3 main.py -d intents_de -i in/in_eng.xlsx -o llama_7_de.xlsx -m llama370b -pp prompts/new_prompts_ger.json
#python3 main.py -d intents_sp -i in/in_eng.xlsx -o llama_7_sp.xlsx -m llama370b -pp prompts/new_prompts_sp.json
#python3 main.py -d intents_tr -i in/in_eng.xlsx -o llama_7_tr.xlsx -m llama370b -pp prompts/new_prompts_tr.json






#python3 main.py -d intents -i in/in.xlsx -o gpt35_2nd_3rd.xlsx -m openai_gpt35 -pp prompts/prompts_mod.json > gpt35_2nd_3rd.txt 2>&1 &
#python3 main.py -d intents -i in/in.xlsx -o gpt4_2nd_3rd.xlsx -m openai_gpt4 -pp prompts/prompts_mod.json > gpt4_2nd_3rd.txt 2>&1 &
#python3 main.py -d intents -i in/in.xlsx -o gemini_2nd_3rd.xlsx -m gemini -pp prompts/prompts_mod.json > gemini_2nd_3rd.txt 2>&1 &
#python3 main.py -d intents -i in/in.xlsx -s Unknown -o llama_u_2nd_3rd.xlsx -m llama370b -pp prompts/prompts_mod.json > llama_u_2nd_3rd.txt 2>&1 &
#python3 main.py -d intents -i in/in.xlsx -s GetHumanAssistance -o llama_gha_2nd_3rd.xlsx -m llama370b -pp prompts/prompts_mod.json > llama_gha_2nd_3rd.txt 2>&1 &
#python3 main.py -d intents -i in/in.xlsx -s GetOptionRecommendation -o llama_gor_2nd_3rd.xlsx -m llama370b -pp prompts/prompts_mod.json > llama_gor_2nd_3rd.txt
#python3 main.py -d intents -i in/in.xlsx -s GetPreConfiguration -o llama_gpc_2nd_3rd.xlsx -m llama370b -pp prompts/prompts_mod.json > llama_gpc_2nd_3rd.txt 
#python3 main.py -d intents -i in/in.xlsx -s GetStockAvailability -o llama_gsa_2nd_3rd.xlsx -m llama370b -pp prompts/prompts_mod.json > llama_gsa_2nd_3rd.txt 
#python3 main.py -d intents -i in/in.xlsx -s GetTechnicalInformation -o llama_gti_2nd_3rd.xlsx -m llama370b -pp prompts/prompts_mod.json > llama_gti_2nd_3rd.txt
#python3 main.py -d intents -i in/in.xlsx -o gpt4_3.xlsx -m openai_gpt4 > gpt4_3.txt 2>&1 &
#python3 main.py -d intents -i in/in.xlsx -s Unknown -o llama_3_u.xlsx -m llama370b > llama_u.txt 2>&1
#python3 main.py -d intents -i in/in.xlsx -s GetHumanAssistance -o llama_3_gha.xlsx -m llama370b > llama_gha.txt 2>&1
#python3 main.py -d intents -i in/in.xlsx -s GetOptionRecommendation -o llama_3_gor.xlsx -m llama370b > llama_gor.txt 2>&1
#python3 main.py -d intents -i in/in.xlsx -s GetPreConfiguration -o llama_3_gpc.xlsx -m llama370b > llama_gpc.txt 2>&1
#python3 main.py -d intents -i in/in.xlsx -s GetStockAvailability -o llama_3_gsa.xlsx -m llama370b > llama_gsa.txt 2>&1
#python3 main.py -d intents -i in/in.xlsx -s GetTechnicalInformation -o llama_3_gti.xlsx -m llama370b > llama_gti.txt 2>&1
#python3 main.py -d intents -i in/in.xlsx -s Unknown -o mistral_1.xlsx -m mistral7b > mistral_u.txt 2>&1 
#python3 main.py -d intents -i in/in.xlsx -s GetHumanAssistance -o mistral_1.xlsx -m mistral7b > mistral_gha.txt 2>&1 
#python3 main.py -d intents -i in/in.xlsx -s GetOptionRecommendation -o mistral_1.xlsx -m mistral7b > mistral_gor.txt 2>&1 
#python3 main.py -d intents -i in/in.xlsx -s GetPreConfiguration -o mistral_1.xlsx -m mistral7b > mistral_gpc.txt 2>&1 
#python3 main.py -d intents -i in/in.xlsx -s GetStockAvailability -o mistral_1.xlsx -m mistral7b > mistral_1gsa.txt 2>&1 
#python3 main.py -d intents -i in/in.xlsx -s GetTechnicalInformation -o mistral_1.xlsx -m mistral7b > mistral_gti.txt 2>&1 
#python3 main.py -d intents -i in/in.xlsx -o gemini_3.xlsx -m gemini > gemini_3.txt 2>&1 &
#python3 calculate_f1.py -i gemini_1.xlsx -o f1_gemini_1.json
#python3 calculate_f1.py -i gemini_2.xlsx -o f1_gemini_2.json
#python3 calculate_f1.py -i gemini_3.xlsx -o f1_gemini_3.json
#python3 calculate_f1.py -i gpt4_1.xlsx -o f1_gpt4_1.json
#python3 calculate_f1.py -i gpt4_2.xlsx -o f1_gpt4_2.json
#python3 calculate_f1.py -i gpt4_3.xlsx -o f1_gpt4_3.json
#python3 calculate_f1.py -i gpt4_1.xlsx -o f1_gpt4_1.json
#python3 calculate_f1.py -i gpt4_2.xlsx -o f1_gpt4_2.json
#python3 calculate_f1.py -i gpt4_3.xlsx -o f1_gpt4_3.json
#python3 calculate_f1.py -i llama_1.xlsx -o f1_llama_1.json
#python3 calculate_f1.py -i llama_2.xlsx -o f1_llama_2.json
#python3 calculate_f1.py -i llama_3.xlsx -o f1_llama_3.json
#python3 calculate_f1.py -i mistral_1.xlsx -o f1_mistral_1.json

#Testfall: Prompt und Input in gleicher Sprache
#python3 main.py -d intents_de -i in/in.xlsx -o gpt4_de.xlsx -m openai_gpt4 -pp prompt_de.json
#python3 main.py -d intents_eng -i in/in_eng.xlsx -o gpt4_eng.xlsx -m openai_gpt4 -pp prompt_eng.json
#python3 main.py -d intents_sp -i in/in_sp.xlsx -o gpt4_sp.xlsx -m openai_gpt4 -pp prompt_sp.json
#python3 main.py -d intents_tr -i in/in_tr.xlsx -o gpt4_tr.xlsx -m openai_gpt4 -pp prompt_tr.json

#Testfall: Prompt Englisch und Input in Deutsch, Spanisch, Türkisch
#python3 main.py -d intents_eng -i in/in.xlsx -o gpt4_eng_de.xlsx -m openai_gpt4 -pp prompt_eng.json
#python3 main.py -d intents_eng -i in/in_sp.xlsx -o gpt4_eng_sp.xlsx -m openai_gpt4 -pp prompt_eng.json
#python3 main.py -d intents_eng -i in/in_tr.xlsx -o gpt4_eng_tr.xlsx -m openai_gpt4 -pp prompt_eng.json

#Testfall: Prompt Deutsch und Input in Englisch, Spanisch, Türkisch
#python3 main.py -d intents_de -i in/in_eng.xlsx -o gpt4_de_eng.xlsx -m openai_gpt4 -pp prompt_de.json
#python3 main.py -d intents_de -i in/in_sp.xlsx -o gpt4_de_sp.xlsx -m openai_gpt4 -pp prompt_de.json
#python3 main.py -d intents_de -i in/in_tr.xlsx -o gpt4_de_tr.xlsx -m openai_gpt4 -pp prompt_de.json

#Testfall: Prompt Spanisch und Input in Englisch, Deutsch, Türkisch
#python3 main.py -d intents_sp -i in/in.xlsx -o gpt4_sp_de.xlsx -m openai_gpt4 -pp prompt_sp.json
#python3 main.py -d intents_sp -i in/in_eng.xlsx -o gpt4_sp_eng.xlsx -m openai_gpt4 -pp prompt_sp.json
#python3 main.py -d intents_sp -i in/in_tr.xlsx -o gpt4_sp_tr.xlsx -m openai_gpt4 -pp prompt_sp.json

#Testfall: Prompt Türkisch und Input in Englisch, Deutsch, Spanisch
#python3 main.py -d intents_tr -i in/in.xlsx -o gpt4_tr_de.xlsx -m openai_gpt4 -pp prompt_tr.json
#python3 main.py -d intents_tr -i in/in_eng.xlsx -o gpt4_tr_eng.xlsx -m openai_gpt4 -pp prompt_tr.json
#python3 main.py -d intents_tr -i in/in_sp.xlsx -o gpt4_tr_sp.xlsx -m openai_gpt4 -pp prompt_tr.json


#python3 calculate_f1.py -i gpt4_de.xlsx -o f1_gpt4_de.json
#python3 calculate_f1.py -i gpt4_eng.xlsx -o f1_gpt4_eng.json
#python3 calculate_f1.py -i gpt4_sp.xlsx -o f1_gpt4_sp.json
#python3 calculate_f1.py -i gpt4_tr.xlsx -o f1_gpt4_tr.json
#python3 calculate_f1.py -i gpt4_de_eng.xlsx -o f1_gpt4_de_eng.json
#python3 calculate_f1.py -i gpt4_de_sp.xlsx -o f1_gpt4_de_sp.json
#python3 calculate_f1.py -i gpt4_de_tr.xlsx -o f1_gpt4_de_tr.json
#python3 calculate_f1.py -i gpt4_eng_de.xlsx -o f1_gpt4_eng_de.json
#python3 calculate_f1.py -i gpt4_eng_sp.xlsx -o f1_gpt4_eng_sp.json
#python3 calculate_f1.py -i gpt4_eng_tr.xlsx -o f1_gpt4_eng_tr.json
#python3 calculate_f1.py -i gpt4_sp_de.xlsx -o f1_gpt4_sp_de.json
#python3 calculate_f1.py -i gpt4_sp_eng.xlsx -o f1_gpt4_sp_eng.json
#python3 calculate_f1.py -i gpt4_sp_tr.xlsx -o f1_gpt4_sp_tr.json
#python3 calculate_f1.py -i gpt4_tr_de.xlsx -o f1_gpt4_tr_de.json
#python3 calculate_f1.py -i gpt4_tr_eng.xlsx -o f1_gpt4_tr_eng.json
#python3 calculate_f1.py -i gpt4_tr_sp.xlsx -o f1_gpt4_tr_sp.json
