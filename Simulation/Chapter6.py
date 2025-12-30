import numpy as np
import matplotlib.pyplot as plt

# 结果
# n = 10, Y_interpolated = -0.21059503776268712, Y_regular = 0.0415973377703827, error = 0.25219237553306983
# n = 20, Y_interpolated = 7.774896937027671, Y_regular = 0.0415973377703827, error = 7.733299599257288
# Runge function
def runge_function(x):
    return 1 / (1 +  x ** 2)
# 定义插值函数

def lagrange_interpolation(x_values, y_values,x):
    n = len(x_values)
    result = 0.0
    for i in range(n):
        term = y_values[i]
        for j in range(n):
            if j != i:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        result += term
    return result

# Generate x values
n = np.array([10,20], dtype=int)
X_test = 4.8

for i in range(len(n)):
    x_values = np.linspace(-5, 5, n[i])
    # Generate y values using the Runge function
    y_values = runge_function(x_values)
    # Perform Lagrange interpolation
    Y_interpolated = lagrange_interpolation(x_values, y_values, X_test)
    Y_regular = runge_function(X_test)
    # Calculate the error
    error = np.abs(Y_interpolated - Y_regular)
    print(f"n = {n[i]}, Y_interpolated = {Y_interpolated}, Y_regular = {Y_regular}, error = {error}")

# 绘制图像
x_original = np.linspace(-5, 5, 500)
y_original = runge_function(x_original)

plt.figure(figsize=(10, 6))
plt.plot(x_original, y_original, label="Original Function", color="blue")

for i in range(len(n)):
    x_values = np.linspace(-5, 5, n[i])
    y_values = runge_function(x_values)
    y_interpolated = [lagrange_interpolation(x_values, y_values, x) for x in x_original]
    plt.plot(x_original, y_interpolated, label=f"Interpolated (n={n[i]})", linestyle="--")

plt.title("Function and Interpolations")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid()
# 调整保存图像的位置
plt.savefig("interpolation_plot.png")
plt.show()
print("图像已保存为 interpolation_plot.png")

