use std::{fs::File, io::prelude::*, collections::HashSet};
#[macro_use(c)]
extern crate cute;
// use std::{thread, time};

// fn read_large_data() -> Vec<Vec<f64>> {
//     let filename = "/mnt/c/Users/zax45/codeSpace/cs170/project2/main/CS170_largetestdata__9.txt";
//     let mut file = File::open(filename).expect("Cannot open file");

//     let mut contents = String::new();
//     file.read_to_string(&mut contents).expect("Cannot read file");

//     let to_parse = contents.split_whitespace().collect::<Vec<&str>>();
//     let mut to_return: Vec<Vec<f64>>  = Vec::new();
//     let mut to_add: Vec<f64> = Vec::new();
//     for (i,j) in to_parse.iter().enumerate() {
//         if i % 11 == 0 && i != 0 {
//             to_return.push(to_add.clone());
//             to_add.clear();
//             to_add.push(j.parse::<f64>().unwrap());
//         } else {
//             to_add.push(j.parse::<f64>().unwrap());
//         }
//     }
//     to_return.push(to_add);
    
//     return to_return;
// }

fn read_small_data() -> Vec<Vec<f64>> {
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

fn validate(data: Vec<Vec<f64>>, curr_features: HashSet<usize>, feat_to_add: usize) -> f64 {
    let total = data.len() as f64;
    let mut num_correct = 0 as f64;

    for (i,j) in data.iter().enumerate() {
        // println!("Finding nn for {:?}", j);
        let mut nn_dist = std::f64::MAX;
        let mut nn_class = 0.0;

        for (k,l) in data.iter().enumerate() {
            if i != k {
                let to: Vec<f64> = c![j[m], for m in 0..j.len(), if curr_features.contains(&m) || m == feat_to_add];
                let nn: Vec<f64> = c![l[m], for m in 0..l.len(), if curr_features.contains(&m) || m == feat_to_add];
                // let dist = c![f64::pow((a-b),2), for a in j.iter().zip(l.iter()).len() ].iter().sum().sqrt();
                let dist = c![f64::powf(to[a]-nn[a],2.0), for a in 0..to.len()].iter().sum::<f64>().sqrt();

                if dist < nn_dist {
                    nn_dist = dist;
                    nn_class = l[0]
                }
            }
        }

        if nn_class == j[0] {
            num_correct = num_correct + 1.0;
        }
    }

    let acc = num_correct / total;
    return acc;
}

fn fs(data: Vec<Vec<f64>>) {
    // set of features
    let mut curr_features: HashSet::<usize> = HashSet::new();
    // best set of features and accuracy so far
    let mut best_set: (HashSet<usize>, f64) = (HashSet::new(), -1.0);

    for (i,j) in data.iter().enumerate() {
        // println!("i={}",i);
        let mut best_accuracy: f64 = 0.0;
        let mut best_feat: usize = 0;

        // out of l features, 
        for (k,l) in j.iter().enumerate() {
            // println!("k={}",k);
            if curr_features.contains(&k) == false && k != 0 {                
                // let ten_millis = time::Duration::from_millis(1000);
                // let now = time::Instant::now();
                // thread::sleep(ten_millis);
                // println!("k not seen before");
                let current_accuracy = validate(data.clone(), curr_features.clone(), k);
                // println!("curr_acc={}",current_accuracy);

                if best_accuracy < current_accuracy {
                    best_accuracy = current_accuracy;
                    // println!("New best accuracy={}",best_accuracy);
                    best_feat = k;
                }
            }
        }

        // println!("Done with inner loop, best_feat={}",best_feat);
        if best_feat > 0 {
            curr_features.insert(best_feat);
            println!("On level {}, we add feature {}, with accuracy {}", i+1, best_feat, best_accuracy);
            if best_accuracy > best_set.1 {
                best_set = (curr_features.clone(), best_accuracy)
            }
        }
    }

    println!("Found best set of features to be: {:?}\nwith accuracy of {}",best_set.0,best_set.1);
}

fn main() {
    println!("Welcome to Anthony Hallak's Feature Selection Algorithm!");
    let data = read_small_data();
    println!("Performing Forward Selection on Small data");
    fs(data);
}










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
// https://doc.rust-lang.org/std/vec/struct.Vec.html#method.len
// https://doc.rust-lang.org/rust-by-example/std/vec.html
// https://stackoverflow.com/questions/61660794/convert-vecf641-to-vecf64
// https://stackoverflow.com/questions/28800121/what-do-i-have-to-do-to-solve-a-use-of-moved-value-error
// https://doc.rust-lang.org/std/vec/struct.Vec.html#method.new
// https://stackoverflow.com/questions/28991050/how-to-iterate-a-vect-with-the-indexed-position
// https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.position
// https://stackoverflow.com/questions/26643688/how-do-i-split-a-string-in-rust
// https://doc.rust-lang.org/std/vec/struct.Vec.html
// https://stackoverflow.com/questions/27312069/how-can-i-iterate-over-a-vector-of-functions-and-call-each-of-them

// # CS170_largetestdata__9.txt
// # CS170_SMALLtestdata__72.txt


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
