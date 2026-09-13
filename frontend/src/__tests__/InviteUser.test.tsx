import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { HashRouter } from 'react-router-dom';
import InviteUser from '../page/invite/InviteUser';
import useAuth from '../hooks/api/use-auth';
import { useMutation } from '@tanstack/react-query';

vi.mock('../hooks/api/use-auth', () => ({
  default: vi.fn(),
}));

vi.mock('@tanstack/react-query', () => ({
  useMutation: vi.fn(),
  useQueryClient: () => ({ resetQueries: vi.fn() }),
}));

vi.mock('@/lib/api', () => ({
  invitedUserJoinWorkspaceMutationFn: vi.fn().mockResolvedValue({ workspaceId: 'ws123' }),
}));

describe('InviteUser', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders invite heading when not authenticated', async () => {
    vi.mocked(useAuth).mockReturnValue({ data: undefined, isPending: false } as unknown as ReturnType<typeof useAuth>);
    vi.mocked(useMutation).mockReturnValue({ mutate: vi.fn(), isPending: false } as unknown as ReturnType<typeof useMutation>);

    render(
      <HashRouter>
        <InviteUser />
      </HashRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Hey there! You're invited/i)).toBeInTheDocument();
    });
  });
});
