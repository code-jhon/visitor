/**
 * Secure token storage abstraction (VIS-2).
 *
 * On device this should be backed by Expo SecureStore / react-native-keychain
 * (Keychain on iOS, Keystore on Android). To keep the scaffold buildable
 * without native modules, the default implementation is an in-memory store;
 * swap `impl` for the SecureStore-backed version when wiring native deps.
 */
export interface TokenStorage {
  get(key: string): Promise<string | null>;
  set(key: string, value: string): Promise<void>;
  remove(key: string): Promise<void>;
}

const memory = new Map<string, string>();

const inMemoryStorage: TokenStorage = {
  async get(key) {
    return memory.get(key) ?? null;
  },
  async set(key, value) {
    memory.set(key, value);
  },
  async remove(key) {
    memory.delete(key);
  },
};

export const tokenStorage: TokenStorage = inMemoryStorage;
