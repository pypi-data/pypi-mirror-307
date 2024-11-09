import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer, AutoConfig
from huggingface_hub import PyTorchModelHubMixin

# rapids-24.04 on ipp1-3303

cache_dir = "/home/nfs/syurick/hf_cache"

class CustomModel(nn.Module, PyTorchModelHubMixin):
    def __init__(self, config):
        super(CustomModel, self).__init__()
        self.model = AutoModel.from_pretrained(config['base_model'], cache_dir=cache_dir)
        self.dropout = nn.Dropout(config['fc_dropout'])
        self.fc = nn.Linear(self.model.config.hidden_size, len(config['id2label']))

    def forward(self, input_ids, attention_mask):
        features = self.model(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        dropped = self.dropout(features)
        outputs = self.fc(dropped)
        return torch.softmax(outputs[:, 0, :], dim=1)

# Setup configuration and model
config = AutoConfig.from_pretrained("nvidia/domain-classifier", cache_dir=cache_dir)
tokenizer = AutoTokenizer.from_pretrained("nvidia/domain-classifier", cache_dir=cache_dir)
model = CustomModel.from_pretrained("nvidia/domain-classifier", cache_dir=cache_dir)

# Prepare and process inputs
text_samples = ["Sports is a popular domain", "Politics is a popular domain"]
inputs = tokenizer(text_samples, return_tensors="pt", padding="longest", truncation=True)
print(inputs)
outputs = model(inputs['input_ids'], inputs['attention_mask'])
print(outputs)

# Predict and display results
predicted_classes = torch.argmax(outputs, dim=1)
print(predicted_classes)
predicted_domains = [config.id2label[class_idx.item()] for class_idx in predicted_classes.cpu().numpy()]
print(predicted_domains)
# ['Sports', 'News']
