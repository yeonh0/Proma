import { invoke } from '@tauri-apps/api/core';

export async function invokeCommand<T>(command: string, args?: Record<string, unknown>): Promise<T> {
  if (!('__TAURI_INTERNALS__' in window)) {
    throw new Error(
      `Tauri IPC 브릿지가 초기화되지 않았습니다. ` +
      `Tauri 앱 창에서 실행 중인지 확인하세요 (브라우저에서 직접 열면 동작하지 않습니다). ` +
      `커맨드: ${command}`
    );
  }
  return invoke<T>(command, args);
}
