export interface Email {
  id: number;
  message_id: string | null;
  subject: string | null;
  sender: string | null;
  recipients: string | null;
  cc: string | null;
  body_text: string | null;
  body_html: string | null;
  sent_at: string | null;
  imported_at: string;
  file_path: string | null;
  created_at: string;
}

export interface EmailAttachment {
  id: number;
  email_id: number;
  filename: string;
  content_type: string | null;
  size_bytes: number | null;
  file_path: string | null;
  created_at: string;
}

export interface EmailProjectMapping {
  id: number;
  email_id: number;
  project_id: number;
  mapped_by: string;
  is_confirmed: boolean;
  confidence: number | null;
  created_at: string;
}

export interface EmailWithMeta {
  email: Email;
  attachments: EmailAttachment[];
  project_ids: number[];
}
