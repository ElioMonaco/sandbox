//https://github.com/emilk/egui/blob/master/examples


#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] // hide console window on Windows in release


use eframe::egui;
use std::thread;
use std::time::Duration;
use systemstat::{System, Platform, saturating_sub_bytes};

fn sensor_data() -> Result<f32, &'static str>{
    let sys = System::new();

    match sys.cpu_temp() {
        Ok(cpu_temp) => Ok(cpu_temp),
        Err(x) => println!("CPU temp: {}", x)
    }

}

fn main() {
    sensor_data()
}

// fn main() -> Result<(), eframe::Error> {
//     env_logger::init(); // Log to stderr (if you run with `RUST_LOG=debug`).
//     let options = eframe::NativeOptions {
//         decorated: false,
//         transparent: true,
//         initial_window_size: Some(egui::vec2(100.0, 120.0)),
//         initial_window_pos: Some(egui::pos2(10.0, 10.0)),
//         ..Default::default()
//     };
//     eframe::run_native(
//         "Sensors",
//         options,
//         Box::new(|_cc| Box::<MyApp>::default()),
//     )
// }

// struct MyApp {
//     cpu_temp: String,
//     age: u32,
// }

// impl Default for MyApp {
//     fn default() -> Self {
//         Self {
//             //cpu_temp: "Arthur".to_owned(),
//             cpu_temp: sys_info(),
//             age: 42,
//         }
//     }
// }

// impl eframe::App for MyApp {
//     fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
//         egui::CentralPanel::default().show(ctx, |ui| {
//             //ui.heading("My egui Application");
//             ui.horizontal(|ui| {
//                 let name_label = ui.label("Your name: ");
//                 // ui.text_edit_singleline(&mut self.name)
//                 //     .labelled_by(name_label.id);
//             });
//             // ui.add(egui::Slider::new(&mut self.age, 0..=120).text("age"));
//             // if ui.button("Click each year").clicked() {
//             //     self.age += 1;
//             // }
//             // ui.label(format!("Hello '{}', age {}", self.name, self.age));
//         });
//     }
// }
