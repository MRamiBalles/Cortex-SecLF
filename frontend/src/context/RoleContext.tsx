"use client"

import React, { createContext, useContext, useState, ReactNode } from 'react';

export type UserRole = 'CISO' | 'ARCHITECT' | 'ANALYST';

interface RoleContextType {
    role: UserRole;
    setRole: (role: UserRole) => void;
    canAction: (action: string) => boolean;
}

const RoleContext = createContext<RoleContextType | undefined>(undefined);

export function RoleProvider({ children }: { children: ReactNode }) {
    const [role, setRole] = useState<UserRole>('ARCHITECT');

    const canAction = (action: string): boolean => {
        if (role === 'CISO') return true; // CISO has absolute power

        switch (action) {
            case 'PROMOTE_CODE':
                return role === 'ARCHITECT';
            case 'GRANT_CONSENT':
                return role === 'CISO';
            case 'VIEW_TELEMETRY':
                return true;
            case 'TERMINATE_AGENT':
                return role === 'ARCHITECT' || role === 'CISO';
            default:
                return false;
        }
    };

    return (
        <RoleContext.Provider value={{ role, setRole, canAction }}>
            {children}
        </RoleContext.Provider>
    );
}

export function useRole() {
    const context = useContext(RoleContext);
    if (context === undefined) {
        throw new Error('useRole must be used within a RoleProvider');
    }
    return context;
}
