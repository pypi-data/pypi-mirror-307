import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer, AutoConfig
from huggingface_hub import PyTorchModelHubMixin
from dataclasses import dataclass
import pandas as pd


class HFCustomModel(nn.Module, PyTorchModelHubMixin):
    def __init__(self, config):
        super(HFCustomModel, self).__init__()
        self.model = AutoModel.from_pretrained(config['base_model'])
        self.dropout = nn.Dropout(config['fc_dropout'])
        self.fc = nn.Linear(self.model.config.hidden_size, len(config['id2label']))

    def forward(self, input_ids, attention_mask):
        features = self.model(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        dropped = self.dropout(features)
        outputs = self.fc(dropped)
        return torch.softmax(outputs[:, 0, :], dim=1)

@dataclass
class DomainModelConfig:
    model = "microsoft/deberta-v3-base"
    fc_dropout = 0.2
    max_len = 512

class NCCustomModel(nn.Module):
    def __init__(
        self, config, out_dim, config_path=None, pretrained=False, autocast=False
    ):
        super().__init__()
        self.config = config
        if config_path is None:
            self.config = AutoConfig.from_pretrained(
                config.model, output_hidden_states=True
            )
        else:
            self.config = torch.load(config_path)
        if pretrained:
            self.model = AutoModel.from_pretrained(config.model, config=self.config)
        else:
            self.model = AutoModel(self.config)
        self.fc_dropout = nn.Dropout(config.fc_dropout)
        self.fc = nn.Linear(self.config.hidden_size, out_dim)
        self._init_weights(self.fc)
        self.autocast = autocast

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
            if module.bias is not None:
                module.bias.data.zero_()
        elif isinstance(module, nn.Embedding):
            module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
            if module.padding_idx is not None:
                module.weight.data[module.padding_idx].zero_()
        elif isinstance(module, nn.LayerNorm):
            module.bias.data.zero_()
            module.weight.data.fill_(1.0)

    def feature(self, input_ids, attention_mask):
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_states = outputs[0]
        return last_hidden_states

    # def _forward(self, batch):
    def _forward(self, input_ids, attention_mask):
        feature = self.feature(input_ids, attention_mask)
        output = self.fc(self.fc_dropout(feature))
        output = output.to(torch.float32)
        return torch.softmax(output[:, 0, :], dim=1)

    # def forward(self, batch):
    def forward(self, input_ids, attention_mask):
        if self.autocast:
            with torch.autocast(device_type="cuda"):
                return self._forward(input_ids, attention_mask)
        else:
            return self._forward(input_ids, attention_mask)

# Setup configuration and model
config = AutoConfig.from_pretrained("nvidia/domain-classifier")
tokenizer = AutoTokenizer.from_pretrained("nvidia/domain-classifier")
model_hf = HFCustomModel.from_pretrained("nvidia/domain-classifier").eval()

# TODO: Add model.eval()

# model_nc = NCCustomModel(DomainModelConfig, out_dim=26).from_pretrained("/home/nfs/syurick/LLM_domain_classifier_inference/model.pth")
# model_nc = NCCustomModel.from_config(DomainModelConfig)
model_nc = NCCustomModel(
    DomainModelConfig,
    26,
    config_path=None,
    pretrained=True,
    autocast=True,
).eval()
sd = torch.load("/home/nfs/syurick/LLM_domain_classifier_inference/model.pth", map_location="cpu")
if "model_state_dict" in sd:
    sd = sd["model_state_dict"]
sd = {k[7:] if k.startswith("module.") else k: sd[k] for k in sd.keys()}
model_nc.load_state_dict(sd, strict=True)

# Prepare and process inputs
# text_samples = ["Sports is a popular domain", "Politics is a popular domain"]
df_path = "/home/nfs/syurick/LLM_domain_classifier_inference/justext_resiliparse_trafilatura2/00047_resiliparse_stopwords.jsonl"
df = pd.read_json(df_path, lines=True).sort_values(by='url')
text_samples = df.head(20)["text"].tolist()

inputs = tokenizer(text_samples, return_tensors="pt", padding="longest", truncation=True)
# print(inputs)
outputs = model_nc(inputs['input_ids'], inputs['attention_mask'])
# print(outputs)
# Predict and display results
predicted_classes = torch.argmax(outputs, dim=1)
print(predicted_classes)
predicted_domains = [config.id2label[class_idx.item()] for class_idx in predicted_classes.cpu().numpy()]
# print(predicted_domains)
# ['Sports', 'News']

print("********************************")

inputs = tokenizer(text_samples, return_tensors="pt", padding="longest", truncation=True)
#print(inputs)
outputs = model_hf(inputs['input_ids'], inputs['attention_mask'])
#print(outputs)
# Predict and display results
predicted_classes = torch.argmax(outputs, dim=1)
print(predicted_classes)
predicted_domains = [config.id2label[class_idx.item()] for class_idx in predicted_classes.cpu().numpy()]
#print(predicted_domains)
# ['Sports', 'News']
