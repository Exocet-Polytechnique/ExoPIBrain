use exo_pi_brain_rs::{devices::SensorData, interface::Interface};

fn main() {
    let mut interface = Interface::new();
    loop {
        let should_close = interface.update(&SensorData {
            fuel_cell_a: None,
            fuel_cell_b: None,
        });
        if should_close {
            break;
        }
        interface.render();
    }
}
