// engine/tests/load_test.rs
use divina_ludus::loader::load_pack_from_path;
use std::path::Path;

#[test]
fn test_heungbu_nolbu_pack_loading() {
    let pack_path = Path::new("../packs/heungbu_nolbu/4_game_scene.yaml");
    let pack = load_pack_from_path(pack_path).expect("Failed to load pack");

    println!("Pack Title: {}", pack.meta.title);
    println!("Loaded Scenes count: {}", pack.scenes.len());

    assert_eq!(pack.meta.title, "흥부놀부전");
    assert!(!pack.scenes.is_empty(), "Scenes should not be empty");

    for (id, scene) in &pack.scenes {
        println!("- Scene ID: {}, act: {}, choices: {}, art_lines: {}", id, scene.act, scene.choices.len(), scene.scene_art.len());
    }
}
