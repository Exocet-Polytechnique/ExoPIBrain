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
                
                let speed_widget = Paragraph::new(format!("{:>5.2} km/h", 12.1))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP)
                        .title_style(speed_style)
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
                        .title_style(efficiency_style)
                        .title(" 󰌪 Efficiency ")
                );

                let battery_widget = Paragraph::new(format!("Capacity:{:>10} %\nVoltage:{:>11.2} V\nCurrent:{:>11.2} A\nTemperature:{:>7.2} °C", 92, 23.21, 5.2, 142.1283))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.vertical_right,
                            ..symbols::border::PLAIN
                        })
                        .title_style(battery_title_style)
                        .title(" 󰁹 Battery ")
                );

                let hydrogen_widget = Paragraph::new(format!("High Pressure:{:>7.2} Bar\nLow Pressure:{:>8.2} Bar\nTemperature:{:>9.2} °C", 399.0, 5.29312, 142.1283))
                .style(default_style)
                .block(
                    Block::default()
                        .borders(Borders::LEFT | Borders::TOP | Borders::RIGHT)
                        .border_set(symbols::border::Set {
                            top_left: symbols::line::NORMAL.horizontal_down,
                            ..symbols::border::PLAIN
                        })
                        .title_style(hydrogen_title_style)
                        .title("  Hydrogen ")
                );

                let fuel_cells_widget = Paragraph::new(format!("Fuel Cell A:{:>9.2} Bar\nFuel Cell B:{:>9.2} Bar\nTemperature:{:>9.2} °C", 5800.07, 5803.07, 142.1283))
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
                        .title(" 󱐋 Fuel Cells ")
                );

                let tank_widget = Paragraph::new(format!("Temperature:{:>9.2} °C", 142.1283))
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
                        .title_style(messages_title_style)
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
                            Constraint::Length(23),
                            Constraint::Length(27)
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
                        Constraint::Length(50),
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
