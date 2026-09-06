import RoleModel from '../models/roles-permission.model';
import { RolePermissions } from './role-permission';

export const ensureRoles = async () => {
  for (const [name, permission] of Object.entries(RolePermissions)) {
    const existingRole = await RoleModel.findOne({ name });

    if (!existingRole) {
      await RoleModel.create({ name, permission });
    }
  }
};
