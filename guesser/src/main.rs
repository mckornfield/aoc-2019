use std::io;
use std::cmp::Ordering;
use rand::Rng;

fn main() {
    println!("Guess the number");

    let secret_number = rand::thread_rng().gen_range(1,101);

    let mut count = 0;
    loop {
    let mut guess = String::new();

    println!("Please input your guess");
    io::stdin().read_line(& mut guess)
        .expect("Failed to read line");

    let guess : u32 = match guess.trim().parse() {
        Ok(num) => num,
        Err(_) => {println!("that's wrong!"); continue;},
    };
    
    println!("You guessed: {}", guess);

        println!("Guess number {}", count);
        match guess.cmp(&secret_number) {
            Ordering::Less => println!("too small!"),
            Ordering::Equal => {
                println!("too equal!");
                break;
            },
            Ordering::Greater => println!("too big!"),
        }
        count+= 1;
    }
    println!("Secret number was {}", secret_number);
}

