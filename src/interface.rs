use std::{default, io::{stdout, Stdout}};

use crossterm::{
    event::{self, KeyEventKind},
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
    ExecutableCommand,
};

use ratatui::{backend::CrosstermBackend, prelude::*, style::*, symbols, widgets::*, Terminal};

use crate::devices::{fuel_cell, SensorData};

enum State {
    Startup,
    Shutdown,
    Running,
}

pub struct InterfaceData {
    pub speed: Option<f32>, // km/h

    pub efficiency: Option<f32>, // 0-100%

    pub battery_capacity: Option<f32>, // 0-100%
    pub battery_voltage: Option<f32>, // V
    pub battery_current: Option<f32>, // A
    pub battery_temperature: Option<f32>, // deg C

    pub high_pressure: Option<f32>, // bar
    pub low_pressure: Option<f32>, // bar
    pub h2_plate_temperature: Option<f32>, // deg C

    pub fuel_cell_a_current: Option<f32>, // A
    pub fuel_cell_b_current: Option<f32>, // A
    pub fuel_cell_controllers_temperature: Option<f32>, // deg C

    pub h2_tanks_temperature: Option<f32>, // deg C
}

pub struct Interface {
    state: State,
    terminal: Terminal<CrosstermBackend<Stdout>>,
    data: SensorData,
    // error_rx
}

impl Interface {
    pub fn new() -> Interface {
        stdout().execute(EnterAlternateScreen).unwrap();
        enable_raw_mode().unwrap();
        let mut terminal = Terminal::new(CrosstermBackend::new(stdout())).unwrap();
        terminal.clear().unwrap();

        Interface {
            state: State::Startup,
            terminal,
            data: SensorData::default(),
        }
    }

    pub fn update(&mut self, data: &SensorData) -> bool {
        self.data = *data;

        // if error_rx.read() ...

        if event::poll(std::time::Duration::from_millis(10)).unwrap() {
            if let event::Event::Key(key) = event::read().unwrap() {
                if key.kind == KeyEventKind::Press {
                    return true;
                }
            }
        }

        false
    }

    fn format_an_optional_float(value: Option<f32>) -> String {
        match value {
            Some(x) => return format!("{:.2}", x),
            None => return "-.--".to_string(),
        }
    }

    pub fn render(&mut self, data: &InterfaceData) {
        self.terminal
            .draw(|frame| {
                ///////////////
                // Constants
                ///////////////
                let default_style = Style::default().fg(Color::White).bg(Color::Black);
                let speed_style = Style::default().fg(Color::LightMagenta);
                let efficiency_style = Style::default().fg(Color::LightMagenta);
                let battery_title_style = Style::default().fg(Color::LightGreen);
                let hydrogen_title_style = Style::default().fg(Color::LightBlue);
                let fuel_cells_title_style = Style::default().fg(Color::LightRed);
                let tank_title_style = Style::default().fg(Color::LightYellow);
                let messages_title_style = Style::default().fg(Color::White);

                /////////////
                // Widgets
                /////////////
                
                let speed_widget = Paragraph::new(format!("{:>12} km/h", Self::format_an_optional_float(data.speed)))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP)
                        .title_style(speed_style)
                        .title(" 󰓅 SPEED ")
                );

                let efficiency_widget = Paragraph::new(format!("{:>12} %", Self::format_an_optional_float(data.efficiency)))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.vertical_right,
                            ..symbols::border::PLAIN
                        })
                        .title_style(efficiency_style)
                        .title(" 󰌪 EFFICIENCY ")
                );

                let battery_widget = Paragraph::new(format!("Capacity:{:>6} %\nVoltage:{:>7} V\nCurrent:{:>7} A\nTemp:{:>10}°C", Self::format_an_optional_float(data.battery_capacity), Self::format_an_optional_float(data.battery_voltage), Self::format_an_optional_float(data.battery_current), Self::format_an_optional_float(data.battery_temperature)))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.vertical_right,
                            ..symbols::border::PLAIN
                        })
                        .title_style(battery_title_style)
                        .title(" 󰁹 BATTERY ")
                );

                let hydrogen_widget = Paragraph::new(format!("Hi Pres:{:>7} Bar\nLo Pres:{:>7} Bar\nTemp:{:>10} °C", Self::format_an_optional_float(data.high_pressure), Self::format_an_optional_float(data.low_pressure), Self::format_an_optional_float(data.h2_plate_temperature)))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP | Borders::RIGHT)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.horizontal_down,
                            ..symbols::border::PLAIN
                        })
                        .title_style(hydrogen_title_style)
                        .title("  HYDROGEN ")
                );

                let fuel_cells_widget = Paragraph::new(format!("Temp:{:>10} °C", Self::format_an_optional_float(data.fuel_cell_controllers_temperature)))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP | Borders::RIGHT)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.cross,
                            top_right: symbols::line::NORMAL.vertical_left,
                            ..symbols::border::PLAIN
                        })
                        .title_style(fuel_cells_title_style)
                        .title(" 󱐋 FUEL CELLS ")
                );

                let tank_widget = Paragraph::new(format!("Temp:{:>10} °C", 142.1283))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP | Borders::RIGHT)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.vertical_right,
                            top_right: symbols::line::NORMAL.vertical_left,
                            ..symbols::border::PLAIN
                        })
                        .title_style(tank_title_style)
                        .title(" 󱍗 TANK ")
                );

                let messages_widget = Paragraph::new(format!("No message"))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::ALL)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.vertical_right,
                            top_right: symbols::line::NORMAL.vertical_left,
                            ..symbols::border::PLAIN
                        })
                        .title_style(messages_title_style)
                        .title("  MESSAGES ")
                );

                /////////////
                // Layouts
                /////////////

                let main_layout = Layout::default()
                    .direction(Direction::Vertical)
                    .constraints([Constraint::Length(9), Constraint::Length(3)].as_ref())
                    .split(frame.size());

                let columns_layout = Layout::default()
                    .direction(Direction::Horizontal)
                    .constraints([
                            Constraint::Length(18),
                            Constraint::Length(21)
                        ].as_ref())
                    .split(main_layout[0]);

                let left_column_layout = Layout::default()
                    .direction(Direction::Vertical)
                    .constraints([
                        Constraint::Length(2),
                        Constraint::Length(2),
                        Constraint::Length(5),
                    ].as_ref(),)
                    .split(columns_layout[0]);

                let right_column_layout = Layout::default()
                    .direction(Direction::Vertical)
                    .constraints([
                        Constraint::Length(4),
                        Constraint::Length(2),
                        Constraint::Length(3),
                    ].as_ref(),)
                    .split(columns_layout[1]);

                let messages_layout = Layout::default()
                    .direction(Direction::Horizontal)
                    .constraints([
                        Constraint::Length(39),
                    ].as_ref(),)
                    .split(main_layout[1]);

                frame.render_widget(speed_widget, left_column_layout[0]);
                frame.render_widget(efficiency_widget, left_column_layout[1]);
                frame.render_widget(battery_widget, left_column_layout[2]);
                frame.render_widget(hydrogen_widget, right_column_layout[0]);
                frame.render_widget(fuel_cells_widget, right_column_layout[1]);
                frame.render_widget(tank_widget, right_column_layout[2]);
                frame.render_widget(messages_widget, messages_layout[0]);
            })
            .unwrap();
    }
}

impl Drop for Interface {
    fn drop(&mut self) {
        stdout().execute(LeaveAlternateScreen).unwrap();
        disable_raw_mode().unwrap();
    }
}
