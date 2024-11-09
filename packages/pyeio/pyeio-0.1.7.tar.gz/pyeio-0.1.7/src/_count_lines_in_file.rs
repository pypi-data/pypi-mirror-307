use memchr::memchr_iter;
use memmap2::MmapOptions;
use rayon::prelude::*;
use rayon::ThreadPoolBuilder;
use std::fs::File;
use std::io;

pub fn call(filename: &str, chunk_size: usize, num_threads: usize) -> io::Result<usize> {
    // Open the file.
    let file = File::open(filename)?;

    // Memory-map the file.
    let mmap = unsafe { MmapOptions::new().map(&file)? };

    // Create a local thread pool with the specified number of threads.
    let pool = ThreadPoolBuilder::new()
        .num_threads(num_threads)
        .build()
        .unwrap();

    // Use the local thread pool to execute the computation.
    let lines = pool.install(|| {
        mmap.par_chunks(chunk_size)
            .map(|chunk| memchr_iter(b'\n', chunk).count())
            .sum()
    });

    Ok(lines)
}
