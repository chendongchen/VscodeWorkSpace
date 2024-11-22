import time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, GRU
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from tensorflow.keras import backend as K

# 路径
file_path = r'C:\Users\32429\Desktop\机器学习基础\上机实践\5_dynamic_system\dynamic_system'

# 读取数据
time_start = time.time()
input_data = pd.read_csv(file_path + '/input_x.csv')  # 输入数据
output_data = pd.read_csv(file_path + '/output_y.csv')  # 输出数据
time_end = time.time()
print('Data loading took', time_end - time_start, 'seconds')

# 数据预处理
x = input_data.values  # 输入力数据
y = output_data.values  # 输出位移数据

scalerX = MinMaxScaler(feature_range=(-2, 2))  # 输入缩放到 -2 到 2
XX = scalerX.fit_transform(x)

scalerY = MinMaxScaler(feature_range=(0, 1))  # 输出缩放到 0 到 1
YY = scalerY.fit_transform(y)

# 数据划分
sample = 100  # 样本总数
nn = 80  # 训练集样本数
mm = sample - nn  # 测试集样本数
deltlength = 1001  # 每段样本的序列长度
bs = 10  # 批处理大小

X = XX[:sample * deltlength]  # 输入
Y = YY[:sample * deltlength]  # 输出
n_train = deltlength * nn
n_test = deltlength * sample

# 划分训练集和测试集
trainX = X[:n_train]
trainY = Y[:n_train]
testX = X[n_train:n_test]
testY = Y[n_train:n_test]

# 转换为3D输入
train3DX = trainX.reshape((nn, deltlength, trainX.shape[1]))
test3DX = testX.reshape((mm, deltlength, testX.shape[1]))
train3DY = trainY.reshape((nn, deltlength, trainY.shape[1]))
test3DY = testY.reshape((mm, deltlength, testY.shape[1]))

# 定义GRU模型
model = Sequential()
model.add(GRU(units=20, input_shape=(train3DX.shape[1], train3DX.shape[2]), return_sequences=True))
model.add(GRU(units=20, return_sequences=True))
model.add(Dense(units=1, kernel_initializer='normal', activation='sigmoid'))
model.summary()

# 自定义损失函数
def myloss(y_true, y_pred):
    return K.mean(K.square(y_pred[:, :] - y_true[:, :]), axis=-1)

# 编译模型
model.compile(loss=myloss, optimizer='adam')

# 设置学习率和模型检查点
lr_new = 0.005
model.optimizer.learning_rate.assign(lr_new)  # 直接分配新学习率

# 修改文件扩展名为 .keras
filepath = file_path + '/model_n20n20_size1001_lr0.005_epoch100_best.keras'
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

# 训练模型
time_start = time.time()
history = model.fit(train3DX, train3DY, epochs=100, batch_size=bs, validation_data=(test3DX, test3DY),
                    verbose=2, shuffle=False, callbacks=callbacks_list)
time_end = time.time()
print('Training took', time_end - time_start, 'seconds')

# 绘制损失函数收敛曲线
t = range(100)
aa = history.history['loss']
bb = history.history['val_loss']

plt.figure(dpi=100, figsize=(8, 8))
plt.plot(t, aa, c='blue', label='Loss')
plt.plot(t, bb, c='red', label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('MSE')
plt.yscale('log')
plt.legend(loc='best')
plt.show()

# 加载模型并进行预测
model = load_model(filepath, custom_objects={'myloss': myloss})
forecasttest3DY0 = model.predict(test3DX)
forecasttest2DY0 = forecasttest3DY0.reshape((deltlength * mm, 1))

# 反归一化结果
YP = scalerY.inverse_transform(forecasttest2DY0)

# 绘制预测值和实际值对比图
index = 10  # 选取测试集的第10段
t = range(100100)

plt.figure(dpi=100, figsize=(8, 8))
plt.plot(t[(nn + index - 1) * deltlength:(nn + index) * deltlength],
         y[(nn + index - 1) * deltlength:(nn + index) * deltlength], c='blue', label='Actual')
plt.plot(t[(nn + index - 1) * deltlength:(nn + index) * deltlength],
         YP[(index - 1) * deltlength:index * deltlength], c='red', label='Predicted')
plt.xlabel('Time steps')
plt.ylabel('Displacement (m)')
plt.legend(loc='best')
plt.show()
