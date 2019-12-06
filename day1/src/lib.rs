use math::round;
use std::fs;


pub fn get_fuel(num : u32) -> u32{
    let floored_val: u32 = round::floor( (num / 3).into(), 0) as u32;
    if floored_val <= 2 {
        return 0
    }
    return floored_val - 2;
}

pub fn get_fuel_cumulative(mass: u32) -> u32 {
    let first_needed_fuel = get_fuel(mass);

    let mut next_needed_amount = get_fuel(first_needed_fuel);
    if next_needed_amount <= 0 {
        return first_needed_fuel
    }
    let mut total_fuel = first_needed_fuel;
    while next_needed_amount > 0 {
        total_fuel += next_needed_amount;
        next_needed_amount = get_fuel(next_needed_amount);
    }
    return total_fuel;
}

pub fn get_fuel_sum(nums : &[u32]) -> u32{
    return nums.iter().fold(0, |acc, &x| acc + get_fuel(x))
}

pub fn get_fuel_sums_cumulative(nums : &[u32]) -> u32{
    return nums.iter().fold(0, |acc, &x| acc + get_fuel_cumulative(x))
}

pub fn get_fuels_from_file(file_name : &str) -> Vec<u32> {
    let contents = fs::read_to_string(file_name).expect("everything ok");

    let vals: Vec<u32> = contents
        .split('\n')
        .filter(|s| !s.is_empty())
        .map(|s| s.parse().unwrap())
        .collect();
    // println!("{}", vals);
    return vals;
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_simple_cases() {
        for vals in vec![
            (12, 2),
            (14, 2),
            (1969, 654),
            (100756, 33583),
            ] {
            let input = vals.0;
            let expected = vals.1;

            let result = get_fuel(input);
            assert_eq!(result, expected);
        }
    }
    #[test]
    fn test_get_all_fuel_vals() {
        let nums = [12,14,1969,100756];
        let result = get_fuel_sum(&nums);
        assert_eq!(result, 2+2+654+33583);
    }

    #[test]
    fn test_get_fuels_from_file() {
        let expected_masses = vec![12,14,1969,100756];
        let result = get_fuels_from_file("src/puzzle_input_test.txt");
        assert_eq!(result, expected_masses);
    }

    #[test]
    fn test_get_fuels_from_file_p1() {
        let masses = get_fuels_from_file("src/puzzle_input.txt");
        let result = get_fuel_sum(&masses);
        assert_eq!(3287620, result);
    }


    #[test]
    fn test_get_fuel_cumulative() {
        for vals in vec![
            (12, 2),
            (14, 2),
            (1969, 966),
            (100756, 50346),
            ] {
            let input = vals.0;
            let expected = vals.1;

            let result = get_fuel_cumulative(input);
            assert_eq!(result, expected);
        }
    }

    #[test]
    fn test_get_fuels_from_file_p2() {
        let masses = get_fuels_from_file("src/puzzle_input.txt");
        let result = get_fuel_sums_cumulative(&masses);
        assert_eq!(3287620, result);
    }

}
