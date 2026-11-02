#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

const double EPS = 1e-6;

double f(double x) {
    return x * x * x - 0.1 * x * x + 0.4 * x + 2;
}

double df(double x) {
    return 3 * x * x - 0.2 * x + 0.4;
}

double ddf(double x) {
    return 6 * x - 0.2;
}

//1. Метод половинного деления
void bisection(double a, double b, double& x, int& n) {
    n = 0;
    while (fabs(b - a) > EPS) {
        x = (a + b) / 2.0;
        if (f(a) * f(x) <= 0) b = x;
        else a = x;
        n++;
    }
    x = (a + b) / 2.0;
}

//2. Метод хорд
void chord(double a, double b, double& x, int& n) {
    n = 0;
    double x_curr;
    double fixed_end;

    //неподвижный конец f * f'' > 0
    if (f(a) * ddf(a) > 0) {
        fixed_end = a;
        x_curr = b;
    } else {
        fixed_end = b;
        x_curr = a;
    }

    while (true) {
        double x_next = x_curr - f(x_curr) / (f(x_curr) - f(fixed_end)) * (x_curr - fixed_end);
        n++;
        if (fabs(x_next - x_curr) < EPS) {
            x = x_next;
            break;
        }
        x_curr = x_next;
    }
}

// 3. Метод Ньютона (универсальный)
void newton(double a, double b, double& x, int& n) {
    n = 0;
    double x_curr;
    
    // Выбираем начальное приближение: f(x0) * f''(x0) > 0
    if (f(a) * ddf(a) > 0) x_curr = a;
    else x_curr = b;

    while (true) {
        double x_next = x_curr - f(x_curr) / df(x_curr);
        n++;
        if (fabs(x_next - x_curr) < EPS) {
            x = x_next;
            break;
        }
        x_curr = x_next;
    }
}

//4. Комбинированный метод 
void combined(double a, double b, double& x, int& n) {
    n = 0;
    double x_n, x_bar;
    
    if (f(a) * ddf(a) > 0) {
        x_n = a;     // Касательная от неподвижного
        x_bar = b;   // Хорда от подвижного
    } else {
        x_n = b;
        x_bar = a;
    }
    
    while (true) {
        // Шаг касательной
        double x_n_next = x_n - f(x_n) / df(x_n);
        // Шаг хорды
        double x_bar_next = x_bar - f(x_bar) / (f(x_bar) - f(x_n)) * (x_bar - x_n);
        
        n++;
        if (fabs(x_n_next - x_bar_next) < EPS) {
            x = (x_n_next + x_bar_next) / 2.0;
            break;
        }
        x_n = x_n_next;
        x_bar = x_bar_next;
    }
}

//5. Метод итераций
void iteration(double a, double b, double& x, int& n) {
    n = 0;
    
    // Ищем максимум модуля первой производной на отрезке (Q)
    double Q = 0;
    for (double t = a; t <= b; t += 0.01) {
        if (fabs(df(t)) > Q) Q = fabs(df(t));
    }
    
    // Выбираем k > Q/2, чтобы гарантировать сходимость
    double k = Q / 2.0 + 1.0; 
    // Знак k должен совпадать со знаком f'(x) (у нас f' > 0, значит k > 0)
    
    // Начальное приближение - любой конец отрезка
    double x_curr = a; 
    
    while (true) {
        // phi(x) = x - f(x)/k
        double x_next = x_curr - f(x_curr) / k;
        n++;
        if (fabs(x_next - x_curr) < EPS) {
            x = x_next;
            break;
        }
        x_curr = x_next;
    }
}

int main() {
    double a = -2.0, b = -1.0;
    double root;
    int steps;

    cout << "--------------------------------------------------------------------------------" << endl;
    cout << "               Метод       |   a, b, x0   |  Значение корня  | Шаги" << endl;
    cout << "--------------------------------------------------------------------------------" << endl;

    // 1. Половинного деления
    bisection(a, b, root, steps);
    cout << "1. Половинного деления      |   [-2, -1]   |    " 
         << setw(10) << left << setprecision(7) << fixed << root 
         << "    |  " << steps << endl;

    // 2. Хорд
    chord(a, b, root, steps);
    cout << "2. Хорд                     |   [-2, -1]   |    " 
         << setw(10) << left << setprecision(7) << fixed << root 
         << "    |  " << steps << endl;

    // 3. Касательных
    newton(a, b, root, steps);
    cout << "3. Касательных              |   [-2, -1]   |    " 
         << setw(10) << left << setprecision(7) << fixed << root 
         << "    |  " << steps << endl;

    // 4. Комбинированный
    combined(a, b, root, steps);
    cout << "4. Комбинированный          |   [-2, -1]   |    " 
         << setw(10) << left << setprecision(7) << fixed << root 
         << "    |  " << steps << endl;

    // 5. Итераций
    iteration(a, b, root, steps);
    cout << "5. Итераций                 |   [-2, -1]   |    " 
         << setw(10) << left << setprecision(7) << fixed << root 
         << "    |  " << steps << endl;

    cout << "--------------------------------------------------------------------------------" << endl;
    return 0;
}
