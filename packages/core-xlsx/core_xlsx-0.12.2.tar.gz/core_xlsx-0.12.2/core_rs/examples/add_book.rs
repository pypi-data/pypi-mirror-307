use std::time::Instant;

use core_rs::writer::book::XLSXBook;

fn main() -> anyhow::Result<()> {
    let start = Instant::now();

    let mut book = XLSXBook::new();
    let _ = book.add_sheet("A".to_string(), Some(5), Some(5));

    let sheet = book.get_sheet_name("A".to_string());
    println!(
        "Find NameSheet {:?}",
        sheet.map(|s| s.lock().unwrap().name.clone())
    );

    let sheet = book.get_sheet_index(0);
    println!(
        "Find Idx Sheet {:?}",
        sheet.map(|s| s.lock().unwrap().name.clone())
    );

    let end = start.elapsed();
    println!(
        "Выполнено за: {}.{:03} сек.",
        end.as_secs(),
        end.subsec_millis(),
    );

    Ok(())
}
