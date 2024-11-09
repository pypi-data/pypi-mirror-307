import pandas as pd

og_path = "/home/nfs/syurick/LLM_domain_classifier_inference/justext_resiliparse_trafilatura2/00047_resiliparse_stopwords.jsonl"
hf_path = "/home/nfs/syurick/LLM_domain_classifier_inference/hf_results/00047_resiliparse_stopwords.jsonl"
standard_path = "/home/nfs/syurick/LLM_domain_classifier_inference/standard_results/00047_resiliparse_stopwords.jsonl"

og = pd.read_json(og_path, lines=True).sort_values(by='url')
hf = pd.read_json(hf_path, lines=True).sort_values(by='url')
standard = pd.read_json(standard_path, lines=True).sort_values(by='url')
print(hf.shape)
print(standard.shape)
print(og.shape)
print(hf['domain_pred'].value_counts())
print(standard['domain_pred'].value_counts())

print("*")

og_path = "/home/nfs/syurick/LLM_domain_classifier_inference/justext_resiliparse_trafilatura2/00088_resiliparse_stopwords.jsonl"
hf_path = "/home/nfs/syurick/LLM_domain_classifier_inference/hf_results/00088_resiliparse_stopwords.jsonl"
standard_path = "/home/nfs/syurick/LLM_domain_classifier_inference/standard_results/00088_resiliparse_stopwords.jsonl"

og = pd.read_json(og_path, lines=True).sort_values(by='url')
hf = pd.read_json(hf_path, lines=True)
standard = pd.read_json(standard_path, lines=True)
print(hf.shape)
print(standard.shape)
print(og.shape)
print(hf['domain_pred'].value_counts())
print(standard['domain_pred'].value_counts())

hf_path = "/home/nfs/syurick/LLM_domain_classifier_inference/filtered_hf_results/00088_resiliparse_stopwords.jsonl"
hf = pd.read_json(hf_path, lines=True)
print(hf.shape)
print(hf['domain_pred'].value_counts())
