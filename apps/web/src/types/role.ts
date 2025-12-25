export interface Permission {
    id: number;
    name: string;
    description?: string;
    module: string;
}

export interface PermissionGroup {
    module: string;
    permissions: Permission[];
}

export interface Role {
    id: number;
    name: string;
    description?: string;
    is_system: boolean;
    is_active: boolean;
    permissions: Permission[];
}

export interface RoleCreateDTO {
    name: string;
    description?: string;
    permission_ids: number[];
}

export interface RoleUpdateDTO {
    name?: string;
    description?: string;
    is_active?: boolean;
    permission_ids?: number[];
}

export interface PermissionAuditLog {
    id: number;
    actor_id: number;
    actor_name?: string;
    role_id: number;
    role_name?: string;
    action: 'ADD_PERMISSION' | 'REMOVE_PERMISSION';
    permission_name: string;
    timestamp: string;
}
