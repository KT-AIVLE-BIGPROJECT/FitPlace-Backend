from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):
    ## 글 조회는 누구나 가능 / 글 작성은 로그인한 유저만 / 글 수정은 작성자만
    
    # 전체 객체에 대한 권한
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_authenticated
    
    # 각 객체별 권한
    def has_object_permission(self, request, view, obj):
        # 데이터에 영향을 미치지 않는 메소드 (GET 등)은 통과
        if request.method in permissions.SAFE_METHODS:
            return True
        # PUT/PATCH 등의 경우에는 요청으로 들어온 유저와 객체의 유저를 비교해 같으면 통과
        return obj.author == request.user
