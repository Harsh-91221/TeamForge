import { describe, it, expect, vi, beforeEach } from 'vitest';
import { joinWorkspaceByInviteService } from '../src/services/member.service';
import WorkspaceModel from '../src/models/workspace.model';
import RoleModel from '../src/models/roles-permission.model';
import MemberModel from '../src/models/member.model';

vi.mock('../src/models/workspace.model', () => ({
  __esModule: true,
  default: {
    findOne: vi.fn(),
  },
}));

vi.mock('../src/models/member.model', () => ({
  __esModule: true,
  default: {
    findOneAndUpdate: vi.fn(),
  },
}));

vi.mock('../src/models/roles-permission.model', () => ({
  __esModule: true,
  default: {
    findOne: vi.fn(),
  },
}));

describe('joinWorkspaceByInviteService', () => {
  beforeEach(() => vi.clearAllMocks());

  it('should return existing member role when already a member', async () => {
    const workspaceId = 'ws1';
    const userId = 'user1';
    const inviteCode = 'CODE';

    (WorkspaceModel.findOne as any).mockReturnValue({
      exec: vi.fn().mockResolvedValue({ _id: workspaceId }),
    });
    (RoleModel.findOne as any).mockReturnValue({
      exec: vi.fn().mockResolvedValue({ _id: 'role_member' }),
    });
    (MemberModel.findOneAndUpdate as any).mockReturnValue({
      exec: vi.fn().mockResolvedValue({ role: { name: 'ADMIN' } }),
    });

    const result = await joinWorkspaceByInviteService(userId, inviteCode);

    expect(result.role).toBe('ADMIN');
  });

  it('should return MEMBER role for new member', async () => {
    const workspaceId = 'ws1';
    const userId = 'user1';
    const inviteCode = 'CODE';

    (WorkspaceModel.findOne as any).mockReturnValue({
      exec: vi.fn().mockResolvedValue({ _id: workspaceId }),
    });
    (RoleModel.findOne as any).mockReturnValue({
      exec: vi.fn().mockResolvedValue({ _id: 'role_member' }),
    });
    (MemberModel.findOneAndUpdate as any).mockReturnValue({
      exec: vi.fn().mockResolvedValue({ role: { name: 'MEMBER' } }),
    });

    const result = await joinWorkspaceByInviteService(userId, inviteCode);

    expect(result.role).toBe('MEMBER');
  });
});
