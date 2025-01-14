

# DistilBERT:

# Hugging Face Model Name: distilbert-base-uncased
# PyTorch Model Class: DistilBertModel


def tran_distillbert():
    # 源文件： https://github.com/feldges/TextClassificationWithBert/blob/main/TextClassificationWithBERT.ipynb
    from datetime import datetime

    import numpy as np
    import pandas as pd
    import tensorflow as tf
    import torch
    # distilBERT tokenizer
    import transformers
    from matplotlib import pyplot as plt
    from tensorflow.keras import layers, metrics, models
    from torch import nn
    from tqdm import tqdm

    # from matplotlib import pyplot as plt
    # Download the dataset and put it in subfolder called data
    datapath = "data/bbc-text.csv"
    df = pd.read_csv(datapath)
    df = df[["category", "text"]]

    # Show the data
    df.head()

    print('Total number of news: {}'.format(len(df)))
    print(40*'-')
    print('Split by category:')
    print(df["category"].value_counts())
    print(40*'-')
    nr_categories = len(df["category"].unique())
    print("Number of categories: {n}".format(n=nr_categories))

    # You can adjust n:
    n=100
    print('Category: ',df['category'][n])
    print(100*'-')
    print('Text:')
    print(df['text'][n])

    # Renaming, Input -> X, Output -> y
    X = df['text']
    y=np.unique(df['category'], return_inverse=True)[1]
    print(y)


    tokenizer = transformers.DistilBertTokenizer.from_pretrained('distilbert-base-uncased')


    X_tf = [tokenizer(text, padding='max_length', max_length = 512, truncation=True)['input_ids'] for text in X]
    X_tf = np.array(X_tf, dtype='int32')

    # Train/test split
    from sklearn.model_selection import train_test_split
    X_tf_train, X_tf_test, y_tf_train, y_tf_test = train_test_split(X_tf, y, test_size=0.3, random_state=42, stratify=y)
    print('Shape of training data: ',X_tf_train.shape)
    print('Shape of test data: ',X_tf_test.shape)

    # build the model
    # Get BERT layer
    config = transformers.DistilBertConfig(dropout=0.2, attention_dropout=0.2)
    dbert_tf = transformers.TFDistilBertModel.from_pretrained('distilbert-base-uncased', config=config, trainable=False)

    # Let's create a sample of size 5 from the training data
    sample = X_tf_train[0:5]
    print('Object type: ', type(dbert_tf(sample)))
    print('Output format (shape): ',dbert_tf(sample)[0].shape)
    print('Output used as input for the classifier (shape): ', dbert_tf(sample)[0][:,0,:].shape)


    input_ids_in = layers.Input(shape=(512,), name='input_token', dtype='int32')

    x = dbert_tf(input_ids=input_ids_in)[0][:,0,:]
    x = layers.Dropout(0.2, name='dropout')(x)
    x = layers.Dense(64, activation='relu', name='dense')(x)
    x = layers.Dense(5, activation='softmax', name='classification')(x)

    model_tf = models.Model(inputs=input_ids_in, outputs = x, name='ClassificationModelTF')

    model_tf.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=[metrics.SparseCategoricalAccuracy()])

    model_tf.summary()

    # 训练

    # Train the model
    start_time = datetime.now()
    history = model_tf.fit(X_tf_train, y_tf_train, batch_size=32, shuffle=True, epochs=5, validation_data=(X_tf_test, y_tf_test))
    end_time = datetime.now()

    training_time_tf = (end_time - start_time).total_seconds()

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    ax[0].set(title='Loss')
    ax[0].plot(history.history['loss'], label='Training')
    ax[0].plot(history.history['val_loss'], label='Validation')
    ax[0].legend(loc="upper right")

    ax[1].set(title='Accuracy')
    ax[1].plot(history.history['sparse_categorical_accuracy'], label='Training')
    ax[1].plot(history.history['val_sparse_categorical_accuracy'], label='Validation')
    ax[1].legend(loc="lower right")

    accuracy_tf = history.history['val_sparse_categorical_accuracy'][-1]
    print('Accuracy Training data: {:.1%}'.format(history.history['sparse_categorical_accuracy'][-1]))
    print('Accuracy Test data: {:.1%}'.format(history.history['val_sparse_categorical_accuracy'][-1]))
    print('Training time: {:.1f}s (or {:.1f} minutes)'.format(training_time_tf, training_time_tf/60))

    #保存模型
    model_tf.save('model_tf.h5', save_format='h5')
    model_tf2 = models.load_model('model_tf.h5', custom_objects={'TFDistilBertModel': dbert_tf})
    model_tf2.summary()

    #执行文本分类
    X_list=X.to_list()
    X_pt = tokenizer(X_list, padding='max_length', max_length = 512, truncation=True, return_tensors='pt')["input_ids"]

    y_list=y.tolist()
    y_pt = torch.Tensor(y_list).long()
    #Let's split the dataset into training and test data.
    X_pt_train, X_pt_test, y_pt_train, y_pt_test = train_test_split(X_pt, y_pt, test_size=0.3, random_state=42, stratify=y_pt)
    # We create a Dataset class and will instantiate for both the training and test datasets.

    # Convert data to torch dataset
    from torch.utils.data import DataLoader, Dataset
    class BBCNewsDataset(Dataset):
        """Custom-built BBC News dataset"""

        def __init__(self, X, y):
            """
            Args:
                X, y as Torch tensors
            """
            self.X_train = X
            self.y_train = y


        def __len__(self):
            return len(self.y_train)

        def __getitem__(self, idx):
            return self.X_train[idx], self.y_train[idx]

    # Get train and test data in form of Dataset class
    train_data_pt = BBCNewsDataset(X=X_pt_train, y=y_pt_train)
    test_data_pt = BBCNewsDataset(X=X_pt_test, y=y_pt_test)

    # We embed the datasets into a dataloader, to prepare the dataset to be used for training.

    # Get train and test data in form of Dataloader class
    train_loader_pt = DataLoader(train_data_pt, batch_size=32)
    test_loader_pt = DataLoader(test_data_pt, batch_size=32)

    # ## Build the Model

    # From now we will follow very closely the approach we have used for TensorFlow and try to stick to the same parameters wherever it is possible.

    # Let's build the model. For this we first need to get the BERT layer from the transformer library. We configure it such that its parameters will not be trained during training.

    # Note that we have already defined a config object while building the TensorFlow model. The first line below is therefore not needed. We have added just to allow you to run both models (TensorFlow and PyTorch) independently.

    config = transformers.DistilBertConfig(dropout=0.2, attention_dropout=0.2)
    dbert_pt = transformers.DistilBertModel.from_pretrained('distilbert-base-uncased', config=config)

    # Let's create a sample of size 5 from the training data
    sample = X_pt_train[0:5]
    print('Object type: ', type(dbert_pt(sample)))
    print('Output format (shape): ',dbert_pt(sample)[0].shape)
    print('Output used as input for the classifier (shape): ', dbert_pt(sample)[0][:,0,:].shape)


    # Get cpu or gpu device for training.
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using {device} device")

    class DistilBertClassification(nn.Module):
        def __init__(self):
            super(DistilBertClassification, self).__init__()
            self.dbert = dbert_pt
            self.dropout = nn.Dropout(p=0.2)
            self.linear1 = nn.Linear(768,64)
            self.ReLu = nn.ReLU()
            self.linear2 = nn.Linear(64,5)

        def forward(self, x):
            x = self.dbert(input_ids=x)
            x = x["last_hidden_state"][:,0,:]
            x = self.dropout(x)
            x = self.linear1(x)
            x = self.ReLu(x)
            logits = self.linear2(x)
            # No need for a softmax, because it is already included in the CrossEntropyLoss
            return logits

    model_pt = DistilBertClassification().to(device)

    print(model_pt)


    for param in model_pt.dbert.parameters():
        param.requires_grad = False


    total_params = sum(p.numel() for p in model_pt.parameters())
    total_params_trainable = sum(p.numel() for p in model_pt.parameters() if p.requires_grad)
    print("Number of parameters: ", total_params)
    print("Number of trainable parameters: ", total_params_trainable)

    epochs = 5
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model_pt.parameters())


    # Define the dictionary "history" that will collect key performance indicators during training
    history = {}
    history["epoch"]=[]
    history["train_loss"]=[]
    history["valid_loss"]=[]
    history["train_accuracy"]=[]
    history["valid_accuracy"]=[]

    # Measure time for training
    start_time = datetime.now()

    # Loop on epochs
    for e in range(epochs):

        # Set mode in train mode
        model_pt.train()

        train_loss = 0.0
        train_accuracy = []

        # Loop on batches
        for X, y in tqdm(train_loader_pt):

            # Get prediction & loss
            prediction = model_pt(X)
            loss = criterion(prediction, y)

            # Adjust the parameters of the model
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

            prediction_index = prediction.argmax(axis=1)
            accuracy = (prediction_index==y)
            train_accuracy += accuracy

        train_accuracy = (sum(train_accuracy) / len(train_accuracy)).item()

        # Calculate the loss on the test data after each epoch
        # Set mode to evaluation (by opposition to training)
        model_pt.eval()
        valid_loss = 0.0
        valid_accuracy = []
        for X, y in test_loader_pt:

            prediction = model_pt(X)
            loss = criterion(prediction, y)

            valid_loss += loss.item()

            prediction_index = prediction.argmax(axis=1)
            accuracy = (prediction_index==y)
            valid_accuracy += accuracy
        valid_accuracy = (sum(valid_accuracy) / len(valid_accuracy)).item()

        # Populate history
        history["epoch"].append(e+1)
        history["train_loss"].append(train_loss / len(train_loader_pt))
        history["valid_loss"].append(valid_loss / len(test_loader_pt))
        history["train_accuracy"].append(train_accuracy)
        history["valid_accuracy"].append(valid_accuracy)

        print(f'Epoch {e+1} \t\t Training Loss: {train_loss / len(train_loader_pt) :10.3f} \t\t Validation Loss: {valid_loss / len(test_loader_pt) :10.3f}')
        print(f'\t\t Training Accuracy: {train_accuracy :10.3%} \t\t Validation Accuracy: {valid_accuracy :10.3%}')

    # Measure time for training
    end_time = datetime.now()
    training_time_pt = (end_time - start_time).total_seconds()


    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    ax[0].set(title='Loss')
    ax[0].plot(history['train_loss'], label='Training')
    ax[0].plot(history['valid_loss'], label='Validation')
    ax[0].legend(loc="upper right")

    ax[1].set(title='Accuracy')
    ax[1].plot(history['train_accuracy'], label='Training')
    ax[1].plot(history['valid_accuracy'], label='Validation')
    ax[1].legend(loc="lower right")

    accuracy_pt = history['valid_accuracy'][-1]
    print('Accuracy Training data: {:.1%}'.format(history['train_accuracy'][-1]))
    print('Accuracy Test data: {:.1%}'.format(history['valid_accuracy'][-1]))
    print('Training time: {:.1f}s (or {:.1f} minutes)'.format(training_time_pt, training_time_pt/60))

    ## Save the Model
    # Save only the parameters of the model but not the model itself, and get it back
    torch.save(model_pt.state_dict(), 'PyModel.sd')
    model_reloaded = DistilBertClassification()
    model_reloaded.load_state_dict(torch.load('PyModel.sd'))
    model_reloaded.eval()

    # Save the entire model, and get it back
    torch.save(model_pt, 'PyModelComplete.pt')
    model_reloaded2 = torch.load('PyModelComplete.pt')
    model_reloaded2.eval()
