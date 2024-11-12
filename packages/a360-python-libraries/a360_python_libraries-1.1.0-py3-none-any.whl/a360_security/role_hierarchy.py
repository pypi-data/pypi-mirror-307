from a360_security.enums.role import Role

ROLE_HIERARCHY = {
    Role.PRACTICE_SECRETARY: [],
    Role.PRACTICE_DOCTOR: [
        Role.PRACTICE_SECRETARY.value,
    ],
    Role.PRACTICE_OFFICE_ADMIN: [
        Role.PRACTICE_DOCTOR.value,
        Role.PRACTICE_SECRETARY.value,
    ],
    Role.PRACTICE_ADMIN: [
        Role.PRACTICE_DOCTOR.value,
        Role.PRACTICE_OFFICE_ADMIN.value,
        Role.PRACTICE_SECRETARY.value,
    ],
    Role.AI_TESTER: [],
    Role.SERVICE: [],
    Role.ADMIN: [
        Role.SERVICE.value,
        Role.AI_TESTER.value,
        Role.PRACTICE_ADMIN.value,
        Role.PRACTICE_OFFICE_ADMIN.value,
        Role.PRACTICE_DOCTOR.value,
        Role.PRACTICE_SECRETARY.value,
    ],
}

ROLES_PRACTICE = [
    Role.PRACTICE_SECRETARY,
    Role.PRACTICE_DOCTOR,
    Role.PRACTICE_OFFICE_ADMIN,
    Role.PRACTICE_ADMIN,
]


def has_role(user_roles: list[str], required_role: Role) -> bool:
    all_roles = set(user_roles)
    roles_to_check = list(user_roles)
    while roles_to_check:
        role = roles_to_check.pop()
        if role in ROLE_HIERARCHY:
            inherited_roles = ROLE_HIERARCHY[role]
            for inherited_role in inherited_roles:
                if inherited_role not in all_roles:
                    all_roles.add(inherited_role)
                    roles_to_check.append(inherited_role)

    return required_role.value in all_roles
