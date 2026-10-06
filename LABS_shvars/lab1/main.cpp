#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

const int n = 3;
const double eps = 0.0001;

// Вывод расширенной матрицы
void printMatrix(double a[n][n+1]) {
    for (int i = 0; i < n; i++) {
        cout << "| ";
        for (int j = 0; j <= n; j++) {
            cout << setw(9) << setprecision(4) << fixed << a[i][j] << " ";
        }
        cout << "|" << endl;
    }
    cout << endl;
}

// Метод Гаусса с выбором главного элемента
void gauss(double a[n][n+1], double x[n]) {
    cout << "==================================================" << endl;
    cout << "МЕТОД ГАУССА С ВЫБОРОМ ГЛАВНОГО ЭЛЕМЕНТА" << endl;
    cout << "==================================================" << endl << endl;

    cout << "Исходная расширенная матрица:" << endl;
    printMatrix(a);

    for (int k = 0; k < n; k++) {
        cout << "--- Шаг " << k+1 << " ---" << endl;

        // Поиск главного элемента в столбце k
        int maxRow = k;
        double maxVal = fabs(a[k][k]);
        for (int i = k+1; i < n; i++) {
            if (fabs(a[i][k]) > maxVal) {
                maxVal = fabs(a[i][k]);
                maxRow = i;
            }
        }

        cout << "Главный элемент в столбце " << k+1 << ": ";
        cout << "a[" << maxRow+1 << "][" << k+1 << "] = " << a[maxRow][k] << endl;

        // Перестановка строк
        if (maxRow != k) {
            for (int j = 0; j <= n; j++) {
                swap(a[k][j], a[maxRow][j]);
            }
            cout << "Перестановка строк " << k+1 << " и " << maxRow+1 << ":" << endl;
            printMatrix(a);
        } else {
            cout << "Перестановка не требуется." << endl;
        }

        // Обнуление элементов ниже диагонали
        for (int i = k+1; i < n; i++) {
            double factor = a[i][k] / a[k][k];
            cout << "Множитель для строки " << i+1 << ": m = " << factor << endl;
            for (int j = k; j <= n; j++) {
                a[i][j] -= factor * a[k][j];
            }
        }

        cout << "После обнуления столбца " << k+1 << ":" << endl;
        printMatrix(a);
    }

    // Обратный ход
    cout << "--- Обратный ход ---" << endl;
    for (int i = n-1; i >= 0; i--) {
        x[i] = a[i][n];
        for (int j = i+1; j < n; j++) {
            x[i] -= a[i][j] * x[j];
        }
        x[i] /= a[i][i];
        cout << "x" << i+1 << " = " << x[i] << endl;
    }

    cout << endl << "Решение методом Гаусса:" << endl;
    for (int i = 0; i < n; i++) {
        cout << "x" << i+1 << " = " << x[i] << endl;
    }
    cout << endl;
}

// Метод Зейделя
void seidel(double a[n][n+1], double x[n], double eps) {
    cout << "==================================================" << endl;
    cout << "МЕТОД ЗЕЙДЕЛЯ" << endl;
    cout << "==================================================" << endl << endl;

    double C[n][n], d[n];

    // Приведение к виду x = Cx + d
    cout << "Приведение к виду x = Cx + d:" << endl;
    for (int i = 0; i < n; i++) {
        d[i] = a[i][n] / a[i][i];
        cout << "d" << i+1 << " = " << a[i][n] << " / " << a[i][i] << " = " << d[i] << endl;
        for (int j = 0; j < n; j++) {
            if (i != j) {
                C[i][j] = -a[i][j] / a[i][i];
            } else {
                C[i][j] = 0;
            }
        }
    }
    cout << endl;

    cout << "Матрица C:" << endl;
    for (int i = 0; i < n; i++) {
        cout << "| ";
        for (int j = 0; j < n; j++) {
            cout << setw(9) << setprecision(4) << fixed << C[i][j] << " ";
        }
        cout << "|" << endl;
    }
    cout << endl;

    cout << "Вектор d:" << endl;
    for (int i = 0; i < n; i++) {
        cout << "d" << i+1 << " = " << d[i] << endl;
    }
    cout << endl;

    // Проверка нормы
    double norm = 0;
    for (int i = 0; i < n; i++) {
        double sum = 0;
        for (int j = 0; j < n; j++) {
            sum += fabs(C[i][j]);
        }
        cout << "Сумма модулей в строке " << i+1 << ": " << sum << endl;
        if (sum > norm) norm = sum;
    }
    cout << "Норма ||C||_inf = " << norm << endl;
    if (norm >= 1) {
        cout << "ВНИМАНИЕ: условие сходимости не выполнено!" << endl;
    } else {
        cout << "Условие сходимости выполнено." << endl;
    }
    cout << endl;

    // Начальное приближение
    for (int i = 0; i < n; i++) x[i] = 0;
    cout << "Начальное приближение: x = (0, 0, 0)" << endl << endl;

    cout << "Итерации:" << endl;
    cout << setw(5) << "k" << setw(12) << "x1" << setw(12) << "x2" << setw(12) << "x3" << setw(15) << "погрешность" << endl;
    cout << string(56, '-') << endl;

    int iter = 0;
    double error;
    do {
        double x_old[n];
        for (int i = 0; i < n; i++) x_old[i] = x[i];

        for (int i = 0; i < n; i++) {
            double sum = d[i];
            for (int j = 0; j < n; j++) {
                if (j < i) sum += C[i][j] * x[j];      // новые значения
                else if (j > i) sum += C[i][j] * x_old[j]; // старые значения
            }
            x[i] = sum;
        }

        iter++;
        error = 0;
        for (int i = 0; i < n; i++) {
            error += fabs(x[i] - x_old[i]);
        }

        cout << setw(5) << iter;
        for (int i = 0; i < n; i++) {
            cout << setw(12) << setprecision(6) << fixed << x[i];
        }
        cout << setw(15) << setprecision(6) << error << endl;
    } while (error > eps);

    cout << endl << "Решение методом Зейделя:" << endl;
    for (int i = 0; i < n; i++) {
        cout << "x" << i+1 << " = " << x[i] << endl;
    }
    cout << endl;
}

int main() {
    // Исходная система (вариант 26)
    double a[n][n+1] = {
        {0.9, 2.7, -3.8, 2.4},
        {2.5, 5.8, -0.5, 3.5},
        {4.5, -2.1, 3.2, -1.2}
    };

    double x[n];

    // Метод Гаусса
    double a_gauss[n][n+1];
    for (int i = 0; i < n; i++)
        for (int j = 0; j <= n; j++)
            a_gauss[i][j] = a[i][j];
    gauss(a_gauss, x);

    // Метод Зейделя (с преобразованием для сходимости)
    // Преобразованная система:
    // 7.0x1 + 3.7x2 + 2.7x3 = 2.3
    // 3.4x1 + 8.5x2 - 4.3x3 = 5.9
    // 0.9x1 + 2.7x2 - 3.8x3 = 2.4
    double a_seidel[n][n+1] = {
        {7.0, 3.7, 2.7, 2.3},
        {3.4, 8.5, -4.3, 5.9},
        {0.9, 2.7, -3.8, 2.4}
    };
    seidel(a_seidel, x, eps);

    return 0;
}
