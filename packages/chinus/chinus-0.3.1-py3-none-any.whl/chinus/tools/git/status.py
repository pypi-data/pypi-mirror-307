import subprocess


def has_modified_files() -> bool:
    """
    Git 상태를 확인하여 수정된 파일이 있는지 여부를 반환합니다.

    Returns:
        bool: 수정된 파일이 있으면 True, 없으면 False.
    """
    # 'git status --porcelain'으로 변경 사항이 있는지 확인
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

    # stdout이 비어있지 않으면 수정된 파일이 있다는 뜻
    return bool(result.stdout.strip())