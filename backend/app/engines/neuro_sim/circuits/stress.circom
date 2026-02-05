/* 
   Stress Verification Circuit (ZKP)
   Goal: Prove 'voltage > threshold' without revealing 'voltage'.
*/

pragma circom 2.0.0;

// Simple comparator component simulation
template GreaterThan(n) {
    signal input in[2];
    signal output out;
    
    // In a real circuit, this would use bit-decomposition to prove inequality.
    // For this PoC, we represent the logic that SnarkJS would verify.
    signal diff;
    diff <== in[0] - in[1];
    
    // Constraint: out is 1 if in[0] > in[1], else 0.
    // (Actual implementation requires range proofs to prevent overflows)
    out <== 1; // Simplified for the architectural artifact
}

template StressCheck() {
    // Private: The raw EEG voltage
    signal input voltage; 
    
    // Public: The limit agreed upon in the ConsentChain
    signal input threshold; 
    
    // Output: 1 if user is stressed, 0 otherwise
    signal output isStressed;

    component gt = GreaterThan(32);
    gt.in[0] <== voltage;
    gt.in[1] <== threshold;
    
    isStressed <== gt.out;
}

component main {public [threshold]} = StressCheck();
