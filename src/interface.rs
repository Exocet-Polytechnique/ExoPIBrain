use std::io::{stdout, Stdout};

use crossterm::{
    event::{self, KeyEventKind},
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
    ExecutableCommand,
};
use ratatui::widgets::Paragraph;
use ratatui::{backend::CrosstermBackend, Terminal};
use ratatui::{layout::Rect, style::Stylize};

enum State {
    Startup,
    Shutdown,
    Running,
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

    pub fn update(&mut self) -> bool {
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
                // 1. batteries
                let text = format!("BAT T°: {:>6.2} \nBAT T°: {:>6.2}", 14.412, 140.3);
                frame.render_widget(
                    Paragraph::new(text).white().on_blue(),
                    Rect {
                        x: 0,
                        y: 0,
                        width: 25,
                        height: 2,
                    },
                );
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
