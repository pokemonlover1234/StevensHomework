import pickle, gzip
from keras import layers, models, losses
import matplotlib.pyplot as plt

class Conv():
    def __init__(self, fname):
        f = gzip.open(fname, 'rb')
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        train_set, valid_set, test_set = u.load()
        self.train_images, self.train_labels = train_set
        self.valid_images, self.valid_labels = valid_set
        self.test_images, self.test_labels = test_set
        self.train_images = self.train_images.reshape((50000, 28, 28, 1))
        self.valid_images = self.valid_images.reshape((10000, 28, 28, 1))
        self.test_images = self.test_images.reshape((10000, 28, 28, 1))
        self.train_labels = self.train_labels.reshape((50000, 1))
        self.valid_labels = self.valid_labels.reshape((10000, 1))
        self.test_labels = self.test_labels.reshape((10000, 1))
        f.close()
        self.setup_layers()
        self.model.compile(optimizer='adam', loss=losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
        self.epoch = 0
        self.tol = 0.0005
        self.best_accuracy = 0

    
    # Sets up the convolutional neural network
    def setup_layers(self):
        model = models.Sequential()
        model.add(layers.Conv2D(32, (7, 7), activation='relu', input_shape=(28, 28,1)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (5, 5), activation = 'relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation = 'relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(10))
        self.model = model


    # Runs a single epoch of training
    # Returns the history object returned by the iteration
    def run_epoch(self):
        h = self.model.fit(self.train_images, self.train_labels, verbose=1, validation_data=(self.valid_images, self.valid_labels), initial_epoch=self.epoch, epochs=self.epoch+1)
        self.epoch += 1
        return h


    # Run training to completion. 
    # Applies early stopping if no significant
    # improvement over best validation accuracy
    # ocurred over last 4 iterations. 
    # Displays a plot of train, validation, and test errors
    # Stores best model as self.best_model for future use.
    def run_training(self):
        train_errs = []
        valid_errs = []
        test_errs = []
        iters_since_last_sigimprove = 0
        best_val = 0
        best_epoch = 0
        best_model = None
        while iters_since_last_sigimprove <= 4:
            h = self.run_epoch()
            _, test_acc = self.model.evaluate(self.test_images, self.test_labels, verbose=0)
            train_acc = h.history["accuracy"][0]
            valid_acc = h.history["val_accuracy"][0]
            train_errs.append(1-train_acc)
            valid_errs.append(1-valid_acc)
            test_errs.append(1-test_acc)
            iters_since_last_sigimprove += 1
            if valid_acc > best_val + self.tol:
                iters_since_last_sigimprove = 0
            if valid_acc > best_val:
                best_val = valid_acc
                best_epoch = self.epoch
                best_model = h.model
        fig = plt.figure()
        ax = fig.add_subplot(111)
        trl = plt.Line2D(range(1, len(train_errs)+1), train_errs, color='green', label="Training error")
        val = plt.Line2D(range(1, len(valid_errs)+1), valid_errs, color='yellow', label="Validation error")
        tel = plt.Line2D(range(1, len(test_errs)+1), test_errs, color='red', label="Testing error")
        ax.add_line(trl)
        ax.add_line(val)
        ax.add_line(tel)
        ax.set_xlim(1, self.epoch)
        ax.set_ylim(0, max(max(train_errs),max(valid_errs), max(test_errs)))
        plt.legend(handles=[trl,val,tel])
        plt.show()
        print(f"Best Train Accuracy: {1 - min(train_errs)}\nBest Valid Accuracy: {1 - min(valid_errs)}\nBest Test Accuracy: {1 - min(test_errs)}")
        print(f"Best epoch: {best_epoch}")
        self.best_model = best_model
