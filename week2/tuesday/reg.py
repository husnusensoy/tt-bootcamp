from typing import Tuple

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from sklearn.datasets import make_regression


def make_reg_data() -> Tuple[np.array, np.array]:
    n = st.slider("Number of Sample", 10, 10_000, value=100)

    if st.checkbox("Outlier"):
        x, y = make_regression(
            n,
            1,
            random_state=42,
            noise=st.slider("Noise", 1, 100, value=10, help="Jitter around point"),
        )

        x = np.concatenate((x, np.array([[-1], [0], [2], [-2], [0], [2]])))
        y = np.concatenate((y, np.array([300, 300, 300, 300, 300, 300])))
    else:
        x, y = make_regression(
            n,
            1,
            random_state=42,
            noise=st.slider("Noise", 1, 100, value=10, help="Jitter around point"),
        )

    return x, y


def ls(x, y, alpha=0.01) -> np.array:
    w = np.random.random(2)

    print("Starting gradient descent")
    for _ in range(10):
        y_pred = w[0] + w[1] * x

        g_w0 = -2 * (y - y_pred).sum()
        g_w1 = -2 * (x * (y - y_pred)).sum()

        print(f"gradient w_0 = {g_w0} w_1 {g_w1}")

        w[0] -= alpha * g_w0
        w[1] -= alpha * g_w1

    return w


def ls_l1(x, y, alpha=0.01, lamb: float = 1.0) -> np.array:
    w = np.random.random(2)

    print("Starting gradient descent")
    for _ in range(40):
        y_pred = w[0] + w[1] * x

        if w[0] > 0:
            g_w0 = -2 * (y - y_pred).sum() + lamb
        else:
            g_w0 = -2 * (y - y_pred).sum() - lamb

        if w[1] > 0:
            g_w1 = -2 * (x * (y - y_pred)).sum() + lamb
        else:
            g_w1 = -2 * (x * (y - y_pred)).sum() - lamb

        print(f"gradient w_0 = {g_w0} w_1 {g_w1}")

        w[0] -= alpha * g_w0
        w[1] -= alpha * g_w1

    return w


def main():
    section = st.sidebar.radio(
        "Section", ["Data", "Regression Models", "Convexity", "Polynomial Features"]
    )

    if section == "Regression Models":
        x, y = make_reg_data()

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=x[:, 0], y=y, mode="markers", name="Data Points"))

        m1, m2, m3, m4 = "Model 1 (LSR)", "Model 2 (L1 Reg)", "Model 3", "Model 4"

        model_selected = st.radio("Model Type", [m1, m2, m3, m4])

        if model_selected == m1:
            w = ls(x[:, 0], y, alpha=0.001)
        elif model_selected == m2:
            w = ls_l1(x[:, 0], y, alpha=0.001, lamb=1.0)

        y_pred = w[1] * x[:, 0] + w[0]

        # print(y_pred)

        fig.add_trace(
            go.Scatter(x=x[:, 0], y=y_pred, mode="lines", name="Model Prediction")
        )

        st.plotly_chart(fig, use_container_width=True)

    elif section == "Data":
        x, y = make_reg_data(100)

        st.dataframe(y)
    elif section == "Polynomial Features":
        ...
    else:
        ...


if __name__ == "__main__":
    main()
