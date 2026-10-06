#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

const int n = 3;
const int m = n + 1;
const double EPS = 0.0001;

// Пересчёт индексов (i, j) в одномерный массив
int idx(int i, int j) {
    return i * m + j;
}

void printMatrix(const double a[]) {
    for (int i = 0; i < n; i++) {
        cout << "| ";
        for (int j = 0; j < m; j++)
            cout << setw(10) << setprecision(4) << fixed << a[idx(i, j)] << " ";
        cout << "|" << endl;
    }
    cout << endl;
}

// Метод Гаусса с выбором главного элемента и нормированием
// Метод Гаусса с выбором главного элемента и нормированием
void gaussJordan(double a[], double x[]) {
    cout << "=== МЕТОД ГАУССА С ВЫБОРОМ ГЛАВНОГО ЭЛЕМЕНТА И НОРМИРОВАНИЕМ ===\n\n";
    cout << "Исходная расширенная матрица:\n";
    printMatrix(a);

    for (int k = 0; k < n; k++) {
        cout << "--- Шаг " << k + 1 << " ---\n";

        // Поиск главного элемента
        cout << "Ищем главный элемент в столбце " << k + 1 << ".\n";
        int maxRow = k;
        for (int i = k + 1; i < n; i++)
            if (fabs(a[idx(i, k)]) > fabs(a[idx(maxRow, k)]))
                maxRow = i;

        cout << "Максимальный по модулю: a[" << maxRow + 1 << "][" << k + 1
             << "] = " << a[idx(maxRow, k)] << "\n";

        // Перестановка
        if (maxRow != k) {
            cout << "Переставляем строки " << k + 1 << " и " << maxRow + 1 << ":\n";
            for (int j = 0; j < m; j++)
                swap(a[idx(k, j)], a[idx(maxRow, j)]);
            printMatrix(a);
        } else {
            cout << "Перестановка не требуется.\n\n";
        }

        // Нормирование
        double pivot = a[idx(k, k)];
        cout << "Нормируем строку " << k + 1
             << ": делим все элементы на " << pivot
             << " (a[" << k + 1 << "][" << k + 1 << "])\n";
        for (int j = 0; j < m; j++)
            a[idx(k, j)] /= pivot;
        printMatrix(a);

        // Обнуление
        cout << "Обнуляем столбец " << k + 1 << " в остальных строках.\n";
        for (int i = 0; i < n; i++) {
            if (i == k) continue;
            double factor = a[idx(i, k)];
            cout << "Для строки " << i + 1 << ": множитель = " << factor
                 << ", вычитаем " << factor << " * строку " << k + 1 << "\n";
            for (int j = 0; j < m; j++)
                a[idx(i, j)] -= factor * a[idx(k, j)];
        }
        printMatrix(a);
    }

    for (int i = 0; i < n; i++)
        x[i] = a[idx(i, n)];
}

// Метод Зейделя
void seidel(const double a[], double x[], double eps) {
    cout << "=== МЕТОД ЗЕЙДЕЛЯ ===\n\n";
    cout << "Система, приведённая к виду с диагональным преобладанием:\n";
    printMatrix(a);

    // --- Проверка условия сходимости ---
    cout << "Проверка условия сходимости ||C||_inf < 1:\n";
    double norm = 0;
    for (int i = 0; i < n; i++) {
        double sum = 0;
        cout << "  Строка " << i + 1 << ": ";
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            double c = fabs(a[idx(i, j)] / a[idx(i, i)]);
            sum += c;
            cout << "|a" << i + 1 << j + 1 << "/a" << i + 1 << i + 1 << "|";
            if (j < n - 1) cout << " + ";
        }
        cout << " = " << sum << "\n";
        if (sum > norm) norm = sum;
    }
    cout << "Норма ||C||_inf = " << norm;
    if (norm < 1)
        cout << " < 1 — условие сходимости выполнено.\n\n";
    else
        cout << " >= 1 — условие сходимости НЕ выполнено!\n\n";

    // --- Приведение к виду x = Cx + d ---
    cout << "Приведение к виду x = Cx + d:\n";
    for (int i = 0; i < n; i++) {
        cout << "  x" << i + 1 << " = ";
        bool first = true;
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            double c = -a[idx(i, j)] / a[idx(i, i)];
            if (!first) cout << (c >= 0 ? " + " : " - ");
            else if (c < 0) cout << "-";
            cout << fabs(c) << "*x" << j + 1;
            first = false;
        }
        double d = a[idx(i, n)] / a[idx(i, i)];
        cout << (d >= 0 ? " + " : " - ") << fabs(d) << "\n";
    }
    cout << "\n";

    // --- Начальное приближение ---
    for (int i = 0; i < n; i++) x[i] = 0;
    cout << "Начальное приближение: x = (0, 0, 0)\n\n";

    cout << "Итерации:\n";
    cout << setw(4)  << "k"
         << setw(14) << "x1"
         << setw(14) << "x2"
         << setw(14) << "x3"
         << setw(16) << " погрешность" << endl;
    cout << string(62, '-') << endl;

    int iter = 0;
    double error;
    do {
        double x_old[n];
        for (int i = 0; i < n; i++) x_old[i] = x[i];

        cout << "\nИтерация " << iter + 1 << ":\n";

        for (int i = 0; i < n; i++) {
            double sum = a[idx(i, n)] / a[idx(i, i)];
            cout << "  x" << i + 1 << " = " << a[idx(i, n)] << "/"
                 << a[idx(i, i)];

            for (int j = 0; j < n; j++) {
                if (i == j) continue;
                double c = -a[idx(i, j)] / a[idx(i, i)];
                double val = (j < i) ? x[j] : x_old[j]; // новые или старые
                cout << (c >= 0 ? " + " : " - ")
                     << fabs(c) << "*" << val;
                sum += c * val;
            }
            x[i] = sum;
            cout << " = " << x[i] << "\n";
        }

        iter++;
        error = 0;
        for (int i = 0; i < n; i++) error += fabs(x[i] - x_old[i]);

        cout << "  Погрешность: ";
        for (int i = 0; i < n; i++) {
            cout << "|x" << i + 1 << " - x" << i + 1 << "_old|";
            if (i < n - 1) cout << " + ";
        }
        cout << " = " << error << "\n";

        cout << setw(4)  << iter;
        for (int i = 0; i < n; i++)
            cout << setw(14) << setprecision(6) << fixed << x[i];
        cout << setw(16) << setprecision(6) << fixed << error << endl;

        if (error <= eps) {
            cout << "\nПогрешность " << error << " <= " << eps
                 << " — итерации завершены.\n";
            break;
        }
    } while (true);
}
int main() {
    double a[n * m];
    cout << "Введите матрицу " << n << "x" << m << ":" << endl;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            cin >> a[idx(i, j)];

    double a1[n * m], a2[n * m];
    for (int i = 0; i < n * m; i++) a1[i] = a2[i] = a[i];

    double x1[n], x2[n];
    gaussJordan(a1, x1);

    cout << "Решение (Гаусс): ";
    for (int i = 0; i < n; i++) cout << x1[i] << " ";
    cout << endl;

    // Преобразование системы для сходимости Зейделя
    for (int j = 0; j < m; j++) {
        a2[idx(0, j)] = a[idx(1, j)] + a[idx(2, j)];
        a2[idx(1, j)] = a[idx(0, j)] + a[idx(1, j)];
        a2[idx(2, j)] = a[idx(0, j)];
    }

    seidel(a2, x2, EPS);

    cout << "Решение (Зейдель): ";
    for (int i = 0; i < n; i++) cout << x2[i] << " ";
    cout << endl;

    return 0;
}
