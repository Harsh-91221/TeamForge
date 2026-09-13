import { describe, it, expect } from 'vitest';
import { getInviteCodeFromHash } from '../components/auth/google-oauth-button';

describe('getInviteCodeFromHash', () => {
  it('should extract invite code from direct hash query', () => {
    const saved = window.location.hash;
    window.location.hash = '#/?inviteCode=ABC123';
    expect(getInviteCodeFromHash()).toBe('ABC123');
    window.location.hash = saved;
  });
});
