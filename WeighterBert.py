import datasets  # pip install datasets
import nltk
import re
from sentence_transformers import SentenceTransformer, models
from sentence_transformers.datasets import DenoisingAutoEncoderDataset
from torch.utils.data import DataLoader
from sentence_transformers.losses import DenoisingAutoEncoderLoss

nltk.download('punkt')

oscar = datasets.load_dataset(
    'oscar',
    'unshuffled_deduplicated_en',
    split='train',
    streaming=True
)

for row in oscar:
    break
row



splitter = re.compile(r'\.\s?\n?')
splitter.split(row['text'])[:10]
num_sentences = 0
sentences = []
for row in oscar:
    new_sentences = splitter.split(row['text'])
    new_sentences = [line for line in new_sentences if len(line) > 10]
    # we will need a list of sentences (remove too short ones above)
    sentences.extend(new_sentences)
    # the full OSCAR en corpus is huge, we don't need all that data
    num_sentences += len(new_sentences)
    if num_sentences > 100_000:
        # Sentence transformers recommends 10-100K sentences for training
        break



# dataset class with noise functionality built-in
train_data = DenoisingAutoEncoderDataset(sentences)

# we use a dataloader as usual
loader = DataLoader(train_data, batch_size=8, shuffle=True, drop_last=True)


bert = models.Transformer('bert-base-uncased')
pooling = models.Pooling(bert.get_word_embedding_dimension(), 'cls')

model = SentenceTransformer(modules=[bert, pooling])
model


loss = DenoisingAutoEncoderLoss(model, tie_encoder_decoder=True)

model.fit(
    train_objectives=[(loader, loss)],
    epochs=1,
    weight_decay=0,
    scheduler='constantlr',
    optimizer_params={'lr': 3e-5},
    show_progress_bar=True
)

model.save('output/tsdae-bert-base-uncased')



