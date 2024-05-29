use rppal::spi::Spi;

use crate::config::ManometerConfig;

struct Manometer {
    spi_device: Spi,
}

impl Manometer {
    fn initalize(config: &ManometerConfig) -> Manometer {
        let spi_device = Spi::new(
            rppal::spi::Bus::Spi0,
            rppal::spi::SlaveSelect::Ss0,
            3_600_000,
            rppal::spi::Mode::Mode0,
        )
        .unwrap();
        Manometer { spi_device }
    }
}
