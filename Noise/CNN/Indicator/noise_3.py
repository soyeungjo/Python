
import tensorflow as tf
import numpy as np
import pandas as pd
import keras
a
noise_3.shape

x = np.array(noise_3.iloc[:, 2:])
x.shape[1] / 13

y = noise_3.iloc[:, 1]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, shuffle = True, random_state = 123)
x_train.shape, y_train.shape


#%% tensor
train_tensor = tf.reshape(x_train, shape = [x_train.shape[0], 3, 3, 13])
train_tensor.shape

test_tensor = tf.reshape(x_test, shape = [x_test.shape[0], 3, 3, 13])
test_tensor.shape

#%% CNN using Conv2D
model = models.Sequential()
model.add(layers.Conv2D(64, (1, 1), activation = 'relu', padding = 'same', input_shape = (3, 3, 13)))
model.add(layers.Dropout(0.3))
model.add(layers.Conv2D(32, (1, 1), activation = 'relu', padding = "same", ))
# model.add(layers.Dropout(0.3))
model.add(layers.Conv2D(16, (2, 2), activation = 'relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation = "relu"))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(32, activation = "relu"))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(1))

model_3.summary()

adam = Adam(lr = 0.00001)
model.compile(optimizer = adam, loss = 'mae', metrics = ['mse'])
model.fit(train_tensor, y_train, epochs = 1000, batch_size = 10, validation_data = (test_tensor, y_test))

# model_3.save(r"C:")
# model_3 = tf.keras.models.load_model(r"C:")

y_hat_train = model_3.predict(train_tensor).flatten()
# y_train.values.flatten()

plt.scatter(y_hat_train, y_train, alpha = 0.1)
plt.xlabel(r'$\hat{y}$')
plt.ylabel('$y$')

# np.min(y_hat_train)
# np.min(y_train)

# idx = np.argsort(y_hat_train)
# plt.scatter(np.array(y_train)[idx], y_hat_train[idx])

#%% test data
pred_y = model_3.predict(test_tensor)
plt.scatter(y_test, pred_y, alpha = 0.1)
# np.mean((pred_y - y_test)**2)


#%%
train_noise = pd.DataFrame({'ID' : noise_3.iloc[:, 0][y_train.index], 'pred_noise' : y_hat_train})
train_noise.shape
test_noise = pd.DataFrame({'ID' : noise_3.iloc[:, 0][y_test.index], 'pred_noise' : pred_y})
test_noise.shape

train_data = noise_3.iloc[y_train.index]
train_merge = pd.merge(train_data, train_noise, on = 'ID')
train_merge.shape
train_merge.to_csv(r'C:\Users\SOYOUNG\Desktop\3by3_train.csv', header = True, index = False, encoding = 'utf-8')

test_merge = pd.merge(noise_3.iloc[y_test.index], test_noise, on = 'ID')
test_merge.shape
test_merge.to_csv(r'C:\Users\SOYOUNG\Desktop\3by3_test.csv', header = True, index = False, encoding = 'utf-8')


noise_pred = pd.concat([train_noise, test_noise])
noise_pred.shape

noise_3by3 = pd.merge(noise_3, noise_pred, on = 'ID')
noise_3by3.shape

noise_3by3.to_csv(r'C:\Users\SOYOUNG\Desktop\noise_3by3.csv', header = True, index = False, encoding = 'utf-8')



#%% Conv2D
# model_input = layers.Input(shape = (3, 3, 13))
# conv1 = layers.Conv2D(10, (3, 3), activation = 'relu', padding = 'same')
# h = conv1(model_input)
# h = layers.Dropout(0.5)(h)
# conv2 = layers.Conv2D(5, (2, 2), activation = 'relu', padding = 'valid')
# h = conv2(h)
# h = layers.Dropout(0.5)(h)
# conv3 = layers.Conv2D(1, (2, 2), activation = 'relu', padding = 'valid')
# h = conv3(h)
# output_layer = layers.Dense(1)
# # h = tf.squeeze(h, axis=[1,2])
# output = output_layer(h)

# model_test = keras.models.Model(model_input, output)

# model_test.summary()

# #%%
# adam = Adam(lr = 0.000005)
# model_test.compile(optimizer = adam, loss = 'mae', metrics = ['mse'])
# model_test.fit(train_tensor, y_train, epochs = 300, batch_size = 10, validation_data = (test_tensor, y_test))

# pseudo_pred_y = model_test.predict(train_tensor).flatten()

# plt.scatter(y_train, pseudo_pred_y)


