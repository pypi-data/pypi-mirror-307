import os


def get_project_root(root_identifiers: set = None, start_path: str = os.getcwd()) -> str:
    """프로젝트 루트 경로를 자동으로 추출하는 함수.

    Args:
        start_path (str): 탐색을 시작할 경로. 기본값은 현재 작업 디렉토리.

    Returns:
        str: 프로젝트 루트 경로.
        :param start_path:
        :param root_identifiers:
    """
    # 확인할 파일 목록: 프로젝트 루트에 있는지 확인할 파일들
    root_identifiers1 = root_identifiers or {'.idea'}

    # 현재 경로를 설정
    current_path = start_path

    # 루트 경로가 아니고 상위 디렉토리가 있는 동안 탐색
    while current_path != os.path.dirname(current_path):
        # 현재 디렉토리 내에 루트 식별 파일들이 있는지 확인
        if any(os.path.exists(os.path.join(current_path, identifier)) for identifier in root_identifiers1):
            return current_path  # 루트 경로 반환
        # 상위 디렉토리로 이동
        current_path = os.path.dirname(current_path)

    # 루트를 찾지 못한 경우 현재 작업 디렉토리 반환
    return start_path