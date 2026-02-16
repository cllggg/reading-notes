"""
nash_upgrade.py - Game Theory Strategy Analyzer & Upgrader
Author: Trae AI (Geek Persona)
Date: 2026-02-16

This script analyzes a 2x2 game matrix to detect:
1. Nash Equilibria
2. Pareto Optimality
3. Dilemmas (Prisoner's Dilemma, Chicken, Stag Hunt)

And proposes "Dimensionality Upgrades" to solve dilemmas.
"""

import numpy as np

class GameMatrix:
    def __init__(self, name, r, s, t, p):
        """
        Payoff Matrix for Player A (Symmetric Game):
        (R, R) - Reward for mutual cooperation
        (S, T) - Sucker's payoff, Temptation to defect
        (T, S) - Temptation, Sucker
        (P, P) - Punishment for mutual defection
        """
        self.name = name
        self.R = r  # Reward
        self.S = s  # Sucker
        self.T = t  # Temptation
        self.P = p  # Punishment

    def analyze(self):
        print(f"\n--- Analyzing Game: {self.name} ---")
        print(f"Payoffs: T={self.T}, R={self.R}, P={self.P}, S={self.S}")
        
        # Check for Prisoner's Dilemma: T > R > P > S
        if self.T > self.R > self.P > self.S:
            print("[!] Detected: Prisoner's Dilemma")
            print("    Nash Equilibrium: (Defect, Defect)")
            print("    Social Optimum: (Cooperate, Cooperate)")
            self.suggest_upgrade("repetition")
            
        # Check for Chicken Game: T > R > S > P
        elif self.T > self.R > self.S > self.P:
            print("[!] Detected: Chicken Game (Snowdrift)")
            print("    Nash Equilibria: (C, D) and (D, C)")
            self.suggest_upgrade("commitment")
            
        # Check for Stag Hunt: R > T > P > S
        elif self.R > self.T > self.P > self.S:
            print("[!] Detected: Stag Hunt (Assurance Game)")
            print("    Nash Equilibria: (C, C) [Payoff Dominant] and (D, D) [Risk Dominant]")
            self.suggest_upgrade("signaling")
            
        else:
            print("[*] No standard dilemma detected.")

    def suggest_upgrade(self, strategy_type):
        print("\n>>> Dimensionality Upgrade Proposal <<<")
        
        if strategy_type == "repetition":
            # Solve PD with infinite repetition
            # Condition: delta >= (T-R)/(T-P)
            delta_min = (self.T - self.R) / (self.T - self.P)
            print(f"1. [Ascension] Introduce 'Shadow of the Future'")
            print(f"   Required Discount Factor (delta) >= {delta_min:.2f}")
            print(f"   Action: Sign long-term contracts; Use 'Tit-for-Tat'.")
            
        elif strategy_type == "commitment":
            print(f"1. [Ascension] Introduce 'Credible Threat'")
            print(f"   Action: Publicly burn bridges; Remove steering wheel.")
            print(f"   Goal: Force opponent to Swerve.")
            
        elif strategy_type == "signaling":
            print(f"1. [Ascension] Introduce 'Costly Signaling'")
            print(f"   Action: Invest in brand/reputation upfront.")
            print(f"   Goal: Coordinate on (Stag, Stag).")

if __name__ == "__main__":
    # 1. Prisoner's Dilemma (T=5, R=3, P=1, S=0)
    pd = GameMatrix("Prisoner's Dilemma", r=3, s=0, t=5, p=1)
    pd.analyze()

    # 2. Chicken Game (T=5, R=3, S=1, P=0)
    chicken = GameMatrix("Chicken Game", r=3, s=1, t=5, p=0)
    chicken.analyze()

    # 3. Stag Hunt (R=5, T=4, P=2, S=0)
    stag = GameMatrix("Stag Hunt", r=5, s=0, t=4, p=2)
    stag.analyze()
