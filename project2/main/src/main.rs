use std::{fs::File, io::prelude::*, collections::HashSet};
#[macro_use(c)]
extern crate cute;

fn read_large_data() -> Vec<Vec<f64>> {
    let filename = "/home/zax/repos/cs170/project2/main/CS170_largetestdata__9.txt";
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

fn read_small_data() -> Vec<Vec<f64>> {
    // let filename = "/mnt/c/Users/zax45/codeSpace/cs170/project2/main/CS170_SMALLtestdata__72.txt";
    let filename = "/home/zax/repos/cs170/project2/main/CS170_SMALLtestdata__72.txt";
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
                // let mut to: Vec<f64> = Vec::new();
                // for m in 0..j.len() {
                //     if curr_features.contains(&m) == false || m == feat_to_add {
                //         to.push(j[m]);
                //     }
                // }
                // let mut nn: Vec<f64> = Vec::new();
                // for m in 0..l.len() {
                //     if curr_features.contains(&m) == false || m == feat_to_add {
                //         nn.push(l[m]);
                //     }
                // }
                let to: Vec<f64> = c![j[m], for m in 0..j.len(), if curr_features.contains(&m) || m == feat_to_add];
                let nn: Vec<f64> = c![l[m], for m in 0..l.len(), if curr_features.contains(&m) || m == feat_to_add];
                // let dist = c![f64::pow((a-b),2), for a in j.iter().zip(l.iter()).len() ].iter().sum().sqrt();
                // println!("Eval: {:?}\n{:?}\n\n",to,nn);
                let dist = c![f64::powf(to[a]-nn[a],2.0), for a in 0..to.len()].iter().sum::<f64>().sqrt();
                // j and l are same length, so this is ok
                // let mut dist: f64 = 0.0;
                // // let mut sum: f64 = 0.0;
                // for m in 0..l.len() {
                //     dist = dist + f64::powf(j[m]-l[m],2.0)
                // }
                // dist = dist.sqrt();

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
    let start = std::time::Instant::now();
    fs(data);
    println!("Seconds elapsed: {}", start.elapsed().as_secs());
    println!("Performing Forward Selection on Large data");
    let data = read_large_data();
    let start = std::time::Instant::now();
    fs(data);
    println!("Seconds elapsed: {}", start.elapsed().as_secs());
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
// https://users.rust-lang.org/t/what-is-wrong-no-method-found-for-type-in-the-current-scope/2282
// https://stackoverflow.com/questions/23100534/how-to-sum-the-values-in-an-array-slice-or-vec-in-rust
// https://www.reddit.com/r/rust/comments/2v2mba/how_to_use_sqrt_function_in_rust/
// https://www.reddit.com/r/rust/comments/61agwc/how_do_i_powx_y_in_rust/
// https://stackoverflow.com/questions/34463980/rust-cant-find-crate
// https://doc.rust-lang.org/cargo/guide/dependencies.html
// https://stackoverflow.com/questions/27893223/how-do-i-iterate-over-a-range-with-a-custom-step
// https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.zip
// https://github.com/mattgathu/cute
// https://www.reddit.com/r/rust/comments/6o1wm2/list_comprehensions/
// https://doc.rust-lang.org/std/thread/fn.sleep.html
// https://doc.rust-lang.org/std/primitive/index.html
// https://doc.rust-lang.org/rust-by-example/primitives/tuples.html
// https://doc.rust-lang.org/std/collections/hash_set/struct.HashSet.html#method.insert
// https://doc.rust-lang.org/std/collections/index.html
// https://doc.rust-lang.org/std/time/struct.Instant.html

// # CS170_largetestdata__9.txt
// # CS170_SMALLtestdata__72.txt