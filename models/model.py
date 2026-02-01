import os
import shutil
import kagglehub
import numpy as np
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import DenseNet121
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.densenet import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

class Model:

    train_dir = None
    test_dir = None
    image_generator = None
    model = None
    history = None
    
    BATCH_SIZE = 32
    TARGET_SIZE = (224, 224)

    def __init__(self, path="paultimothymooney/chest-xray-pneumonia"):
        pass

    def load_data(self, path="paultimothymooney/chest-xray-pneumonia"):
        self.path = kagglehub.dataset_download(path)
        self.train_dir = os.path.join(self.path, 'train')
        self.test_dir = os.path.join(self.path, 'test')

    def preprocess_data(self):
        self.train_dir_path, self.val_dir_path, self.test_dir_path = [os.path.join(self.path, "chest_xray", d) for d in ["train", "val", "test"]]

        for cls in ["NORMAL", "PNEUMONIA"]:
            src, dst = os.path.join(self.train_dir_path, cls), os.path.join(self.val_dir_path, cls)
            os.makedirs(dst, exist_ok=True)
            
            if os.path.exists(src) and len(os.listdir(dst)) < 50:
                files = os.listdir(src)
                for img in np.random.choice(files, int(len(files) * 0.2), replace=False):
                    shutil.move(os.path.join(src, img), os.path.join(dst, img))
                print(f"Movido 10% de {cls} para validação.")
    
        self.class_weights = self.get_class_weights()
        self.process_images()
    
    def process_images(self):
        train_datagen = ImageDataGenerator(
            rotation_range=20,
            zoom_range=0.15,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=True,
            fill_mode="nearest",
            preprocessing_function=preprocess_input
        )

        test_datagen = ImageDataGenerator(
            preprocessing_function=preprocess_input
        )

        print("Carregando datasets...")
        self.train_ds = train_datagen.flow_from_directory(
            self.train_dir_path,
            target_size=self.TARGET_SIZE,
            batch_size=self.BATCH_SIZE,
            class_mode='binary',
            shuffle=True
        )

        self.val_ds = test_datagen.flow_from_directory(
            self.val_dir_path,
            target_size=self.TARGET_SIZE,
            batch_size=self.BATCH_SIZE,
            class_mode='binary',
            shuffle=False
        )

        self.test_ds = test_datagen.flow_from_directory(
            self.test_dir_path,
            target_size=self.TARGET_SIZE,
            batch_size=self.BATCH_SIZE,
            class_mode='binary',
            shuffle=False
        )
    
    def get_class_weights(self):
        try:
            count_normal = len(os.listdir(os.path.join(self.train_dir_path, 'NORMAL')))
            count_pneumonia = len(os.listdir(os.path.join(self.train_dir_path, 'PNEUMONIA')))
            total = count_normal + count_pneumonia
            weight_0 = (1 / count_normal) * (total / 2.0)
            weight_1 = (1 / count_pneumonia) * (total / 2.0)
            class_weights = {0: weight_0, 1: weight_1}
            print(f"\nClass Weights calculados: {class_weights}")
            return class_weights
        except Exception as e:
            print(f"Erro ao calcular pesos das classes: {e}. Usando pesos iguais.")
            class_weights = {0: 1.0, 1: 1.0}
        return class_weights
    
    def create_model(self):
        base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        base_model.trainable = False

        self.model =  Sequential([
            base_model,
            GlobalAveragePooling2D(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])
        self.model.summary()
    
    def compile_model(self):
        self.model.compile(
            optimizer=Adam(learning_rate=1e-4),
            loss='binary_crossentropy',
            metrics=['accuracy', 
                tf.keras.metrics.Precision(name='precision'), 
                tf.keras.metrics.Recall(name='recall'), 
                tf.keras.metrics.AUC(name='auc')]
        )
    
    def fit_model(self, epochs=10):
        callbacks = [
            ModelCheckpoint('./models/pneumonia_model.keras', monitor='val_auc', mode='max', save_best_only=True, verbose=1),
            EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1),
            ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=1)
        ]
        self.history = self.model.fit(
            self.train_ds,
            epochs=epochs,
            validation_data=self.val_ds,
            callbacks=callbacks,
            class_weight=self.class_weights,
            verbose=1
        )
    
    def plot_history(self):
        plt.subplot(1, 2, 1)
        plt.plot(self.history.history['loss'], label='Train Loss')
        plt.plot(self.history.history['val_loss'], label='Val Loss')
        plt.title('Curva de Perda (Loss)')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(self.history.history['auc'], label='Train AUC')
        plt.plot(self.history.history['val_auc'], label='Val AUC')
        plt.title('Curva ROC-AUC')
        plt.legend()
        plt.show()

        print("\n--- Avaliação no Dataset de Teste ---")
        eval_results = self.model.evaluate(self.test_ds)
        print(f"Test Loss: {eval_results[0]:.4f}")
        print(f"Test Accuracy: {eval_results[1]:.4f}")
        print(f"Test AUC: {eval_results[4]:.4f}")
        print("\nRelatório de Classificação Detalhado:")
        y_pred = (self.model.predict(self.test_ds) > 0.5).astype("int32")
        y_true = self.test_ds.classes
        print(classification_report(y_true, y_pred, target_names=['NORMAL', 'PNEUMONIA']))
    
    def load_model(self):
        self.model = tf.keras.models.load_model('best_model.h5')
    
    def evaluate_model(self):
        self.model.evaluate(self.test_ds)
    
    def predict(self, image):
        return self.model.predict(image)


if __name__ == '__main__':
    model = Model()
    model.load_data()
    model.preprocess_data()
    model.create_model()
    model.compile_model()
    model.fit_model(epochs=10)
    model.plot_history()