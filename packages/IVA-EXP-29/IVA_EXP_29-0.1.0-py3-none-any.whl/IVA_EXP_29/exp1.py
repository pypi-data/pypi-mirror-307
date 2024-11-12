# exp1.py

def run():
    print("""Code for Experiment 1 mnist data using tensorflow
import tensorflow as tf
import tensorflow_datasets as tfds

# Load and preprocess the MNIST dataset
mnist_data = tfds.load('mnist', split=['train', 'test'], as_supervised=True)
train_data, test_data = mnist_data

# Preprocess: Flatten, cast to float32, normalize images, and one-hot encode labels
batch_size = 100
train_data = train_data.map(lambda img, lbl: (tf.cast(tf.reshape(img, [-1]), tf.float32) / 255.0, tf.one_hot(lbl, depth=10)))
test_data = test_data.map(lambda img, lbl: (tf.cast(tf.reshape(img, [-1]), tf.float32) / 255.0, tf.one_hot(lbl, depth=10)))

train_data = train_data.shuffle(10000).batch(batch_size)
test_data = test_data.batch(batch_size)

# Model parameters
input_size = 784
no_classes = 10
learning_rate = 0.5
epochs = 10

# Initialize weights and biases
W = tf.Variable(tf.random.normal([input_size, no_classes]))
b = tf.Variable(tf.random.normal([no_classes]))

# Optimizer
optimizer = tf.optimizers.SGD(learning_rate)

# Training loop
for epoch in range(epochs):
    epoch_loss = 0
    for images, labels in train_data:
        with tf.GradientTape() as tape:
            # Compute logits (predictions before softmax)
            logits = tf.matmul(images, W) + b
            # Compute loss using softmax cross-entropy
            loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=labels, logits=logits))
        # Compute gradients and update weights
        gradients = tape.gradient(loss, [W, b])
        optimizer.apply_gradients(zip(gradients, [W, b]))
        
        # Accumulate loss for this epoch
        epoch_loss += loss
    print(f"Epoch {epoch+1}, Loss: {epoch_loss.numpy()}")

# Testing accuracy
accuracy_metric = tf.metrics.Accuracy()
for images, labels in test_data:
    logits = tf.matmul(images, W) + b
    predictions = tf.argmax(logits, axis=1)
    actuals = tf.argmax(labels, axis=1)
    accuracy_metric.update_state(actuals, predictions)

accuracy = accuracy_metric.result().numpy()
print("Accuracy:", accuracy)
""")
    
