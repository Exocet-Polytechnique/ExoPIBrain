use exo_pi_brain_rs::{
    config::load_config,
    devices::{actuator::Actuator, temperature::Temperature},
};
use rppal::gpio::Gpio;

fn main() {
    let config = load_config("device_config.toml");

    let mut temperature = Temperature::initialize(&config.temperatures);
    let gpio = Gpio::new().unwrap();
    let mut actuator = Actuator::initialize(&gpio, &config.valve1);

    let mut is_open = false;

    loop {
        let data = temperature.read();
        println!("Temperature: {data:?}");

        println!("Actuator: {}", actuator.get_status());
        if is_open {
            actuator.close_valve()
        } else {
            actuator.open_valve()
        };
        is_open = !is_open;
    }
}
