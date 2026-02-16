// evolution_sim.rs
// A Rust simulation of Axelrod's Iterated Prisoner's Dilemma Tournament
// Compile: rustc evolution_sim.rs
// Run: ./evolution_sim

use std::collections::HashMap;

#[derive(Clone, Copy, Debug, PartialEq)]
enum Move {
    Cooperate,
    Defect,
}

trait Strategy {
    fn name(&self) -> String;
    // Given the history of the opponent's moves, decide the next move
    fn play(&mut self, opponent_history: &[Move]) -> Move;
    // Reset internal state for a new game
    fn reset(&mut self);
}

// 1. Always Cooperate (Sucker)
struct AlwaysCooperate;
impl Strategy for AlwaysCooperate {
    fn name(&self) -> String { "Always Cooperate".to_string() }
    fn play(&mut self, _history: &[Move]) -> Move { Move::Cooperate }
    fn reset(&mut self) {}
}

// 2. Always Defect (Mean)
struct AlwaysDefect;
impl Strategy for AlwaysDefect {
    fn name(&self) -> String { "Always Defect".to_string() }
    fn play(&mut self, _history: &[Move]) -> Move { Move::Defect }
    fn reset(&mut self) {}
}

// 3. Tit For Tat (Nice, Provocable, Forgiving)
struct TitForTat;
impl Strategy for TitForTat {
    fn name(&self) -> String { "Tit For Tat".to_string() }
    fn play(&mut self, opponent_history: &[Move]) -> Move {
        match opponent_history.last() {
            Some(last_move) => *last_move,
            None => Move::Cooperate, // Start nice
        }
    }
    fn reset(&mut self) {}
}

// 4. Grim Trigger (Unforgiving)
struct GrimTrigger {
    triggered: bool,
}
impl Strategy for GrimTrigger {
    fn name(&self) -> String { "Grim Trigger".to_string() }
    fn play(&mut self, opponent_history: &[Move]) -> Move {
        if self.triggered {
            return Move::Defect;
        }
        if let Some(Move::Defect) = opponent_history.last() {
            self.triggered = true;
            return Move::Defect;
        }
        Move::Cooperate
    }
    fn reset(&mut self) { self.triggered = false; }
}

fn play_game(s1: &mut Box<dyn Strategy>, s2: &mut Box<dyn Strategy>, rounds: usize) -> (i32, i32) {
    let mut history1 = Vec::new();
    let mut history2 = Vec::new();
    let mut score1 = 0;
    let mut score2 = 0;

    // Payoff Matrix: T=5, R=3, P=1, S=0
    // (C, C) -> (3, 3)
    // (D, D) -> (1, 1)
    // (D, C) -> (5, 0)
    // (C, D) -> (0, 5)

    for _ in 0..rounds {
        let m1 = s1.play(&history2);
        let m2 = s2.play(&history1);

        history1.push(m1);
        history2.push(m2);

        match (m1, m2) {
            (Move::Cooperate, Move::Cooperate) => { score1 += 3; score2 += 3; }
            (Move::Defect, Move::Defect) => { score1 += 1; score2 += 1; }
            (Move::Defect, Move::Cooperate) => { score1 += 5; score2 += 0; }
            (Move::Cooperate, Move::Defect) => { score1 += 0; score2 += 5; }
        }
    }
    (score1, score2)
}

fn main() {
    let mut strategies: Vec<Box<dyn Strategy>> = vec![
        Box::new(AlwaysCooperate),
        Box::new(AlwaysDefect),
        Box::new(TitForTat),
        Box::new(GrimTrigger{ triggered: false }),
    ];

    let rounds = 200;
    let mut scores: HashMap<String, i32> = HashMap::new();

    println!("--- Starting Tournament ({} Rounds) ---", rounds);

    for i in 0..strategies.len() {
        for j in i..strategies.len() { // Play against self and others
            let (s1_score, s2_score) = play_game(&mut strategies[i], &mut strategies[j], rounds);
            
            // Reset state
            strategies[i].reset();
            strategies[j].reset();

            let name1 = strategies[i].name();
            let name2 = strategies[j].name();
            
            *scores.entry(name1.clone()).or_insert(0) += s1_score;
            if i != j {
                *scores.entry(name2.clone()).or_insert(0) += s2_score;
            }

            println!("{} vs {}: {} - {}", name1, name2, s1_score, s2_score);
        }
    }

    println!("\n--- Final Results ---");
    let mut results: Vec<_> = scores.iter().collect();
    results.sort_by(|a, b| b.1.cmp(a.1)); // Sort descending

    for (name, score) in results {
        println!("{}: {}", name, score);
    }
}
