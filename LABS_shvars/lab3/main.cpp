#include <iostream>
#include <iomanip>
#include <vector>
using namespace std;

// Метод прогонки для системы
// (a[0] = 0, c[n-1] = 0)
vector<double> progonka(const vector<double>& a, const vector<double>& b,
                        const vector<double>& c, const vector<double>& d) {
    int n = b.size();
    vector<double> p(n), q(n), x(n);

    // прямой ход: x[i] = p[i]*x[i+1] + q[i]
    p[0] = -c[0] / b[0];
    q[0] =  d[0] / b[0];
    for (int i = 1; i < n; i++) {
        double den = a[i] * p[i - 1] + b[i];
        p[i] = -c[i] / den;
        q[i] = (d[i] - a[i] * q[i - 1]) / den;
    }

    // обратный ход
    x[n - 1] = q[n - 1];
    for (int i = n - 2; i >= 0; i--)
        x[i] = p[i] * x[i + 1] + q[i];
    return x;
}

int main() {
    // X = 0.1285
    vector<double> x = {0.115, 0.120, 0.125, 0.130, 0.135, 0.140};
    vector<double> y = {8.65729, 8.29329, 7.95829, 7.64893, 7.36235, 7.09613};
    double X = 0.1285;
    int n = x.size();

    vector<double> h(n - 1);
    for (int i = 0; i < n - 1; i++) h[i] = x[i + 1] - x[i];

    // Система для m_i, m_0 = m_{n-1} = 0
    vector<double> A(n, 0), B(n, 0), C(n, 0), D(n, 0);
    B[0] = 1;                       // m_0 = 0
    B[n - 1] = 1;                   // m_{n-1} = 0
    for (int i = 1; i < n - 1; i++) {
        double l = h[i] / (h[i] + h[i - 1]);
        A[i] = 1 - l;
        B[i] = 2;
        C[i] = l;
        D[i] = 6.0 / (h[i] + h[i - 1]) *
               ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1]);
    }
    vector<double> m = progonka(A, B, C, D);

    // Коэффициенты сплайна S_i(x) = a + b*t + c*t^2 + d*t^3, t = x - x_i
    vector<double> a(n - 1), b(n - 1), c(n - 1), d(n - 1);
    for (int i = 0; i < n - 1; i++) {
        a[i] = y[i];
        c[i] = m[i] / 2;
        d[i] = (m[i + 1] - m[i]) / (6 * h[i]);
        b[i] = (y[i + 1] - y[i]) / h[i] - h[i] * m[i] / 3 - h[i] * m[i + 1] / 6;
    }

    cout << fixed << setprecision(6);
    cout << "Коэффициенты сплайна:\n";
    cout << " i |    x_i   |    a_i    |    b_i     |    c_i     |     d_i\n";
    for (int i = 0; i < n - 1; i++)
        cout << setw(2) << i + 1 << " | " << setw(8) << x[i] << " | " << setw(9) << a[i]
             << " | " << setw(10) << b[i] << " | " << setw(10) << c[i]
             << " | " << setw(11) << d[i] << endl;

    // Поиск отрезка [x_i, x_{i+1}], содержащего X
    if (X < x[0] || X > x[n - 1]) {
        cout << "X вне таблицы (экстраполяция не выполняется)\n";
        return 1;
    }
    int k = 0;
    while (k < n - 2 && X > x[k + 1]) k++;

    double t = X - x[k];
    double S = a[k] + b[k] * t + c[k] * t * t + d[k] * t * t * t;

    cout << "\nX = " << X << " лежит на отрезке [" << x[k] << "; " << x[k + 1] << "]\n";
    cout << "S(X) = " << setprecision(6) << S << endl;
    return 0;
}
