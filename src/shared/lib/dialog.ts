import { open } from '@tauri-apps/plugin-dialog';

export async function openEmlFileDialog(): Promise<string[] | null> {
  const result = await open({
    multiple: true,
    filters: [{ name: 'EML 파일', extensions: ['eml'] }],
  });
  if (!result) return null;
  return Array.isArray(result) ? result : [result];
}
