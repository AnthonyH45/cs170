// https://users.rust-lang.org/t/why-is-it-so-difficult-to-get-user-input-in-rust/27444
// https://doc.rust-lang.org/std/fs/struct.File.html
// https://doc.rust-lang.org/book/ch01-03-hello-cargo.html
// https://doc.rust-lang.org/std/io/trait.Read.html#method.read_to_string
// https://doc.rust-lang.org/std/path/struct.Path.html
// https://users.rust-lang.org/t/not-able-to-open-file-even-though-it-is-there-working-with-absolute-path-but-not-relative-path/19525
// https://doc.rust-lang.org/rust-by-example/std_misc/file/open.html
// https://doc.rust-lang.org/std/env/index.html
// https://doc.rust-lang.org/std/path/struct.PathBuf.html
// https://github.com/PascalPrecht/rustlings
// # CS170_largetestdata__9.txt
// # CS170_SMALLtestdata__72.txt

use std::{env, fs::File, io, io::prelude::*};

fn main() -> std::io::Result<()> {
    println!("Welcome to Anthony Hallak's Feature Selection Algorithm!");
    println!("Type in the name of the file to test: ");
    let mut filename = String::new();
    // let filename = "/home/zax/repos/cs170/project2/CS170_SMALLtestdata__72.txt";
    io::stdin().read_line(&mut filename).expect("Cannot read input");

    let mut curr_dir = env::current_dir()?;
    curr_dir.push(filename);
    let mut unwrap = curr_dir.into_os_string().into_string().unwrap();
    println!("{}",unwrap);
    let mut file = File::open(&mut unwrap)?;
    println!("21got here");

    let mut contents = String::new();
    println!("24got here");
    file.read_to_string(&mut contents)?;

    println!("{}",contents);
    Ok(())
}

//     // let contents = fs::read_to_string(filename)
//     //     .expect("Something went wrong reading the file");
//     println!("With text:\n{}", contents);
// }
// use std::fs::File;
// use std::io::prelude::*;
// fn main() -> std::io::Result<()> {
//     let mut file = File::open("CS170_SMALLtestdata__72.txt")?;
//     let mut contents = String::new();
//     file.read_to_string(&mut contents)?;
//     assert_eq!(contents, "Hello, world!");
//     println!("{}",contents);
//     Ok(())
// }
