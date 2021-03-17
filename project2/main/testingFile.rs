use std::fs::OpenOptions;
use std::io::BufReader;
use std::io::prelude::*;
use std::io::Write;

fn main() -> std::io::Result<()> {
    println!("0");
//    let mut file = File::create("foo.txt")?;
    let mut file = OpenOptions::new()
        .write(true)
        .create(true)
        .read(true)
        .truncate(true)
        .open("foo.txt")
        .unwrap();

    let result = file.write_all(b"hello\n");

    match result {
        Ok(_) => println!("written"),
        Err(e) => panic!("failed to write: {}",{e}),
    }

    println!("1");
    //file.write_all(b"Hello World!")?;
    println!("2");
    let mut buf_reader = BufReader::new(file);
    println!("3");
    let mut contents = String::new();
    println!("4");
    buf_reader.read_to_string(&mut contents)?;
    println!("5");
    println!("{}",contents);
    println!("6");
    Ok(())
}
