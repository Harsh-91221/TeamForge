import { describe, it, expect, vi, beforeEach } from 'vitest';
import mongoose from 'mongoose';
import { joinWorkspaceAsMemberOnLogin } from '../src/services/auth.service';
import WorkspaceModel from '../src/models/workspace.model';
import MemberModel from '../src/models/member.model';
import RoleModel from '../src/models/roles-permission.model';
import UserModel from '../src/models/user.model';

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

vi.mock('../src/models/user.model', () => ({
  __esModule: true,
  default: {
    findById: vi.fn(),
  },
}));

describe('joinWorkspaceAsMemberOnLogin', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  const workspaceId = 'workspace123';
  const userId = 'user123';
  const inviteCode = 'ABC123';

  it('should join user as member and update currentWorkspace', async () => {
    const workspaceDoc = { _id: workspaceId };
    (WorkspaceModel.findOne as any).mockReturnValue({
      exec: vi.fn().mockResolvedValue(workspaceDoc),
    });
    (RoleModel.findOne as any).mockReturnValue({
      exec: vi.fn().mockResolvedValue({ _id: 'role_member' }),
    });
    (MemberModel.findOneAndUpdate as any).mockReturnValue({
      exec: vi.fn().mockResolvedValue({}),
    });
    (UserModel.findById as any).mockResolvedValue({
      _id: userId,
      currentWorkspace: null,
      save: vi.fn().mockResolvedValue(undefined),
    });

    const result = await joinWorkspaceAsMemberOnLogin(userId, inviteCode);

    expect(result).toBe(workspaceId);
    expect(MemberModel.findOneAndUpdate).toHaveBeenCalledWith(
      { userId, workspaceId },
      { $setOnInsert: { role: 'role_member', joinedAt: expect.any(Date) } },
      { upsert: true, new: true }
    );
    expect(UserModel.findById).toHaveBeenCalledWith(userId);
  });

  it('should throw if workspace not found', async () => {
    (WorkspaceModel.findOne as any).mockReturnValue({
      exec: vi.fn().mockResolvedValue(null),
    });

    await expect(joinWorkspaceAsMemberOnLogin(userId, inviteCode)).rejects.toThrow('Invalid invite code');
  });
});
