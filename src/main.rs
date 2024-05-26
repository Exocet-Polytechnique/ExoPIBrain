use exo_pi_brain_rs::config;

fn main() {
    let cfg = config::load_config("device_config.toml");
    println!("{cfg:?}");
}
