use std::{fs::File, io::prelude::*, collections::HashSet};

#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;

fn read_small_data() -> Vec<Vec<f32>> {
    let filename = "/home/zax/repos/cs170/project2/main/CS170_SMALLtestdata__72.txt";
    let mut file = File::open(filename).expect("Cannot open file");

    let mut contents = String::new();
    file.read_to_string(&mut contents).expect("Cannot read file");

    let to_parse = contents.split_whitespace().collect::<Vec<&str>>();
    let mut to_return: Vec<Vec<f32>>  = Vec::new();
    let mut to_add: Vec<f32> = Vec::new();
    for (i,j) in to_parse.iter().enumerate() {
        // hardcoded columns for now, will change later
        // 1st column for lablel, 10 columns for features
        if i % 11 == 0 && i != 0 {
            // possible fix this line? clone might be costly
            to_return.push(to_add.clone());
            to_add.clear();
            to_add.push(j.parse::<f32>().unwrap());
        } else {
            to_add.push(j.parse::<f32>().unwrap());
        }
    }
    to_return.push(to_add);
    
    return to_return;
}

fn read_large_data() -> Vec<Vec<f32>> {
    let filename = "/home/zax/repos/cs170/project2/main/CS170_largetestdata__9.txt";
    let mut file = File::open(filename).expect("Cannot open file");

    let mut contents = String::new();
    file.read_to_string(&mut contents).expect("Cannot read file");

    let to_parse = contents.split_whitespace().collect::<Vec<&str>>();
    let mut to_return: Vec<Vec<f32>>  = Vec::new();
    let mut to_add: Vec<f32> = Vec::new();
    for (i,j) in to_parse.iter().enumerate() {
        // hardcoded columns for now, will change later
        // 1st column for lablel, 100 columns for features
        if i % 101 == 0 && i != 0 {
            // possible fix this line? clone might be costly
            to_return.push(to_add.clone());
            to_add.clear();
            to_add.push(j.parse::<f32>().unwrap());
        } else {
            to_add.push(j.parse::<f32>().unwrap());
        }
    }
    to_return.push(to_add);

    return to_return;
}

#[inline(always)]
fn validate(data: &Vec<Vec<f32>>, curr_features: &HashSet<usize>, feat_to_add: usize) -> f32 {
    let total = data.len() as f32;
    let mut num_correct = 0 as f32;
    let mut feat_to_eval = std::usize::MAX;

    if feat_to_add != 0 {
        feat_to_eval = feat_to_add;
    }

    for (i,j) in data.iter().enumerate() {
        let mut nn_dist = std::f32::MAX;
        let mut nn_class = 0.0;

        for (k,l) in data.iter().enumerate() {
            if i != k {
                let mut to: Vec<f32> = Vec::new();
                for m in 0..j.len() {
                    if curr_features.contains(&m) == true || m == feat_to_eval {
                        to.push(j[m]);
                    }
                }
                let mut nn: Vec<f32> = Vec::new();
                for n in 0..l.len() {
                    if curr_features.contains(&n) == true || n == feat_to_eval {
                        nn.push(l[n]);
                    }
                }

                let mut dist: f32 = 0.0;
                // to and nn are same length, so this is ok
                for m in 0..to.len() {
                    dist = dist + f32::powf(to[m]-nn[m],2.0)
                }
                dist = dist.sqrt();

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

fn be(small_or_large: i8) {
    let data: Vec<Vec<f32>>;
    if small_or_large == 1 {
        data = read_small_data();
    } else if small_or_large == 2 {
        data = read_large_data();
    } else { return; } // if not valid, just return and do nothing

    // add all features
    let mut curr_features: HashSet::<usize> = HashSet::new();
    for (i,_) in data[0].iter().enumerate() {
        if i != 0 {
            curr_features.insert(i);
        }
    }
    // best set of features and accuracy so far
    let mut best_set: (HashSet<usize>, f32) = (HashSet::new(), -1.0);

    // default rate with all features
    let default_rate = validate(&data, &curr_features, 0);
    println!("On level 0, with all features, our accuracy is {}", default_rate);

    for (i,j) in data.iter().enumerate() {
        let mut best_accuracy: f32 = 0.0;
        let mut feat_to_rem: usize = 0;

        // out of j features, pick the lowest priority to remove
        for (k,_) in j.iter().enumerate() {
            if curr_features.contains(&k) == true && k != 0 {
                let mut remed: HashSet::<usize> = HashSet::new();
                remed.extend(&curr_features);
                remed.remove(&k);
                let current_accuracy = validate(&data, &remed, 0);

                if best_accuracy < current_accuracy {
                    best_accuracy = current_accuracy;
                    feat_to_rem = k;
                }
            }
        }

        if feat_to_rem > 0 {
            curr_features.remove(&feat_to_rem);
            println!("On level {}, we remove feature {}, and get an accuracy of {}", i+1, feat_to_rem, best_accuracy);
            if best_accuracy > best_set.1 {
                let mut to_add: HashSet::<usize> = HashSet::new();
                to_add.extend(&curr_features);
                best_set = (to_add, best_accuracy)
            }
        }
    }

    println!("Found best set of features to be: {:?}\nwith accuracy of {}",best_set.0,best_set.1);
}

fn fs(small_or_large: i8) {
    let data: Vec<Vec<f32>>;
    if small_or_large == 1 {
        data = read_small_data();
    } else if small_or_large == 2 {
        data = read_large_data();
    } else { return; } // if not valid, just return and do nothing
    
    // set of features, start empty
    let mut curr_features: HashSet::<usize> = HashSet::new();
    // best set of features and accuracy so far
    let mut best_set: (HashSet<usize>, f32) = (HashSet::new(), -1.0);

    // default rate with no features
    let default_rate = validate(&data, &curr_features, 0);
    println!("On level 0, with no features, our accuracy is {}", default_rate);

    for (i,j) in data.iter().enumerate() {
        let mut best_accuracy: f32 = 0.0;
        let mut best_feat: usize = 0;

        // out of j features, pick the highest accuracy
        for (k,_) in j.iter().enumerate() {
            if curr_features.contains(&k) == false && k != 0 {     
                let current_accuracy = validate(&data, &curr_features, k);

                if best_accuracy < current_accuracy {
                    best_accuracy = current_accuracy;
                    best_feat = k;
                }
            }
        }

        if best_feat > 0 {
            curr_features.insert(best_feat);
            println!("On level {}, we add feature {}, with accuracy {}", i+1, best_feat, best_accuracy);
            if best_accuracy > best_set.1 {
                let mut to_add: HashSet::<usize> = HashSet::new();
                to_add.extend(&curr_features);
                best_set = (to_add, best_accuracy)
            }
        }
    }

    println!("Found best set of features to be: {:?}\nwith accuracy of {}",best_set.0,best_set.1);
}

fn main() {
    println!("Welcome to Anthony Hallak's Feature Selection Algorithm!");
    println!("Performing Forward Selection on Small data");
    let start = std::time::Instant::now();
    fs(1); // 1 == small data
    println!("Seconds elapsed: {}", start.elapsed().as_secs());
    println!("");

    println!("Performing Backward Elimination on Small data");
    let start = std::time::Instant::now();
    be(1); // 1 == small data
    println!("Seconds elapsed: {}", start.elapsed().as_secs());
    println!("");

    println!("Performing Forward Selection on Large data");
    let start = std::time::Instant::now();
    fs(2); // 2 == large data
    println!("Seconds elapsed: {:?}", start.elapsed().as_secs_f32());
    println!("");

    println!("Performing Backward Elimination on Large data");
    let start = std::time::Instant::now();
    be(2); // 2 == large data
    println!("Seconds elapsed: {:?}", start.elapsed().as_secs_f32());
}
