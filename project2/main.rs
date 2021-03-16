// https://users.rust-lang.org/t/why-is-it-so-difficult-to-get-user-input-in-rust/27444
// https://doc.rust-lang.org/std/fs/struct.File.html


fn main() {
    let data = fs::read_to_string("/etc/hosts").expect("Unable to read file");
    println!("{}", data);
}