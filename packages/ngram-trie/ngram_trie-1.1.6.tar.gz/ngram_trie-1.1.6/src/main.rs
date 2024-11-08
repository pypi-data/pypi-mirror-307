#![allow(warnings)]
pub mod trie;
pub mod smoothing;
pub mod smoothed_trie;

use trie::NGramTrie;
use trie::trienode::TrieNode;
use smoothing::ModifiedBackoffKneserNey;
use sorted_vector_map::SortedVectorMap;
use smoothed_trie::SmoothedTrie;
use smoothing::CACHE_S_C;
use smoothing::CACHE_S_N;
use trie::CACHE_C;
use trie::CACHE_N;

use rclite::Arc;
use serde::Serialize;
use serde::Deserialize;
use std::time::Instant;
use std::fs::OpenOptions;
use std::io::Write;
use actix_web::{web, App, HttpServer, Responder};
use log::{info, debug, error};

fn test_performance_and_write_stats(tokens: Arc<Vec<u16>>, data_sizes: Vec<usize>, n_gram_lengths: Vec<u32>, output_file: &str) {
    let mut file = OpenOptions::new()
        .write(true)
        .create(true)
        .append(true)
        .open(output_file)
        .unwrap();

    writeln!(file, "Data Size,N-gram Length,Fit Time (s),RAM Usage (MB)").unwrap();

    let num_threads = std::thread::available_parallelism()
        .map(|p| p.get()).unwrap_or(1);

    for data_size in data_sizes {
        for n_gram_length in &n_gram_lengths {
            //let ranges = NGramTrie::split_into_ranges(tokens.clone(), data_size, num_threads, *n_gram_length);
            // Measure fit time
            let start = Instant::now();
            //let trie = NGramTrie::fit_multithreaded(tokens.clone(), ranges, *n_gram_length);
            //let trie = NGramTrie::fit_multithreaded_recursively(tokens.clone(), ranges, *n_gram_length);
            let trie = NGramTrie::fit(tokens.clone(), *n_gram_length, 2_usize.pow(14), Some(data_size));
            let fit_time = start.elapsed().as_secs_f64(); 
            // Measure RAM usage
            let ram_usage = 0 as f64 / (1024.0 * 1024.0);

            // Write statistics to file
            writeln!(
                file,
                "{},{},{},{:.2}",
                data_size, n_gram_length, fit_time, ram_usage
            ).unwrap();

            println!(
                "Completed: Data Size = {}, N-gram Length = {}, Fit Time = {:.2}, RAM Usage = {:.2} MB",
                data_size, n_gram_length, fit_time, ram_usage
            );
        }
    }
}

fn run_performance_tests(filename: &str) {
    println!("----- Starting performance tests -----");
    let tokens = NGramTrie::load_json(filename, Some(100_000_000)).unwrap();
    println!("Tokens loaded: {}", tokens.len());
    let data_sizes = (1..10).map(|x| x * 1_000_000).chain((1..=10).map(|x| x * 10_000_000)).collect::<Vec<_>>();
    let n_gram_lengths = [7].to_vec();
    let output_file = "fit_sorted_vector_map_with_box.csv";

    test_performance_and_write_stats(tokens, data_sizes, n_gram_lengths, output_file);
}

#[derive(Serialize, Deserialize)]
struct PredictionRequest {
    history: Vec<u16>,
    predict: u16,
}

#[derive(Serialize)]
struct PredictionResponse {
    probabilities: Vec<(String, Vec<(u16, f64)>)>,
}

async fn predict_probability(req: web::Json<PredictionRequest>, smoothed_trie: web::Data<SmoothedTrie>) -> impl Responder {
    let mut probabilities = smoothed_trie.get_prediction_probabilities(&req.history);

    let response = PredictionResponse {
        probabilities: probabilities,
    };
    web::Json(response)
}

#[tokio::main]
async fn start_http_server(smoothed_trie: Arc<SmoothedTrie>) -> std::io::Result<()> {
    println!("----- Starting HTTP server -----");
    HttpServer::new(move || {
        App::new()
            .app_data(smoothed_trie.clone())
            .service(web::resource("/predict").route(web::post().to(predict_probability)))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}

fn main() {
    env_logger::Builder::new()
        .format(|buf, record| {
            writeln!(
                buf,
                "{} [{}] {}",
                chrono::Local::now().format("%H:%M:%S"),
                record.level(),
                record.args()
            )
        })
        .filter_level(log::LevelFilter::Debug)
        .init();
    //run_performance_tests("tokens.json");
    //NGramTrie::estimate_time_and_ram(475_000_000);
    
    let mut smoothed_trie = SmoothedTrie::new(NGramTrie::new(8, 2_usize.pow(14)), None);

    let tokens = NGramTrie::load_json("../170k_tokens.json", None).unwrap();
    smoothed_trie.fit(tokens, 8, 0, None, Some("_modified_kneser_ney".to_string()));

    smoothed_trie.save("../170k_tokens");

    //smoothed_trie.load("../170k_tokens");

    info!("----- Getting rule count -----");
    let rule = NGramTrie::_preprocess_rule_context(&vec![987, 4015, 935, 2940, 3947, 987, 4015], Some("+++*++*"));
    let start = Instant::now();
    let count = smoothed_trie.get_count(rule.clone());
    let elapsed = start.elapsed();
    info!("Count: {}", count);
    info!("Time taken: {:.2?}", elapsed);
    
    // 170k_tokens
    let history = vec![987, 4015, 935, 2940, 3947, 987, 4015, 3042, 652, 987, 3211, 278, 4230];
    // let history = vec![987, 4015, 935, 2940, 3947, 987];
    // smoothed_trie.set_all_ruleset_by_length(3);
    // let probabilities = smoothed_trie.get_prediction_probabilities(&history);

    // for (rule, token_probs) in &probabilities {
    //     let total_prob: f64 = token_probs.iter().map(|(_, prob)| prob).sum();
    //     println!("Rule: {}, Total Probability: {}", rule, total_prob);
    // }
    //println!("{:?}", probabilities[0]);
    
    smoothed_trie.set_all_ruleset_by_length(7);

    // 475m_tokens
    //let history = vec![157, 973, 712, 132, 3618, 237, 132, 4988, 134, 234, 342, 330, 4389, 3143];
    //test_seq_smoothing(&mut smoothed_trie, history);
    smoothed_trie.get_prediction_probabilities(&vec![987, 4015, 935, 2940, 3947, 987, 4015]);
    smoothed_trie.debug_cache_sizes();
}

fn test_seq_smoothing(smoothed_trie: &mut SmoothedTrie, tokens: Vec<u16>) {
    info!("----- Testing smoothing -----");
    let start = Instant::now();
    for i in 0..tokens.len() - smoothed_trie.trie.n_gram_max_length as usize + 1 {
        let rule = tokens[i..i + smoothed_trie.trie.n_gram_max_length as usize - 1].to_vec();
        let probabilities = smoothed_trie.get_prediction_probabilities(&rule);
        smoothed_trie.debug_cache_sizes();
    }
    let elapsed = start.elapsed();
    let seq_words = tokens.len() - smoothed_trie.trie.n_gram_max_length as usize + 1;
    info!("Time taken for {:?} sequential words predictions: {:.2?}", seq_words, elapsed);
}
