import random

# Stock 1 has a return uniformly distributed between -1% and 1%
stock1_return = lambda: random.uniform(0.99, 1.01)

# Stock 2 has a return uniformly distributed between -2% and 8%
stock2_return = lambda: random.uniform(0.98, 1.08)

portfolio_value = 100

for _ in range(100):
    # Randomly choose between stock 1 and stock 2
    if random.random() < 0.5:
        s_return = stock1_return()
        portfolio_value *= s_return
        print(f"Day {_ + 1}: Invested in Stock 1, Returned {s_return:.4f} Portfolio Value = {portfolio_value:.2f}")
    else:
        s_return = stock2_return()
        portfolio_value *= s_return
        print(f"Day {_ + 1}: Invested in Stock 2, Returned {s_return:.4f} Portfolio Value = {portfolio_value:.2f}")