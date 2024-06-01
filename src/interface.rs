use std::{default, io::{stdout, Stdout}};

use crossterm::{
    event::{self, KeyEventKind},
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
    ExecutableCommand,
};

use ratatui::{backend::CrosstermBackend, prelude::*, style::*, symbols, widgets::*, Terminal};

use crate::devices::SensorData;

enum State {
    Startup,
    Shutdown,
    Running,
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

    pub fn render(&mut self) {
        self.terminal
            .draw(|frame| {
                ///////////////
                // Constants
                ///////////////
                let default_style = Style::default().fg(Color::White).bg(Color::Black);
                let spacing = 3;


                /////////////
                // Widgets
                /////////////
                
                let speed_widget = Paragraph::new(format!("{:>5.2} km/h", 12.1))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP)
                        .title_style(Style::default().fg(Color::LightMagenta).add_modifier(Modifier::BOLD))
                        .title(" 󰓅 Speed ")
                );

                let efficiency_widget = Paragraph::new(format!("{:>5.2} %", 76.324))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.vertical_right,
                            ..symbols::border::PLAIN
                        })
                        .title_style(Style::default().fg(Color::LightMagenta).add_modifier(Modifier::BOLD))
                        .title(" 󰌪 Efficiency ")
                );

                let battery_widget = Paragraph::new(format!("Capacity:{:>10} %\nTemperature:{:>7.2} °C\nVoltage:{:>11.2} V\nCurrent:{:>11.2} A", 92, 142.1283, 23.21, 5.2))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.vertical_right,
                            ..symbols::border::PLAIN
                        })
                        .title_style(Style::default().fg(Color::LightGreen).add_modifier(Modifier::BOLD))
                        .title(" 󰁹 Battery ")
                );

                let hydrogen_widget = Paragraph::new(format!("Temperature:{:>8.2}  °C\nHigh Pressure:{:>7.2} Bar\nLow Pressure:     {:>6.2} Bar", 142.1283, 23.21, 5.2))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP | Borders::RIGHT)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.horizontal_down,
                            ..symbols::border::PLAIN
                        })
                        .title_style(Style::default().fg(Color::LightBlue).add_modifier(Modifier::BOLD))
                        .title("  Hydrogen ")
                );

                let fuel_cells_widget = Paragraph::new(format!("Temperature:{:>8.2} °C\nHigh Pressure:{:>7.2} Bar\nLow Pressure:{:>6.2} Bar", 142.1283, 23.21, 5.2))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP | Borders::RIGHT)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.cross,
                            top_right: symbols::line::NORMAL.vertical_left,
                            ..symbols::border::PLAIN
                        })
                        .title_style(Style::default().fg(Color::LightRed).add_modifier(Modifier::BOLD))
                        .title(" 󱐋 Fuel Cells ")
                );

                let tank_widget = Paragraph::new(format!("Temperature:{:>8.2}", 142.1283))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP | Borders::RIGHT)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.vertical_right,
                            top_right: symbols::line::NORMAL.vertical_left,
                            ..symbols::border::PLAIN
                        })
                        .title_style(Style::default().fg(Color::LightYellow).add_modifier(Modifier::BOLD))
                        .title(" 󱍗 Tank ")
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
                        .title_style(Style::default().fg(Color::White).add_modifier(Modifier::BOLD))
                        .title("  Messages ")
                );

                /////////////
                // Layouts
                /////////////

                let main_layout = Layout::default()
                    .direction(Direction::Vertical)
                    .constraints([Constraint::Length(10), Constraint::Length(4)].as_ref())
                    .split(frame.size());

                let columns_layout = Layout::default()
                    .direction(Direction::Horizontal)
                    .constraints([
                            Constraint::Length(30),
                            Constraint::Length(31)
                        ].as_ref())
                    .split(main_layout[0]);

                let left_column_layout = Layout::default()
                    .direction(Direction::Vertical)
                    .constraints([
                        Constraint::Length(2),
                        Constraint::Length(2),
                        Constraint::Length(6),
                    ].as_ref(),)
                    .split(columns_layout[0]);

                let right_column_layout = Layout::default()
                    .direction(Direction::Vertical)
                    .constraints([
                        Constraint::Length(4),
                        Constraint::Length(4),
                        Constraint::Length(2),
                    ].as_ref(),)
                    .split(columns_layout[1]);

                let messages_layout = Layout::default()
                    .direction(Direction::Horizontal)
                    .constraints([
                        Constraint::Length(61),
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
