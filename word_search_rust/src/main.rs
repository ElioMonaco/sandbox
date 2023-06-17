/* 
Search for a pattern in a file and display the lines that contain it.
Built following https://rust-cli.github.io/book/index.html
*/

#![allow(unused)]
use clap::Parser;
use simple_logger::SimpleLogger;
use log::{info, warn};
use std::io::{BufReader,BufRead,Error};
use std::fs::File;
use std::io::Read;
use anyhow::{Context, Result};

fn find_matches<R: Read>(reader: &mut BufReader<R>, pattern: &str) -> i32 {
        
    /*
    search for the pattern in each line of the file
    print each line that contains the pattern
    */
    let mut lines: i32 = 0;
    let mut total_occurrences: i32 = 0;
    for line in reader.lines() {
        /*
        seems like parsing files into string is not a good idea: https://stackoverflow.com/questions/53325547/rust-utf-8-error-thread-main-panicked-at-called-resultunwrap
        therfore I am parsing in a vector
        */
        let line_vec: Result<String, Error> = line;
        /*
        trying to handle issues with parsing errors without interrupting the search
        will at least print what line was unable to parse as well as the error
        */
        match &line_vec {
            Err(_) => { log::error!("Failed to decode line {}: {:?}", lines,&line_vec) }
            Ok(line_vec) => { if line_vec.contains(&pattern) {
                                            println!("{}|| {}", lines, line_vec);
                                            total_occurrences += 1
                                        } 
                                    }
        };
        /*
        old attempt was parsing the lines into strings
        */
        //let line_unwrap: &str = &line_vec.unwrap();
        lines += 1;
    }
    total_occurrences
}

#[derive(Parser)]

struct Cli {
    /*
    the pattern to look for and the path to the file to read
    */
    pattern: String,
    path: std::path::PathBuf,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {

    /*
    start environment logger
    */
    SimpleLogger::new().init().unwrap();
    log::info!("Parsing file");
    /*
    parsing the input values
    */
    let args = Cli::parse();
    /*
    read the file from the parsed path
    */
    let file = File::open(&args.path).with_context(|| format!("could not read file `{}`", args.path.display()))?;
    log::info!("Creating buffer");
    /*
    create a buffer for memory efficiency
    */
    let mut reader = BufReader::new(file);

    /*
    print input parameters and execute search
    */    
    log::info!("Searching for occurrences of `{}` in file `{}`", &args.pattern, &args.path.display());
    log::info!("Found {} occurrence(s)", find_matches(&mut reader, &args.pattern));

    Ok(())
}