use std::io::{stdout, Stdout};

use crossterm::{
    event::{self, KeyEventKind}, terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen}, ExecutableCommand
};
use ratatui::{layout::{Constraint, Direction, Layout}, style::{Color, Style}, symbols, widgets::{Block, Borders, Paragraph}};
use ratatui::{backend::CrosstermBackend, Terminal};

use crate::devices::common::message::Message;

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

    pub fuel_cell_a_temperature: Option<f32>, // A
    pub fuel_cell_b_temperature: Option<f32>, // A
    pub fuel_cell_controllers_temperature: Option<f32>, // deg C
    pub h2_tanks_temperature: Option<f32>, // deg C
}

pub struct Interface {
    state: State,
    terminal: Terminal<CrosstermBackend<Stdout>>,
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
        }
    }

    fn format_an_optional_float(value: Option<f32>) -> String {
        match value {
            Some(x) => return format!("{:.2}", x),
            None => return "-.--".to_string(),
        }
    }

    pub fn dispatch_message(&mut self, error: &Message) {}

    pub fn should_quit(&mut self, millis: u64) -> bool {
        if event::poll(std::time::Duration::from_millis(millis)).unwrap() {
            if let event::Event::Key(key) = event::read().unwrap() {
                if key.kind == KeyEventKind::Press {
                    return true;
                }
            }
        }

        false
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
                let temperatures_title_style = Style::default().fg(Color::LightYellow);
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

                let hydrogen_widget = Paragraph::new(format!("Hi Pres:{:>7} Bar\nLo Pres:{:>7} Bar", Self::format_an_optional_float(data.high_pressure), Self::format_an_optional_float(data.low_pressure)))
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

                let temperatures_widget = Paragraph::new(format!("H2 Plate:{:>7} °C\nFC A:{:>11} °C\nFC B:{:>11} °C\nFC Contro:{:>6} °C\nTanks:{:>10} °C",
                    Self::format_an_optional_float(data.h2_plate_temperature),
                    Self::format_an_optional_float(data.fuel_cell_a_temperature),
                    Self::format_an_optional_float(data.fuel_cell_b_temperature),
                    Self::format_an_optional_float(data.fuel_cell_controllers_temperature),
                    Self::format_an_optional_float(data.h2_tanks_temperature)
                ))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP | Borders::RIGHT)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.cross,
                            top_right: symbols::line::NORMAL.vertical_left,
                            ..symbols::border::PLAIN
                        })
                        .title_style(temperatures_title_style)
                        .title(" 󱍗 TEMPERATURES ")
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
                        Constraint::Length(3),
                        Constraint::Length(6),
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
                frame.render_widget(temperatures_widget, right_column_layout[1]);
                frame.render_widget(messages_widget, messages_layout[0]);
            })
            .unwrap();
    }
}

impl InterfaceData {
    pub fn new() -> Self {
        Self {
            speed: None,

            efficiency: None,

            battery_capacity: None,
            battery_voltage: None,
            battery_current: None,
            battery_temperature: None,

            high_pressure: None,
            low_pressure: None,

            h2_plate_temperature: None,

            fuel_cell_a_temperature: None,
            fuel_cell_b_temperature: None,
            fuel_cell_controllers_temperature: None,
            h2_tanks_temperature: None,
        }
    }
}

impl Drop for Interface {
    fn drop(&mut self) {
        stdout().execute(LeaveAlternateScreen).unwrap();
        disable_raw_mode().unwrap();
    }
}
