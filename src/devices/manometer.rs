use rppal::spi::Spi;

use crate::config::ManometerConfig;

pub struct Manometer {
    spi_device: Spi,
}

impl Manometer {
    pub fn initalize(config: &ManometerConfig) -> Manometer {
        let spi_device = Spi::new(
            rppal::spi::Bus::Spi0,
            rppal::spi::SlaveSelect::Ss0,
            3_600_000,
            rppal::spi::Mode::Mode0,
        )
        .unwrap();
        Manometer { spi_device }
    }

    pub fn read(&self) -> Option<f32> {
        let out_data: [u8; 2] = [3, 1];
        let mut in_data: [u8; 2] = [0; 2];
        let size = self.spi_device.transfer(&mut in_data, &out_data).ok()?;
        if size != 2 {
            return None;
        }

        todo!()
    }
}
