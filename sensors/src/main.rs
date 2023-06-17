//use sysinfo::{NetworkExt, NetworksExt, ProcessExt, System, SystemExt};
use sysinfo::{System, SystemExt, CpuExt};
use log::LevelFilter;
use log::{info, warn};

fn main() {
    simple_logging::log_to_file("test.log", LevelFilter::Info);
    log::info!("Collecting system information.");
    let mut sys = System::new_all();

    

    println!("=> components:");
    for component in sys.components() {
        println!("{:?}", component);
    }
    
    let total_ram: f64 = sys.total_memory() as f64;
    let used_ram: f64 = sys.used_memory() as f64;
    // RAM and swap information:
    println!("total memory: {} Gigabytes", total_ram / 1000000000.000);
    println!("used memory : {} Gigabytes", used_ram / 1000000000.000);
    // println!("total swap  : {} bytes", sys.total_swap());
    // println!("used swap   : {} bytes", sys.used_swap());

    // loop {
    //     sys.refresh_cpu(); // Refreshing CPU information.
    //     for cpu in sys.cpus() {
    //         print!("{}% ", cpu.cpu_usage());
    //     }
    //     std::thread::sleep(std::time::Duration::from_millis(500));
    // }
}
