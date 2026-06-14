use rusqlite::{params, Connection};

use crate::models::email::{Email, EmailAttachment, EmailProjectMapping};

const EMAIL_COLS: &str =
    "id, message_id, subject, sender, recipients, cc, body_text, body_html, sent_at, imported_at, file_path, created_at";

fn map_email(row: &rusqlite::Row) -> rusqlite::Result<Email> {
    Ok(Email {
        id: row.get(0)?,
        message_id: row.get(1)?,
        subject: row.get(2)?,
        sender: row.get(3)?,
        recipients: row.get(4)?,
        cc: row.get(5)?,
        body_text: row.get(6)?,
        body_html: row.get(7)?,
        sent_at: row.get(8)?,
        imported_at: row.get(9)?,
        file_path: row.get(10)?,
        created_at: row.get(11)?,
    })
}

pub struct CreateEmailParams<'a> {
    pub message_id: Option<&'a str>,
    pub subject: Option<&'a str>,
    pub sender: Option<&'a str>,
    pub recipients_json: Option<&'a str>,
    pub cc_json: Option<&'a str>,
    pub body_text: Option<&'a str>,
    pub body_html: Option<&'a str>,
    pub sent_at: Option<&'a str>,
    pub file_path: Option<&'a str>,
}

pub fn create(conn: &Connection, p: &CreateEmailParams) -> rusqlite::Result<Email> {
    conn.execute(
        "INSERT INTO emails
             (message_id, subject, sender, recipients, cc, body_text, body_html, sent_at, file_path)
         VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)",
        params![
            p.message_id, p.subject, p.sender, p.recipients_json, p.cc_json,
            p.body_text, p.body_html, p.sent_at, p.file_path,
        ],
    )?;
    let id = conn.last_insert_rowid();
    get(conn, id)?.ok_or(rusqlite::Error::QueryReturnedNoRows)
}

pub fn list(conn: &Connection) -> rusqlite::Result<Vec<Email>> {
    let sql = format!("SELECT {EMAIL_COLS} FROM emails ORDER BY sent_at DESC, created_at DESC");
    let mut stmt = conn.prepare(&sql)?;
    let rows = stmt.query_map([], map_email)?;
    rows.collect()
}

pub fn get(conn: &Connection, id: i64) -> rusqlite::Result<Option<Email>> {
    let sql = format!("SELECT {EMAIL_COLS} FROM emails WHERE id = ?1");
    let mut stmt = conn.prepare(&sql)?;
    let mut rows = stmt.query_map([id], map_email)?;
    rows.next().transpose()
}

pub fn get_by_message_id(conn: &Connection, message_id: &str) -> rusqlite::Result<Option<Email>> {
    let sql = format!("SELECT {EMAIL_COLS} FROM emails WHERE message_id = ?1");
    let mut stmt = conn.prepare(&sql)?;
    let mut rows = stmt.query_map([message_id], map_email)?;
    rows.next().transpose()
}

pub fn delete(conn: &Connection, id: i64) -> rusqlite::Result<bool> {
    let n = conn.execute("DELETE FROM emails WHERE id = ?1", [id])?;
    Ok(n > 0)
}

pub fn create_attachment(
    conn: &Connection,
    email_id: i64,
    filename: &str,
    content_type: &str,
    size_bytes: usize,
    file_path: &str,
) -> rusqlite::Result<EmailAttachment> {
    conn.execute(
        "INSERT INTO email_attachments (email_id, filename, content_type, size_bytes, file_path)
         VALUES (?1, ?2, ?3, ?4, ?5)",
        params![email_id, filename, content_type, size_bytes as i64, file_path],
    )?;
    let id = conn.last_insert_rowid();
    let att = conn.query_row(
        "SELECT id, email_id, filename, content_type, size_bytes, file_path, created_at
         FROM email_attachments WHERE id = ?1",
        [id],
        |row| {
            Ok(EmailAttachment {
                id: row.get(0)?,
                email_id: row.get(1)?,
                filename: row.get(2)?,
                content_type: row.get(3)?,
                size_bytes: row.get(4)?,
                file_path: row.get(5)?,
                created_at: row.get(6)?,
            })
        },
    )?;
    Ok(att)
}

pub fn list_attachments(conn: &Connection, email_id: i64) -> rusqlite::Result<Vec<EmailAttachment>> {
    let mut stmt = conn.prepare(
        "SELECT id, email_id, filename, content_type, size_bytes, file_path, created_at
         FROM email_attachments WHERE email_id = ?1 ORDER BY id ASC",
    )?;
    let rows = stmt.query_map([email_id], |row| {
        Ok(EmailAttachment {
            id: row.get(0)?,
            email_id: row.get(1)?,
            filename: row.get(2)?,
            content_type: row.get(3)?,
            size_bytes: row.get(4)?,
            file_path: row.get(5)?,
            created_at: row.get(6)?,
        })
    })?;
    rows.collect()
}

pub fn link_project(conn: &Connection, email_id: i64, project_id: i64) -> rusqlite::Result<EmailProjectMapping> {
    conn.execute(
        "INSERT OR IGNORE INTO email_project_mappings (email_id, project_id, mapped_by, is_confirmed)
         VALUES (?1, ?2, 'user', 1)",
        params![email_id, project_id],
    )?;
    get_mapping(conn, email_id, project_id)?.ok_or(rusqlite::Error::QueryReturnedNoRows)
}

pub fn unlink_project(conn: &Connection, email_id: i64, project_id: i64) -> rusqlite::Result<bool> {
    let n = conn.execute(
        "DELETE FROM email_project_mappings WHERE email_id = ?1 AND project_id = ?2",
        params![email_id, project_id],
    )?;
    Ok(n > 0)
}

pub fn list_project_ids(conn: &Connection, email_id: i64) -> rusqlite::Result<Vec<i64>> {
    let mut stmt = conn.prepare(
        "SELECT project_id FROM email_project_mappings WHERE email_id = ?1 AND is_confirmed = 1",
    )?;
    let rows = stmt.query_map([email_id], |row| row.get(0))?;
    rows.collect()
}

fn get_mapping(conn: &Connection, email_id: i64, project_id: i64) -> rusqlite::Result<Option<EmailProjectMapping>> {
    let mut stmt = conn.prepare(
        "SELECT id, email_id, project_id, mapped_by, is_confirmed, confidence, created_at
         FROM email_project_mappings WHERE email_id = ?1 AND project_id = ?2",
    )?;
    let mut rows = stmt.query_map(params![email_id, project_id], |row| {
        Ok(EmailProjectMapping {
            id: row.get(0)?,
            email_id: row.get(1)?,
            project_id: row.get(2)?,
            mapped_by: row.get(3)?,
            is_confirmed: row.get::<_, i64>(4)? != 0,
            confidence: row.get(5)?,
            created_at: row.get(6)?,
        })
    })?;
    rows.next().transpose()
}
