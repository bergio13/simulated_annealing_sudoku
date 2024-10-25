import numpy as np

# Simulated Annealing algorithm
def simulated_annealing(initial_state, objective_function, neighborhood_operator, T_init, cooling_rate=0.95, max_iter=20_000, reheat_threshold=500):
    t = 0
    current_state = initial_state
    T = T_init
    current_energy = objective_function(current_state)
    best_state = current_state
    best_energy = current_energy
    stagnant_iterations = 0
    
    # Lists to store metrics for plotting
    objective_values = []
    temperatures = []
    accepted_moves = []
    
    while t < max_iter and current_energy != 0:
        # get neighbor 
        swap_pos1, swap_pos2 = neighborhood_operator(current_state)
        
        # check energy difference
        proposed_energy = objective_function(current_state)
        delta_E = proposed_energy - current_energy
        
        if delta_E < 0 or np.random.rand() < np.exp(-abs(delta_E) / T):
            current_energy = proposed_energy
            accepted_moves.append(1)
            stagnant_iterations = 0
            
            if current_energy < best_energy:
                best_state = np.copy(current_state)
                best_energy = current_energy
        else:
            # Revert the swap if not accepted
            current_state[swap_pos1], current_state[swap_pos2] = current_state[swap_pos2], current_state[swap_pos1]
            accepted_moves.append(0)
            stagnant_iterations += 1
            
        # Record the current objective value and temperature
        objective_values.append(current_energy)
        temperatures.append(T)
        
        # Update temperature and iteration count
        T = T * cooling_rate
        t += 1
        
        # Restart if stuck in local optima
        # Reheat if stuck in local optima
        if stagnant_iterations >= reheat_threshold:
            T = T_init * 0.75 # Increase the temperature
            stagnant_iterations = 0  # Reset stagnation counter but keep the best state
    
    return best_state, objective_values, temperatures, accepted_moves
