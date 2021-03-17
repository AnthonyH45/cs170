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
// https://stackoverflow.com/questions/26643688/how-do-i-split-a-string-in-rust
// https://doc.rust-lang.org/std/string/struct.String.html
// https://doc.rust-lang.org/std/convert/trait.Into.html
// https://stackoverflow.com/questions/31497422/filter-all-non-integers-from-string-and-yield-vector
// https://doc.rust-lang.org/std/primitive.char.html
// https://doc.rust-lang.org/std/string/struct.String.html#method.chars
// https://stackoverflow.com/questions/45282970/does-rust-have-an-equivalent-to-pythons-list-comprehension-syntax/45283083
// https://doc.rust-lang.org/std/vec/struct.Vec.html
// https://doc.rust-lang.org/1.2.0/book/for-loops.html
// https://mkaz.blog/working-with-rust/numbers/
// https://doc.rust-lang.org/std/fs/struct.OpenOptions.html
// https://stackoverflow.com/questions/65862510/why-am-i-getting-a-bad-file-descriptor-error-when-writing-file-in-rust
// https://doc.rust-lang.org/std/fs/struct.File.html
// https://doc.rust-lang.org/1.2.0/book/for-loops.html
// # CS170_largetestdata__9.txt
// # CS170_SMALLtestdata__72.txt

use std::{fs::File, io::prelude::*};

fn read_data() -> Vec<Vec<f64>> {
    let filename = "/mnt/c/Users/zax45/codeSpace/cs170/project2/main/CS170_SMALLtestdata__72.txt";
    let mut file = File::open(filename).expect("Cannot open file");

    let mut contents = String::new();
    file.read_to_string(&mut contents).expect("Cannot read file");

    let to_parse = contents.split_whitespace().collect::<Vec<&str>>();
    let mut to_return: Vec<Vec<f64>>  = Vec::new();
    let mut to_add: Vec<f64> = Vec::new();
    for (i,j) in to_parse.iter().enumerate() {
        if i % 11 == 0 && i != 0 {
            to_return.push(to_add.clone());
            to_add.clear();
            to_add.push(j.parse::<f64>().unwrap());
        } else {
            to_add.push(j.parse::<f64>().unwrap());
        }
    }
    to_return.push(to_add);
    
    return to_return;
}

fn main() {
    println!("Welcome to Anthony Hallak's Feature Selection Algorithm!");
    let data = read_data();
    println!("{:?}",data[299]);
}


// std::io::stdin().read_line(&mut filename).expect("Cannot read input");
// to_return.push(&mut to_add);
// println!("{:?}",to_add);
// println!("i = {} and j = {}", i, j.parse::<f64>().unwrap());
// println!("{:?}",to_return);
// println!("Adding {}", j.parse::<f64>().unwrap());
// fn main() -> std::io::Result<()> {
// println!("{:?}",to_parse);
// small has 11 columns, 300 rows
// let mut data = Vec::new();
// println!("{:?}",contents.chars());
// println!("Type in the name of the file to test: ");
// let mut filename = String::new();
// let filename = "/home/zax/repos/cs170/project2/CS170_SMALLtestdata__72.txt";
// let mut curr_dir = env::current_dir()?;
// curr_dir.push(filename);
// let mut unwrap = curr_dir.into_os_string().into_string().unwrap();
// println!("{}",unwrap);
// let mut file = File::open(&mut unwrap)?;
// println!("21got here");

// let mut contents = String::new();
// println!("24got here");
// file.read_to_string(&mut contents)?;

// println!("{}",contents);
// Ok(())
// }

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
