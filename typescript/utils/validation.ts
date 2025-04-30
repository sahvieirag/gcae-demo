export const USER_ID_PREFIX = "usr_";
const ID_MIN_LENGTH_AFTER_PREFIX = 8;

export function isValidUserId(id: string): boolean {
  if (!id) return false;
  const isValid = id.startsWith(USER_ID_PREFIX) && id.length >= USER_ID_PREFIX.length + ID_MIN_LENGTH_AFTER_PREFIX;
  if (!isValid) {
    console.warn(`[VALIDATION_FAIL] Invalid User ID format: ${id}. Must start with ${USER_ID_PREFIX} and have at least ${ID_MIN_LENGTH_AFTER_PREFIX} chars after prefix.`);
  } else {
    console.log(`[VALIDATION_PASS] User ID format valid: ${id}`);
  }
  return isValid;
}

export function generateStandardId(prefix: string, length: number = 12): string {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = prefix;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    console.log(`[ID_FACTORY] Generated ID: ${result} with prefix ${prefix}`);
    return result;
}