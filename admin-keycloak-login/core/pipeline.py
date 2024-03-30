from django.contrib.auth.models import Group

def save_keycloak_groups(backend, user, response, *args, **kwargs):
    if backend.name == 'keycloak':
        keycloak_groups = response.get('groups', [])
        print(keycloak_groups)

        # Django의 Group 모델과 연동하여 사용자에게 그룹을 할당
        for group_name in keycloak_groups:
            # Django Group 모델에서 그룹을 찾거나 새로 생성
            group, created = Group.objects.get_or_create(name=group_name)

            # 사용자를 그룹에 추가
            user.groups.add(group)

        # 변경사항을 저장
        user.save()

def rbac_for_admin(backend, user, response, *args, **kwargs):
    if backend.name == 'keycloak':
        keycloak_groups = response.get('groups', [])

        # django-staff -> staff 권한 자동 획득
        if 'django-staff' in keycloak_groups:
            user.is_staff = True
            user.save()
        # django-superuser -> staff & superuser 권한 자동 획득
        if 'django-superuser' in keycloak_groups:
            user.is_staff = True
            user.is_superuser = True
            user.save()
