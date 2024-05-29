use exo_pi_brain_rs::{config::load_config, devices::temperature::Temperature};

fn main() {
    let config = load_config("device_config.toml");

    let mut temperature = Temperature::initialize(&config.temperatures);

    loop {
        let data = temperature.read();
        println!("{data:?}");
    }
}
