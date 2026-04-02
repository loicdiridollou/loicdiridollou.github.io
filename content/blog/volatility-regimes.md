---
title: "Detecting Volatility Regimes with Hidden Markov Models"
date: 2026-03-15
---

One of the most persistent challenges in quantitative finance is that markets don't behave consistently over time. A strategy that performs well during a calm trending period can blow up during a crisis. The underlying issue is that markets switch between distinct *regimes* — periods of low volatility interspersed with bursts of high volatility — and most models ignore this structure entirely.

Hidden Markov Models (HMMs) offer a principled way to handle this. The core idea is simple: assume there is a small number of hidden states (e.g., "calm" and "turbulent"), and that the observed returns are drawn from different distributions depending on the current state. The states transition between each other with some probability, and we never directly observe which state we're in — we infer it from the data.

## A Two-State Model

For a two-state HMM on daily log-returns, the setup looks like this:

- **State 0 (low vol):** returns ~ N(μ₀, σ₀²), with σ₀ small
- **State 1 (high vol):** returns ~ N(μ₁, σ₁²), with σ₁ large
- Transition matrix P where P[i,j] is the probability of moving from state i to state j

After fitting the model via the Baum-Welch algorithm (EM for HMMs), you get both the learned parameters and a smoothed state probability for each day.

```python
from hmmlearn.hmm import GaussianHMM
import numpy as np

model = GaussianHMM(n_components=2, covariance_type="full", n_iter=1000)
returns = np.diff(np.log(prices)).reshape(-1, 1)
model.fit(returns)

hidden_states = model.predict(returns)
```

## What You Actually Get

The output is a sequence of 0s and 1s labeling each day. On SPX data going back to 2000, the high-volatility state reliably captures the 2008 crisis, the 2011 European debt scare, the 2020 COVID crash, and little else of note. The low-volatility state covers most of the 2013–2019 bull market.

More useful than the hard labels is the smoothed probability — the probability of being in each state given *all* observations. This gives you a continuous signal you can use to scale position sizes or adjust hedge ratios dynamically.

## Practical Caveats

A few things that bite you in practice:

**Label switching.** HMMs don't inherently know which state is "high vol." You need to label states post-hoc based on the fitted variance parameters.

**Reestimation lag.** If you refit the model in a walk-forward fashion, regime detection lags behind reality. The model needs several days of high-vol observations before it shifts its state estimate. This makes it more useful for medium-frequency positioning than for intraday risk management.

**Number of states.** Two states is a useful first approximation, but real markets have more structure. A three-state model adding a "trending low-vol" state distinct from a "mean-reverting low-vol" state often fits better — though overfitting becomes a real concern past four or five states.

Despite these limitations, regime-aware position sizing is one of the more robust improvements you can make to a simple momentum or mean-reversion strategy. The improvement doesn't come from predicting regimes in advance — it comes from sizing down during the periods the model already identifies as turbulent.
