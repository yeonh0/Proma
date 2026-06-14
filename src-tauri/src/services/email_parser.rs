use mailparse::{parse_mail, MailHeaderMap};
use std::path::Path;

#[derive(Debug)]
pub struct ParsedAttachment {
    pub filename: String,
    pub content_type: String,
    pub size_bytes: usize,
    pub data: Vec<u8>,
}

#[derive(Debug)]
pub struct ParsedEmail {
    pub message_id: Option<String>,
    pub subject: Option<String>,
    pub sender: Option<String>,
    pub recipients: Vec<String>,
    pub cc: Vec<String>,
    pub body_text: Option<String>,
    pub body_html: Option<String>,
    pub sent_at: Option<String>,
    pub attachments: Vec<ParsedAttachment>,
}

pub fn parse_eml(raw: &[u8]) -> Result<ParsedEmail, String> {
    let mail = parse_mail(raw).map_err(|e| format!("EML 파싱 오류: {e}"))?;
    let headers = &mail.headers;

    let message_id = headers
        .get_first_value("Message-ID")
        .map(|s| s.trim_matches(|c| c == '<' || c == '>').to_string());
    let subject = headers.get_first_value("Subject");
    let sender = headers.get_first_value("From");
    let sent_at = headers.get_first_value("Date");

    let recipients = headers
        .get_first_value("To")
        .unwrap_or_default()
        .split(',')
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty())
        .collect();

    let cc = headers
        .get_first_value("CC")
        .unwrap_or_default()
        .split(',')
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty())
        .collect();

    let mut body_text = None;
    let mut body_html = None;
    let mut attachments = Vec::new();

    collect_parts(&mail, &mut body_text, &mut body_html, &mut attachments);

    Ok(ParsedEmail {
        message_id,
        subject,
        sender,
        recipients,
        cc,
        body_text,
        body_html,
        sent_at,
        attachments,
    })
}

fn collect_parts(
    part: &mailparse::ParsedMail,
    text: &mut Option<String>,
    html: &mut Option<String>,
    attachments: &mut Vec<ParsedAttachment>,
) {
    let ct = part.ctype.mimetype.to_lowercase();

    if part.subparts.is_empty() {
        let disposition = part
            .headers
            .get_first_value("Content-Disposition")
            .unwrap_or_default()
            .to_lowercase();
        let is_attachment = disposition.starts_with("attachment")
            || (disposition.starts_with("inline")
                && !matches!(ct.as_str(), "text/plain" | "text/html"));

        if is_attachment {
            let filename = extract_filename(part);
            if let Ok(data) = part.get_body_raw() {
                let size_bytes = data.len();
                attachments.push(ParsedAttachment {
                    filename,
                    content_type: ct,
                    size_bytes,
                    data,
                });
            }
        } else if ct == "text/plain" && text.is_none() {
            *text = part.get_body().ok();
        } else if ct == "text/html" && html.is_none() {
            *html = part.get_body().ok();
        }
    } else {
        for sub in &part.subparts {
            collect_parts(sub, text, html, attachments);
        }
    }
}

fn extract_filename(part: &mailparse::ParsedMail) -> String {
    if let Some(disp) = part.headers.get_first_value("Content-Disposition") {
        if let Some(name) = extract_param(&disp, "filename") {
            return name;
        }
    }
    if let Some(name) = extract_param(&part.ctype.params.iter()
        .map(|(k, v)| format!("{k}={v}"))
        .collect::<Vec<_>>()
        .join("; "), "name")
    {
        return name;
    }
    "attachment".to_string()
}

fn extract_param(header: &str, key: &str) -> Option<String> {
    let lower = header.to_lowercase();
    let needle = format!("{key}=");
    let pos = lower.find(&needle)?;
    let rest = &header[pos + needle.len()..];
    let value = if rest.starts_with('"') {
        rest[1..].split('"').next()?.to_string()
    } else {
        rest.split(';').next()?.trim().to_string()
    };
    Some(value)
}

pub fn save_attachments(
    email_id: i64,
    attachments: &[ParsedAttachment],
    base_dir: &Path,
) -> Vec<(String, String, usize)> {
    let dir = base_dir.join("attachments").join(email_id.to_string());
    let _ = std::fs::create_dir_all(&dir);

    attachments
        .iter()
        .filter_map(|att| {
            let path = dir.join(&att.filename);
            std::fs::write(&path, &att.data).ok()?;
            Some((
                att.filename.clone(),
                att.content_type.clone(),
                att.size_bytes,
            ))
        })
        .collect()
}
