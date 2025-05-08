from datasets import load_dataset, ClassLabel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
import transformers


# 1. Carrega o dataset CSV
dataset = load_dataset('csv', data_files={'train': r'C:\Users\RLima\OneDrive\Documentos\VS CODE\APS - NLP\APS---NLP\Backend\BART\newdataset.csv'}, delimiter=',')

# 2. Verifica e converte o label para inteiro, se necessário
def label_to_int(example):
    label_map = {'negativa': 0, 'irrelevante': 1, 'positiva': 2}
    label = example['label'].strip()  # Remove espaços em branco
    example['label'] = label_map[label]
    return example


dataset = dataset.map(label_to_int)

# 3. Carrega o tokenizer do modelo
model_name = "neuralmind/bert-base-portuguese-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 4. Tokeniza os textos
def preprocess_function(examples):
    return tokenizer(examples['texto'], truncation=True, padding='max_length', max_length=512)

tokenized_dataset = dataset['train'].map(preprocess_function, batched=True)

# 5. Carrega o modelo para classificação binária
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

# 6. Defina os argumentos de treinamento
training_args = TrainingArguments(
    output_dir="./results_bert_pt_final",
    eval_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    save_strategy="no",
    logging_dir='./logs_bert_pt',
    logging_steps=100,
)

# 7. Função de métricas
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        'accuracy': accuracy_score(labels, predictions),
        'f1_macro': f1_score(labels, predictions, average='macro'),
        'f1_weighted': f1_score(labels, predictions, average='weighted')
    }

# 8. Treinador
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,  # Ideal: separar um conjunto de validação
    compute_metrics=compute_metrics,
)

# 9. Treinamento
trainer.train()

# 10. Salve o modelo ajustado
trainer.save_model("./bart_tunado")
tokenizer.save_pretrained("./bart_tunado")