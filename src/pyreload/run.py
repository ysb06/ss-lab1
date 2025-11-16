import subprocess
import re  # 정규 표현식을 사용하기 위해 추가
import os


def run_and_get_output(password_guess, proc_path="../flush-reload/flush-reload"):
    proc_dir = os.path.dirname(proc_path)
    if proc_dir == "":  # 경로가 비어있으면 현재 디렉터리 의미
        proc_dir = "."
    proc_name = os.path.basename(proc_path)
    command = [f"./{proc_name}", password_guess]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            cwd=proc_dir,
        )
        return result.stdout

    except FileNotFoundError:
        print(f"오류: './flush-reload' 파일을 찾을 수 없습니다.")
        return None
    except subprocess.CalledProcessError as e:
        return e.stdout
    except Exception as e:
        print(f"예기치 않은 오류 발생: {e}")
        return None


def get_time_from_run(password_guess, proc_path="../flush-reload/flush-reload"):
    stdout_output = run_and_get_output(password_guess, proc_path)

    if stdout_output:
        match = re.search(r"-> time: (\d+)", stdout_output)

        if match:
            time_str = match.group(1)
            return int(time_str)
        else:
            print(f"오류: 출력에서 '-> time:' 패턴을 찾을 수 없습니다.")
            print("--- 전체 출력 ---")
            print(stdout_output)
            print("-----------------")
            return None
    else:
        return None
