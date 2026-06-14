-- V001 rollback
-- 인덱스는 테이블 DROP 시 SQLite가 자동 제거
-- 자식 테이블 → 부모 테이블 순으로 삭제

DROP TABLE IF EXISTS ai_results;
DROP TABLE IF EXISTS email_tags;
DROP TABLE IF EXISTS email_project_mappings;
DROP TABLE IF EXISTS email_attachments;
DROP TABLE IF EXISTS emails;
DROP TABLE IF EXISTS schedule_tags;
DROP TABLE IF EXISTS project_tags;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS schedules;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS settings;
