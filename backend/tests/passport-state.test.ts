import { describe, it, expect, vi } from 'vitest';
import { generateState, verifyState } from '../src/config/passport.config';

describe('OAuth state helpers', () => {
  it('should generate a signed state token containing invite code', () => {
    const inviteCode = 'ABC123';
    const token = generateState(inviteCode);
    expect(typeof token).toBe('string');
    expect(token.length).toBeGreaterThan(10);
  });

  it('should return undefined for invalid token', () => {
    const result = verifyState('invalid-token');
    expect(result).toBeUndefined();
  });
});
