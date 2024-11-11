import streamlit as st
import time
import numpy as np
from .Computer import Computer
from .Display import Display

class ComputerSystem:
    """Coordinates the computer and display components."""
    def __init__(self):
        # Settings container
        mb_config = st.sidebar.expander("💻 Motherboard Settings")
        with mb_config:
            mb_rows = st.slider("Motherboard Rows", min_value=2, max_value=10, value=4)
            mb_cols = st.slider("Motherboard Columns", min_value=4, max_value=16, value=8)
            
            # Add input data option
            use_input = st.checkbox("Use custom input data")
            if use_input:
                input_data = []
                for i in range(mb_rows):
                    row = st.text_input(f"Row {i+1} (space-separated 0s and 1s)", "0 " * mb_cols)
                    input_data.append([int(x) for x in row.strip().split()])
                self.initial_data = np.array(input_data)
            else:
                self.initial_data = None
    
        # Display settings container            
        display_config = st.sidebar.expander("🖥️ Display Settings")
        with display_config:    
            display_rows = st.slider("Display Rows", min_value=3, max_value=12, value=4)
            display_cols = st.slider("Display Columns", min_value=3, max_value=12, value=8)
        
        self.computer = Computer(shape=(mb_rows, mb_cols))
        self.display = Display(shape=(display_rows, display_cols))
        
    def run(self):
        """Run the system with Streamlit interface."""
        st.title("Simple Computer System Simulation")
        
        power_button = st.toggle("Power", key="on", value=False)
        n_runs_placeholder = st.empty()
        
        # Motherboard display container
        with st.expander("💻 Motherboard Status"):
            motherboard_display = st.empty()
        
        # Display output container    
        with st.expander("🖥️ Display Output"):
            display_container = st.empty()
        
        n_runs = 0
        while power_button:
            # Update motherboard using the computer processor
            motherboard = self.computer.program(self.initial_data if n_runs == 0 else None)
            motherboard_display.dataframe(motherboard, use_container_width=True)
            
            # Render the display using the display processor
            self.display.render(motherboard, display_container)
            
            # Increment and show the run count
            n_runs += 1
            n_runs_placeholder.write(f"Runs: {n_runs}")
            
            time.sleep(0.5)
            
            # Check if the power button has been turned off
            power_button = st.session_state.on
        
        # Final display state after power off
        motherboard_display.dataframe(self.computer.motherboard, use_container_width=True)
        # Display is shown even when power is off
        self.display.render(self.computer.motherboard, display_container)

# Run the computer system
if __name__ == "__main__":
    system = ComputerSystem()
    system.run()