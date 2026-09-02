// engine/src/yaml_parser.rs
// Divina Ludus 초경량 순수 Rust YAML/JSON 파서 (Robust)

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub enum YamlValue {
    String(String),
    Int(i64),
    Float(f64),
    Bool(bool),
    List(Vec<YamlValue>),
    Map(HashMap<String, YamlValue>),
    Null,
}

impl YamlValue {
    pub fn as_str(&self) -> Option<&str> {
        match self {
            YamlValue::String(s) => Some(s),
            _ => None,
        }
    }

    pub fn as_i64(&self) -> Option<i64> {
        match self {
            YamlValue::Int(n) => Some(*n),
            YamlValue::Float(f) => Some(*f as i64),
            YamlValue::String(s) => s.trim().parse::<i64>().ok(),
            _ => None,
        }
    }

    pub fn as_i32(&self) -> Option<i32> {
        self.as_i64().map(|n| n as i32)
    }

    pub fn as_bool(&self) -> Option<bool> {
        match self {
            YamlValue::Bool(b) => Some(*b),
            YamlValue::String(s) => match s.to_lowercase().as_str() {
                "true" | "yes" | "y" | "1" => Some(true),
                "false" | "no" | "n" | "0" => Some(false),
                _ => None,
            },
            _ => None,
        }
    }

    pub fn as_list(&self) -> Option<&Vec<YamlValue>> {
        match self {
            YamlValue::List(l) => Some(l),
            _ => None,
        }
    }

    pub fn as_map(&self) -> Option<&HashMap<String, YamlValue>> {
        match self {
            YamlValue::Map(m) => Some(m),
            _ => None,
        }
    }

    pub fn get(&self, key: &str) -> Option<&YamlValue> {
        self.as_map().and_then(|m| m.get(key))
    }

    pub fn get_str(&self, key: &str) -> Option<&str> {
        self.get(key).and_then(|v| v.as_str())
    }

    pub fn get_i32(&self, key: &str) -> Option<i32> {
        self.get(key).and_then(|v| v.as_i32())
    }

    pub fn get_bool(&self, key: &str) -> Option<bool> {
        self.get(key).and_then(|v| v.as_bool())
    }
}

pub fn parse_yaml(input: &str) -> Result<YamlValue, String> {
    let mut raw_lines = Vec::new();
    for line in input.lines() {
        let stripped = strip_comment(line);
        if stripped.trim().is_empty() {
            continue;
        }
        let indent = stripped.chars().take_while(|c| *c == ' ').count();
        raw_lines.push((indent, stripped.trim().to_string()));
    }

    if raw_lines.is_empty() {
        return Ok(YamlValue::Null);
    }

    let (val, _) = parse_node(&raw_lines, 0);
    Ok(val)
}

fn strip_comment(line: &str) -> &str {
    let mut in_quote = false;
    let mut quote_c = ' ';
    let mut prev_backslash = false;

    for (i, c) in line.char_indices() {
        if prev_backslash {
            prev_backslash = false;
            continue;
        }
        if c == '\\' {
            prev_backslash = true;
            continue;
        }
        if c == '"' || c == '\'' {
            if in_quote && c == quote_c {
                in_quote = false;
            } else if !in_quote {
                in_quote = true;
                quote_c = c;
            }
        } else if c == '#' && !in_quote {
            return &line[..i];
        }
    }
    line
}

fn parse_node(lines: &[(usize, String)], start: usize) -> (YamlValue, usize) {
    if start >= lines.len() {
        return (YamlValue::Null, start);
    }

    let base_indent = lines[start].0;
    let is_list = lines[start].1.starts_with("- ") || lines[start].1 == "-";

    if is_list {
        let mut list = Vec::new();
        let mut idx = start;

        while idx < lines.len() {
            let (indent, text) = &lines[idx];
            if *indent < base_indent {
                break;
            }
            if *indent == base_indent && (text.starts_with("- ") || text == "-") {
                let rest = if text == "-" { "" } else { &text[2..] }.trim();

                if rest.is_empty() {
                    // 항목 내용이 다음 줄부터 나옴
                    let (item_val, next_idx) = parse_node(lines, idx + 1);
                    list.push(item_val);
                    idx = next_idx;
                } else if is_mapping_line(rest) {
                    // "- key: val" 형태 -> 한 맵의 시작
                    let mut item_lines = Vec::new();
                    let item_indent = *indent + 2;
                    item_lines.push((item_indent, rest.to_string()));

                    let mut sub_idx = idx + 1;
                    while sub_idx < lines.len() {
                        let (sub_i, sub_t) = &lines[sub_idx];
                        if *sub_i >= item_indent && !(sub_i == indent && (sub_t.starts_with("- ") || sub_t == "-")) {
                            item_lines.push((*sub_i, sub_t.clone()));
                            sub_idx += 1;
                        } else {
                            break;
                        }
                    }

                    let (item_val, _) = parse_node(&item_lines, 0);
                    list.push(item_val);
                    idx = sub_idx;
                } else {
                    list.push(parse_scalar(rest));
                    idx += 1;
                }
            } else if *indent > base_indent {
                idx += 1;
            } else {
                break;
            }
        }
        (YamlValue::List(list), idx)
    } else {
        let mut map = HashMap::new();
        let mut idx = start;

        while idx < lines.len() {
            let (indent, text) = &lines[idx];
            if *indent < base_indent {
                break;
            }

            if *indent == base_indent {
                if let Some((k, v)) = split_key_value(text) {
                    if v.is_empty() {
                        // 다음 줄부터 하위 블록
                        if idx + 1 < lines.len() && lines[idx + 1].0 > *indent {
                            let (child_val, next_idx) = parse_node(lines, idx + 1);
                            map.insert(k, child_val);
                            idx = next_idx;
                        } else {
                            map.insert(k, YamlValue::Null);
                            idx += 1;
                        }
                    } else if v.starts_with('[') && v.ends_with(']') {
                        // 인라인 리스트 [a, b, c]
                        let inner = &v[1..v.len() - 1];
                        let mut items = Vec::new();
                        for item_str in inner.split(',') {
                            let trimmed = item_str.trim();
                            if !trimmed.is_empty() {
                                items.push(parse_scalar(trimmed));
                            }
                        }
                        map.insert(k, YamlValue::List(items));
                        idx += 1;
                    } else {
                        map.insert(k, parse_scalar(&v));
                        idx += 1;
                    }
                } else {
                    idx += 1;
                }
            } else {
                idx += 1;
            }
        }
        (YamlValue::Map(map), idx)
    }
}

fn is_mapping_line(s: &str) -> bool {
    split_key_value(s).is_some()
}

fn split_key_value(s: &str) -> Option<(String, String)> {
    let mut in_quote = false;
    let mut quote_c = ' ';
    let mut prev_backslash = false;

    for (i, c) in s.char_indices() {
        if prev_backslash {
            prev_backslash = false;
            continue;
        }
        if c == '\\' {
            prev_backslash = true;
            continue;
        }
        if c == '"' || c == '\'' {
            if in_quote && c == quote_c {
                in_quote = false;
            } else if !in_quote {
                in_quote = true;
                quote_c = c;
            }
        } else if c == ':' && !in_quote {
            let key = s[..i].trim().trim_matches('"').trim_matches('\'').to_string();
            let val = s[i + 1..].trim().to_string();
            return Some((key, val));
        }
    }
    None
}

fn parse_scalar(s: &str) -> YamlValue {
    let trimmed = s.trim();

    if (trimmed.starts_with('"') && trimmed.ends_with('"'))
        || (trimmed.starts_with('\'') && trimmed.ends_with('\''))
    {
        if trimmed.len() >= 2 {
            let inner = &trimmed[1..trimmed.len() - 1];
            // BUG-015 해결: \\ 언이스케이프 순서 안전 처리
            let unescaped = inner
                .replace("\\\\", "\x00BS\x00")
                .replace("\\\"", "\"")
                .replace("\\'", "'")
                .replace("\\n", "\n")
                .replace("\x00BS\x00", "\\");
            return YamlValue::String(unescaped);
        }
    }

    match trimmed.to_lowercase().as_str() {
        "true" | "yes" => return YamlValue::Bool(true),
        "false" | "no" => return YamlValue::Bool(false),
        "null" | "~" => return YamlValue::Null,
        _ => {}
    }

    if let Ok(n) = trimmed.parse::<i64>() {
        return YamlValue::Int(n);
    }

    if let Ok(f) = trimmed.parse::<f64>() {
        return YamlValue::Float(f);
    }

    YamlValue::String(trimmed.to_string())
}
